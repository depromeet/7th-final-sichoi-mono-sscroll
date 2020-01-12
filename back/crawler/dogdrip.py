import hashlib
import os
import urllib
from _datetime import datetime

import boto3
from bs4 import BeautifulSoup, element

from app.config import Config
from crawler import Crawler, Item


class Dogdrip(Crawler):
    def __init__(self):
        super().__init__(
            base_url='https://www.dogdrip.net/index.php?mid=dogdrip&sort_index=popular&page={}',
            page=1,
            name='dogdrip',
        )

    def load_page(self):
        self.driver.get(self.base_url.format(self.page))
        self.page += 1

    def load_page_contents(self):
        return [
            a.get_attribute('href')
            for a in self.driver.find_elements_by_css_selector(
                '.ed.table.table-divider tbody td.title > a'
            )
        ]

    def load_content(self, url):
        self.driver.get(url)

    def url_process(self, url) -> (str, str):
        name = url
        if './' in url:
            name = url.replace('./', 'http://www.dogdrip.net/')
        elif url.startswith('/'):
            name = 'https://www.dogdrip.net' + url
        elif not url.startswith('http'):
            name = 'https://www.dogdrip.net/' + url

        return name, name.split('.')[-1]

    def video_process(self, video):
        self.save_resource(video.find('source') or video)

    def img_process(self, img):
        self.save_resource(img)

        if img.parent.name == 'a':
            img.parent['href'] = img['src']

    def parse_content(self):
        title = self.driver.find_elements_by_css_selector(
            '.ed.link.text-bold'
        )[0].text
        body = BeautifulSoup(self.driver.page_source, 'html.parser')
        body = body.select('#article_1 > div')[0]
        body.select('.wgtRv')[0].clear()

        self.body_process(body)
        body = str(body)

        item = Item(title=title, text=body, created_at=datetime.now())
        print(f'created {item.title}')
        self.driver.back()
        return item
