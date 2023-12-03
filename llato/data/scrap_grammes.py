from scrapy import Spider
from scrapy.crawler import CrawlerProcess
import scrapy
import logging


class GramemasSpider(Spider):
    name = "gramemas"

    def start_requests(self):
        with open("raw.csv") as f:
            for word in f:
                yield scrapy.Request(url=f"https://morfologija.lietuviuzodynas.lt/zodzio-formos/{word}", callback=self.parse)

    def parse(self, response: scrapy.http.Response):
        word = response.url.split("/")[-1]
        gramemas = response.css("div.gramemas > *::text").extract()
        yield {
            "word": word,
            "gramemas": gramemas
        }

process = CrawlerProcess(settings={
    "FEEDS": {
        "gramemas.csv": {
            "format": "csv"
        }
    },
    "JOBDIR": "./job/gramemas"
})

process.crawl(GramemasSpider)


def main():
    process.start()


if __name__ == "__main__":
    try:
        main()
    except:
        process.stop()
    finally:
        logging.fatal("Stopped!")
