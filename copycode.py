# 导入os库操作目录
import os
import time
import urllib.request
import urllib.parse
from lxml import etree
# 导入urllib库的urlopen
from urllib.request import urlopen
# 导入BeautifulSoup库用以解析html
from bs4 import BeautifulSoup as bf
# 导入urlretrieve库用以下载
from urllib.request import urlretrieve

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

url = 'https://global.toomics.com/sc/webtoon/detail/code/130693/ep/1/toon/5679'


def handle_request(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    request = urllib.request.Request(url=url, headers=headers)
    return request


def download_iamge(image_src, i):
    dirpath = 'E:\papapa\ziman'
    print('正在下载第' + str(i) + '张图片')
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    filename = os.path.basename(str(i) + '.png')
    filepath = os.path.join(dirpath, filename)
    print(filepath)
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    request = urllib.request.Request(url=image_src, headers=headers)
    respons = urllib.request.urlopen(request)
    # respons.encoding = 'utf-8'
    with open(filepath, 'wb') as fp:
        fp.write(respons.read())


def parse_content(content):
    tree = etree.HTML(content)
    print(tree)
    # image_list = tree.xpath('//div[@id="wrapper-blank"]/div/main/div/div/img/src')
    image_list = tree.xpath('//div[@id="wrapper-blank"]/div/main/div/div/img/src')
    print(image_list)
    i = 1
    for image_sre in image_list:
        i += 1
        download_iamge(image_sre, i)


def main():
    url = 'https://global.toomics.com/sc/webtoon/detail/code/130693/ep/1/toon/5679'
    request = handle_request(url)
    content = urllib.request.urlopen(request).read().decode()
    parse_content(content)
    time.sleep(2)
    print('下载完成')


if __name__ == "__main__":
    main()
