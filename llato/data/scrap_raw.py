from scrapy import Spider
from scrapy.crawler import CrawlerProcess
import scrapy
import logging
from scrapy.responsetypes import Response

class VocabularySpider(scrapy.Spider):
    name = "vocabulary"
    start_urls = [f"https://morfologija.lietuviuzodynas.lt/{letter}" for letter in "ABCDEFGHIJKLMNOPRSTUVZ"]

    def parse(self, response: Response):
        words = response.css("div#category-items > div.row > div.col-md-3 > a::text").extract()
        for word in words:
            yield {
                "word": word
            }

        next_page = response.css("ul.pagination > li.active + li > a::attr(href)").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

process = CrawlerProcess(settings={
    "FEEDS": {
        "raw.csv": {
            "format": "csv"
        }
    },
    "JOBDIR": "./job/vocabulary"
})

process.crawl(VocabularySpider)

def main():
    process.start()
    
if __name__ == "__main__":
    try:
        main()
    except:
        process.stop()
    finally:
        logging.fatal("Stopped!")