import hashlib
import os
import random
import time
import traceback
import urllib
from abc import abstractmethod
from dataclasses import dataclass

import boto3
from boto3 import s3
from selenium import webdriver

from _datetime import datetime
from app.config import Config
from app.db import create_session
from app.models import Article

s3 = boto3.client(
    's3',
    aws_access_key_id=Config.S3_AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.S3_AWS_SECRET_KEY,
)
bucket = Config.BUCKET_NAME
opener = urllib.request.build_opener()
opener.addheaders = [
    (
        'User-Agent',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    ),
    (
        'Accept',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    ),
]
urllib.request.install_opener(opener)


@dataclass
class Crawler:
    base_url: str
    page: int
    name: str
    driver: webdriver.Chrome = webdriver.Chrome('chromedriver')
    s3_domain: str = 'http://img-dev.sscroll.net.s3.amazonaws.com/upload/'

    @abstractmethod
    def load_page(self):
        pass

    @abstractmethod
    def load_page_contents(self):
        pass

    @abstractmethod
    def load_content(self, url):
        pass

    @abstractmethod
    def parse_content(self):
        pass

    @abstractmethod
    def img_process(self, img):
        pass

    @abstractmethod
    def video_process(self, video):
        pass

    @abstractmethod
    def url_process(self, url: str) -> (str, str):
        pass

    def save_resource(self, res) -> None:
        name, last = self.url_process(res['src'])
        rename = self.rename(name.encode())
        rename += '.' + last
        urllib.request.urlretrieve(name, rename)
        s3.upload_file(
            rename,
            bucket,
            'upload/' + rename,
            ExtraArgs={
                'ACL': 'public-read',
                'CacheControl': 'max-age=2592000',
            },
        )
        os.remove(rename)
        res['src'] = self.s3_domain + rename

        if 'height' in res.attrs:
            del res.attrs['height']
        if 'width' in res.attrs:
            del res.attrs['width']

    def rename(self, name: bytes):
        return hashlib.sha256(name).hexdigest()

    def run(self, page=0):
        self.page = page
        try:
            while True:
                self.load_page()
                page_contents = self.load_page_contents()
                if not page_contents:
                    print(f'{self} 완료')
                    return

                for url in page_contents:
                    self.load_content(url)
                    content = self.parse_content()
                    session = create_session()

                    if (
                        session.query(Article)
                        .filter(Article.title == content.title)
                        .first()
                    ):
                        continue

                    article = Article(
                        title=content.title,
                        body=content.text,
                        source=self.name,
                    )
                    session.add(article)
                    session.commit()
                    # time.sleep(random.random() * 3 + 4)
                print(f'{self.page}페이지 탐색 완료')
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            self.driver.quit()


@dataclass
class Item:
    title: str
    text: str
    created_at: datetime
