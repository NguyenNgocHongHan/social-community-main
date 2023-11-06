
import csv
import datetime
import pandas as pd
from flask import Flask, render_template
from concurrent.futures import ThreadPoolExecutor
import subprocess

app = Flask(__name__)
executor = ThreadPoolExecutor()

def run_spiders():
    subprocess.run(['scrapy', 'crawl', 'group_fb_spider'])
    subprocess.run(['scrapy', 'crawl', 'fanpage_fb_spider'])
    subprocess.run(['scrapy', 'crawl', 'youtube_spider'])
    subprocess.run(['scrapy', 'crawl', 'tiktok_spider'])
    file_python1 = 'spiders\instagram_spider.py'
    subprocess.run(['python', file_python1])

def read_csv():
    data = []
    with open('output.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

@app.route('/')
def index():
    data = get_follower_group()
    return render_template('index.html', data=data)

@app.route('/get_follower', methods=['GET'])
def get_follower_group():
    executor.submit(run_spiders).result()
    group_data = pd.read_csv('output_group.csv')
    fanpage_data = pd.read_csv('output_fanpage.csv')
    youtube_data = pd.read_csv('output_youtube.csv')
    instagram_data = pd.read_csv('output_instagram.csv')
    tiktok_data = pd.read_csv('output_tiktok.csv')

    split_group = str(group_data).split()
    split_fanpage = str(fanpage_data).split()
    split_youtube = str(youtube_data).split()
    split_instagram = str(instagram_data).split()
    split_tiktok = str(tiktok_data).split()

    number_follower_group = split_group[2]
    number_follower_fanpage = split_fanpage[2]
    number_follower_youtube = split_youtube[2]
    number_follower_instagram = split_instagram[2]
    number_follower_tiktok = split_tiktok[2]

    #lấy thời gian hiện tại
    end_time = datetime.datetime.now()
    with open('output_time.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['time_value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Ghi header
                writer.writeheader()

                # Ghi dữ liệu
                writer.writerow({'time_value': end_time})

    #tổng lượt follower
    total_follower_social = int(number_follower_fanpage)  + int(number_follower_tiktok) + int(number_follower_youtube) + int(number_follower_instagram) + int(number_follower_group)
    with open('output_total.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['total_value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Ghi header
        writer.writeheader()

        # Ghi dữ liệu
        writer.writerow({'total_value': str(total_follower_social) + ' followers'})

    #phần trăm kpi đạt đượt
    percent_kpi = float(total_follower_social*100 / 50000)
    with open('output_percent.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['percent_value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Ghi header
                writer.writeheader()

                # Ghi dữ liệu
                writer.writerow({'percent_value': str(percent_kpi) + ' (%)'})

    # Kiểm tra xem file đã tồn tại chưa
    content = [end_time, percent_kpi, total_follower_social, number_follower_group, number_follower_fanpage, number_follower_tiktok, number_follower_youtube, number_follower_instagram]
    
    with open('output.csv', mode='a', newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(content)

    history = read_csv()
    return {'time': end_time,
            'group': number_follower_group,
            'fanpage': number_follower_fanpage,
            'youtube': number_follower_youtube,
            'tiktok': number_follower_tiktok,
            'instagram': number_follower_instagram,
            'total': total_follower_social,
            'percent': percent_kpi,
            'history': history}

if __name__ == '__main__':
    app.run(debug=True)

