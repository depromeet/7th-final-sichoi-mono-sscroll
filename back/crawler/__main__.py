from selenium import webdriver

from crawler.daum import Daum
from crawler.dogdrip import Dogdrip
from crawler.humoruniv import HumorUniv

crawlers = [HumorUniv(), Dogdrip()]
# crawlers = [Daum()]


for crawler in crawlers:
    crawler.driver = webdriver.Chrome('chromedriver')
    crawler.run()
