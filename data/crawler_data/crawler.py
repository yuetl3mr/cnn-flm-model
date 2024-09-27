from icrawler.builtin import GoogleImageCrawler

google_crawler = GoogleImageCrawler()
google_crawler.crawl(keyword='sunny', offset=0, max_num=1000,
                     date_min=None, date_max=None, feeder_thr_num=1,
                     parser_thr_num=1, downloader_thr_num=4,
                     min_size=(200,200), max_size=None)