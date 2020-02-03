import os
import ssl
import time
import urllib
from urllib.parse import parse_qs, urlparse
from urllib.request import urlretrieve
from uuid import uuid4
from _datetime import datetime

import requests
import urllib3
from bs4 import BeautifulSoup
from crawler import Crawler, Item
from time import sleep


class DCInsideHit(Crawler):

    session: requests.Session

    def __init__(self):
        super().__init__(
            base_url='https://gall.dcinside.com/board/lists/?id=hit&page={}',
            page=1,
            name='dc_hit',
        )

    def load_page(self):
        self.driver.get(self.base_url.format(self.page))
        self.page += 1

    def load_page_contents(self):
        resources = [
            a.get_attribute('href')
            for a in self.driver.find_elements_by_css_selector(
                'table.gall_list tbody tr.us-post td.gall_tit > a:not(.reply_numbox)'
            )
        ]

        return resources

    def url_process(self, url):
        parsed = urlparse(url)
        parsed = parsed._replace(netloc='image.dcinside.com')
        parsed = parsed._replace(path='/viewimagePop.php')

        image_url = parsed._replace(path='/viewimage.php')
        image = self.session.get(
            headers={'Referer': parsed.geturl()},
            url=image_url.geturl(),
            stream=True,
        )

        filename = str(uuid4())
        last = image.headers['Content-Disposition'].split('.')[-1]

        with open(f'./{filename}.{last}', 'wb') as f:
            f.write(image.content)
        return filename, last

    def save_resource(self, res) -> None:
        name, last = self.url_process(res['src'])
        rename = self.rename(name.encode())
        rename += '.' + last
        self.upload_s3(f'{name}.{last}', rename)
        os.remove(f'{name}.{last}')
        res['src'] = self.cloudfront_domain + rename

    def load_content(self, url):
        self.driver.get(url)

    def video_process(self, video):
        self.save_resource(video.find('source') or video)

    def img_process(self, img):
        self.save_resource(img)

    def parse_content(self):
        try:
            title = self.driver.find_element_by_css_selector(
                'span.title_subject'
            ).text
        except Exception as e:
            import pdb

            pdb.set_trace()
        body = BeautifulSoup(self.driver.page_source, 'html.parser')
        body = body.select('div.writing_view_box')[0]

        self.session = requests.session()

        try:
            self.body_process(body)
        except:
            return None
        for footer in body.select('span#dcappfooter'):
            footer.extract()

        body.select('a')[-1].extract()
        source = [a for a in body.strings if a.strip()][-1]
        self.session.close()
        body = str(body)
        body = body.replace(source, '')

        item = Item(title=title, text=body, created_at=datetime.now())
        self.driver.back()
        return item
