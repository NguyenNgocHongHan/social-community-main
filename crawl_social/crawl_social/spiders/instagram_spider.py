import csv
import requests
from bs4 import BeautifulSoup


def scrapeInstagram(soup1):
    Data = [0]
    for meta in soup1.find_all (name="meta", attrs={"property" : "og:description" }):
        Data = meta["content"].split()

    follower = Data[0]
    if follower:
        with open('output_instagram.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['instagram_value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Ghi header
            writer.writeheader()

            # Ghi dữ liệu
            writer.writerow({'instagram_value': str(follower) + ' followers'})

        print("Dữ liệu đã được lưu vào output_instagram.csv")
    else:
        print("Không tìm thấy dữ liệu")

if __name__ == "__main__":
    #user=input("Write your name chanel: ")
    url="https://www.instagram.com/quizneofficial/" #+user
    page=requests.get(url)
    soup=BeautifulSoup(page.text, "html.parser")
    scrapeInstagram(soup)
