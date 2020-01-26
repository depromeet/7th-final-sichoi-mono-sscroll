import os
import time
from _datetime import datetime

from bs4 import BeautifulSoup
from crawler import Crawler, Item


class DCInsideHit(Crawler):
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
        return [
            a.get_attribute('href')
            for a in self.driver.find_elements_by_css_selector(
                'table.gall_list tbody tr.us-post td.gall_tit > a'
            )
        ]

    def url_process(self, url):
        import pdb

        pdb.set_trace()
        return None

    def load_content(self, url):
        self.driver.get(url)

    def video_process(self, video):
        import pdb

        pdb.set_trace()
        print('what')

    def img_process(self, img):
        self.save_resource(img)

    def img_filename(self) -> str:
        files = filter(os.path.isfile, os.listdir(os.getcwd()))
        files = filter(lambda x: x != '.DS_Store', os.listdir(os.getcwd()))
        files = [
            os.path.join(os.getcwd(), f) for f in files
        ]  # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x))
        return files[-1]

    def save_resource(self, res):
        self.driver.execute_script(f'window.open("{res["src"]}", "_blank")')
        time.sleep(0.5)
        filename = self.img_filename()
        name, last = filename.split('.')
        rename = self.rename(name.encode())
        rename += '.' + last
        self.upload_s3(filename, rename)
        os.remove(filename)
        res['src'] = self.s3_domain + rename

    def parse_content(self):
        title = self.driver.find_element_by_css_selector(
            'span.title_subject'
        ).text
        body = BeautifulSoup(self.driver.page_source, 'html.parser')
        body = body.select('div.writing_view_box')[0]

        self.body_process(body)
        body = str(body)

        item = Item(title=title, text=body, created_at=datetime.now())
        self.driver.back()
        return item
