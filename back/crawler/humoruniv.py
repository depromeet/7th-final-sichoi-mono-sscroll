import hashlib
import os
import urllib

import boto3
from bs4 import BeautifulSoup, element

from _datetime import datetime
from app.config import Config
from crawler import Crawler, Item


class HumorUniv(Crawler):
    def __init__(self):
        super().__init__(
            base_url='http://web.humoruniv.com/board/humor/list.html?table=pick&pg={}',
            page=0,
            name='humoruniv',
        )

    def load_page(self):
        self.driver.get(self.base_url.format(self.page))
        self.page += 1

    def load_page_contents(self):
        return [
            a.get_attribute('href')
            for a in self.driver.find_elements_by_css_selector(
                'div#cnts_list_new > div > table td > div > a'
            )
        ]

    def load_content(self, url):
        self.driver.get(url)
        select = self.driver.find_elements_by_css_selector(
            'wrap_copy a[href^="javascript"]'
        )

        for s in select:
            s.click()
            print('clicked')

    def parse_content(self):

        title = self.driver.find_element_by_css_selector(
            'span#ai_cm_title'
        ).text
        body = BeautifulSoup(self.driver.page_source, 'html.parser')
        body = body.select('wrap_copy')[0]
        body.name = 'div'

        [self.img_process(img) for img in body.findAll('img')]
        [self.video_process(video) for video in body.findAll('video')]

        body = str(body)

        item = Item(title=title, text=body, created_at=datetime.now())
        print(f'created {item.title}')
        self.driver.back()
        return item

    def url_process(self, url) -> (str, str):
        name = url
        if url.startswith('http://t.huv.kr/thumb_crop_resize.php?url='):
            name = url.split('?')[1].split('=')[1]

        return name, name.split('.')[-1]

    def video_process(self, video):
        self.save_resource(video.find('source') or video)

    def img_process(self, img):
        if '/images/' in img['src']:
            return

        self.save_resource(img)
        if img.parent.name == 'a':
            img.parent['href'] = img['src']
