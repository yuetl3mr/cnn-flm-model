from icrawler.builtin import GoogleImageCrawler

google_crawler = GoogleImageCrawler()
google_crawler.crawl(keyword='Paralyzed person face', offset=0, max_num=100,
                    min_size=(200,200), max_size=None)