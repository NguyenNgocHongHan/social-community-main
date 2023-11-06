import csv
import scrapy
from scrapy_splash import SplashRequest

class FanpageFbSpiderSpider(scrapy.Spider):
    name = 'fanpage_fb_spider'
    allowed_domains = ["www.facebook.com"]
    start_urls = ["https://www.facebook.com/quizne"]

    lua_script = '''
        function main(splash, args)
        local headers = {
            ["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        splash:set_custom_headers(headers)
        assert(splash:wait(1))
        assert(splash:go(args.url))
        assert(splash:wait(1))

        assert(splash:go("https://www.facebook.com/quizne"))
        assert(splash:wait(2))

        assert(splash:select("div[aria-label='Close']")):mouse_click()
        assert(splash:wait(2))

        followers = splash:evaljs("document.evaluate('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerText")
        print(followers)
        return {
            html = splash:html(),
            png = splash:png(),
            har = splash:har(),
            followers = followers,
        }
        end
    '''
    def start_requests(self):
        url = "https://www.facebook.com"
        yield SplashRequest(url=url, callback=self.parse, endpoint="execute", args={
            'lua_source': self.lua_script
        })

    def parse(self, response):
        if ('followers') in response.data:
            followers_value = response.data['followers']

            # Ghi vào file CSV
            with open('output_fanpage.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['fanpage_data']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Ghi header
                writer.writeheader()

                # Ghi dữ liệu
                writer.writerow({'fanpage_data': followers_value})

            self.log("Dữ liệu đã được lưu vào output_fanpage.csv")
        else:
            self.log("Không tìm thấy dữ liệu")

