import csv
import scrapy
from scrapy_splash import SplashRequest

class GroupFbSpiderSpider(scrapy.Spider):
    name = "group_fb_spider"
    allowed_domains = ["www.facebook.com"]
    start_urls = ["https://www.facebook.com/groups/nghienquiz"]

    lua_script = '''
        function main(splash, args)
        local headers = {
            ["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        splash:set_custom_headers(headers)
        assert(splash:wait(1))
        assert(splash:go(args.url))
        assert(splash:wait(1))

        assert(splash:go("https://www.facebook.com/groups/nghienquiz"))
        assert(splash:wait(2))

        assert(splash:select("div[aria-label='Close']")):mouse_click()
        assert(splash:wait(2))

        members = splash:evaljs("document.evaluate('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/span/span/div/div[3]/a', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerText")
        print(members)
        
        return {
            html = splash:html(),
            png = splash:png(),
            har = splash:har(),
            members = members,
        }
    end
    '''
    
    def start_requests(self):
        url = "https://www.facebook.com/groups/nghienquiz"
        api_key = "ef4f21ff098e23556eb8e6e33e86710f"
        scraperapi_url = f"http://api.scraperapi.com?api_key={api_key}&url=http://httpbin.org/ip"

        yield SplashRequest(
            url=url,
            callback=self.parse,
            endpoint="execute",
            args={
                'lua_source': self.lua_script,
                # 'proxy': scraperapi_url,
            },
            splash_headers={'timeout': 180}
        )

    def parse(self, response):
        if 'members' in response.data:
            members_value = response.data['members']

            # Ghi vào file CSV
            with open('output_group.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['group_value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Ghi header
                writer.writeheader()

                # Ghi dữ liệu
                writer.writerow({'group_value': members_value})

            self.log("Dữ liệu đã được lưu vào output_group.csv")
        else:
            self.log("Không tìm thấy dữ liệu")
        yield {'data': 'data_from_second_spider'}