from crawler.dogdrip import Dogdrip
from crawler.humoruniv import HumorUniv
from selenium import webdriver

crawlers = [HumorUniv(), Dogdrip()]
# crawlers = [Daum()]


for crawler in crawlers:
    crawler.run()
