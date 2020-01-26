from crawler.dc_hit import DCInsideHit
from crawler.dogdrip import Dogdrip
from crawler.humoruniv import HumorUniv
from selenium import webdriver

crawlers = [DCInsideHit(), HumorUniv(), Dogdrip()]
# crawlers = [HumorUniv(), Dogdrip()]


for crawler in crawlers:
    crawler.run()
