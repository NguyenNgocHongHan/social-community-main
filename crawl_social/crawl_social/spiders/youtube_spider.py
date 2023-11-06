import csv
import scrapy
from scrapy_splash import SplashRequest

class YoutubeSpiderSpider(scrapy.Spider):
    name = 'youtube_spider'
    allowed_domains = ['www.youtube.com']
    start_urls = ['https://www.youtube.com/@QuizNeOfficial']

    def start_requests(self):
        start_urls = ["https://www.youtube.com/@QuizNeOfficial"]
        for url in start_urls:
            yield SplashRequest(
                url,
                self.parse,
                args={'wait': 2}
            )

    def parse(self, response):
        subscribers = response.css('[id="subscriber-count"]::text').get()
        if subscribers:
            with open('output_youtube.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['youtube_value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Ghi header
                writer.writeheader()

                # Ghi dữ liệu
                writer.writerow({'youtube_value': subscribers })

            self.log("Dữ liệu đã được lưu vào output_youtube.csv")
        else:
            self.log("Không tìm thấy dữ liệu")






