import os
import time
import urllib
from urllib.request import urlretrieve

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# 下载功能
def download_pics(image_src, i, title):
    dirPath = 'E:\papapa\ziman\ ' + title
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    filename = os.path.basename(str(i) + '.png')
    filepath = os.path.join(dirPath, filename)
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'Referer': 'https://global.toomics.com/sc/age_verification?cancel_return=L3Nj&return_url=L3NjL3dlYnRvb24vZGV0YWlsL2NvZGUvMTMwNjkzL2VwLzEvdG9vbi81Njc5'}
    request = urllib.request.Request(url=image_src, headers=headers)
    res = urllib.request.urlopen(request)
    # res.encoding = 'utf-8'
    with open(filepath, 'wb') as fp:
        fp.write(res.read())


urlCode = 130693
urlPage = 1
url = 'https://global.toomics.com/sc/webtoon/detail/code/' + str(urlCode) + '/ep/' + str(urlPage) + '/toon/5679'
# 打开浏览器
dri = webdriver.Chrome()
# 模拟浏览器请求网站
dri.get(url)
time.sleep(5)
# 跳过成人页面，注册之后是否去掉该步骤
dri.find_element(By.CLASS_NAME, 'button_yes').click()
time.sleep(5)
# 解析网页
htmlInfo = BeautifulSoup(dri.page_source, 'html.parser')
# 获取网页的title
title = htmlInfo.find('div', class_='viewer-title').get_text().strip()
# 获取网页上所有的图片
pics_info1 = htmlInfo.find_all('img', class_='img-responsive center-block lazy loaded')  # 已经加载的
pics_info2 = htmlInfo.find_all('img', class_='img-responsive center-block lazy')  # 未经加载的
pics_info = pics_info1 + pics_info2  # 图片连接拼合进一个list
print('开始下载')
# 根据List中的图片连接下载图片
for j in range(len(pics_info)):
    img_src = pics_info[j]['src']
    download_pics(img_src, j + 1, title)
    print('图片下载进度{0:.2%}'.format((j + 1)/len(pics_info)))
# 关闭浏览器
dri.quit()
