from selenium import webdriver

from crawler.dogdrip import Dogdrip
from crawler.humoruniv import HumorUniv

crawlers = [Dogdrip(), HumorUniv()]


for crawler in crawlers:
    crawler.driver = webdriver.Chrome('chromedriver')
    crawler.run()
