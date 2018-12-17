'''目地：爬取猫眼电影上的正在热映电影

   详情：本次爬取猫眼电影正在热映的电影，分两页共54部，每部电影爬取三项信息
   ['电影名','类型','上映时间']。运用了-requests- -lxml- -csv-
   不涉及反爬虫技术，简单获取页面的小项目

   收获：增强了自己对xpath的理解，加强了对代码的结构化的理解'''

import csv
from lxml import etree
import requests

# 初始url
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1)'
                  ' Gecko/20100101 Firefox/4.0.1'
}

# 获取url
def get_movie_detail_url(url, headers):
    #请求初始url并得到response对象
    req = requests.get(url, headers=headers)
    page = etree.HTML(req.text)
    hrefs = page.xpath('//dd/div[1]/a/@href')
    #定义一个空列表来存储返回值
    movie_urls = []
    for href in hrefs:
        #构造电影详情页url
        i = 'https://maoyan.com' + href
        #将构造好的url加到列表尾部
        movie_urls.append(i)
    # print(urls)
    return movie_urls

# 解析url并抓取数据
def get_movie_detail_data(movie_urls):
    for movie_url in movie_urls:
        #请求电影详情页面并接受到返回的response对象
        req = requests.get(movie_url, headers=headers)
        #将得到的页面对象转化成text格式，然后再构造成可以使用xpath的数据类型
        page = etree.HTML(req.text)
        #通过xpath取得需要的信息
        name = page.xpath('//div[@class="movie-brief-container"]/h3/text()')
        category = page.xpath('//div[@class="movie-brief-container"]/ul/li[1]/text()')
        start_time = page.xpath('//div[@class="movie-brief-container"]/ul/li[3]/text()')
        #构造一个迭代器
        yield {
            '电影名': name,
            '类型': category,
            '上映时间': start_time
        }

# 保存数据
def save_data(data):
    #以追加的方式一行一行的将得到的数据写入csv文件中
    with open('Hot_movie.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        writer.writerow(data)

# main方法
def main(start_url):
    x =  1
    #得到电影详情页面的url
    movie_urls = get_movie_detail_url(start_url, headers)
    #请求并拿到详情页面并拿到需要的信息
    for item in get_movie_detail_data(movie_urls):
        #保证item.keys()只存储一次
        if x == 1:
            save_data(item.keys())
            x = x - 1
        #存储详细信息
        save_data(item.values())
        print(item.values())

# 运行main方法
if __name__ == '__main__':
    #通过改变页面的offset来构造页面url作为初始url
    url = 'https://maoyan.com/films?showType=1&offset='
    for i in range(0, 31, 30):
        start_url = url + str(i)
        main(start_url)
