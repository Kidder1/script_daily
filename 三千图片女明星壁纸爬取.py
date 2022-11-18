import requests
from lxml import etree
import os
import time

# 创建文件夹
if not os.path.exists('./Pictures'):
    os.mkdir('./Pictures')
li_all = []
# 翻页爬取
for i in range(1, 6):
    # 爬取首页url
    url = 'https://www.win3000.com/tags/nmxtp/' + 'p' + str(i) + '/'
    # print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    page_text = requests.get(url=url, headers=headers).text
    # 实例化etree对象
    tree = etree.HTML(page_text)
    # 爬取首页所有人的链接
    li_list = tree.xpath('/html/body/div[1]/div[2]/ul[2]/li/a/@href')
    # print("The ", i, " is :")
    # 获取详情页每个人所有大图照片链接并且进行爬取
    # print(len(li_list))
    # 存储所有人的链接(100个)
    li_all += li_list

for li in li_all:
    # 建立对应明星的文件夹
    # 爬取文件夹的名称
    url = li
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    title = tree.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/h1/text()')
    dir_name = title[0]
    # 建立文件夹
    if not os.path.exists('./Pictures/' + dir_name):
        os.mkdir('./Pictures/' + dir_name)

    # 爬取照片并且进行持久化存储
    for i in range(1, 20):
        # print(str(li_all[0]).rstrip('.html'))
        picture_url = str(li).rstrip('.html') + '_' + str(i) + '.html'
        print(picture_url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }
        # 判断对应响应是否存在，处理异常
        picture_detail = requests.get(url=picture_url, headers=headers)
        if not picture_detail:
            # 不存在最后一个链接，结束此人的爬出，跳出内循环，进入外循环进行下一个人爬取
            print(dir_name, " is ok。")
            break
        else:
            # 存在爬取并且进行持久化存储
            # 获取图片链接
            picture_detail_text = requests.get(url=picture_url, headers=headers).text
            tree = etree.HTML(picture_detail_text)
            picture_detail_url = tree.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/p/img/@src')
            # 爬取照片
            photo = requests.get(url=picture_detail_url[0], headers=headers).content
            # 对照片进行持久化存储
            file_name = str(picture_detail_url[0]).split('/')[-1]
            with open('./Pictures/' + dir_name + '/' + file_name, 'wb') as fp:
                fp.write(photo)
            print(dir_name, "'s ", i, ' is ok.')
           # time.sleep(0.1)
print("Everything is ok!")
