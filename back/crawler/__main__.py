from crawler.dc_hit import DCInsideHit
from crawler.dogdrip import Dogdrip
from crawler.humoruniv import HumorUniv
import traceback

crawlers = [DCInsideHit(), HumorUniv(), Dogdrip()]
# crawlers = [HumorUniv(), Dogdrip()]


for crawler in crawlers:
    try:
        crawler.run()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
        crawler.driver.quit()
        print(f'{crawler.name} 종료')
