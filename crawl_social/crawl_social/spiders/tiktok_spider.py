import csv
import scrapy


class TiktokSpiderSpider(scrapy.Spider):
    name = "tiktok_spider"
    allowed_domains = ["www.tiktok.com"]
    start_urls = ["https://www.tiktok.com/@quizneofficial"]

    def parse(self, response):
        followers = response.css('[data-e2e="followers-count"]::text').get()
        if followers:
            with open('output_tiktok.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['tiktok_value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Ghi header
                writer.writeheader()

                # Ghi dữ liệu
                writer.writerow({'tiktok_value': followers + ' followers'})

            self.log("Dữ liệu đã được lưu vào output_tiktok.csv")
        else:
            self.log("Không tìm thấy dữ liệu")

