# 导入os库操作目录
import os
# 导入urllib库的urlopen
from urllib.request import urlopen
# 导入BeautifulSoup库用以解析html
from bs4 import BeautifulSoup as bf
# 导入urlretrieve库用以下载
from urllib.request import urlretrieve
# 请求获取html
html = urlopen("https://www.zhihu.com/question/20899988/answer/783269460")
# 用BeautifulSoup库解析html
obj = bf(html.read(), 'html.parser')
# 获取网址标题
title = obj.head.title
# 获取网址标题文本
title_text = title.get_text()
# 获取该网址所有图片
pics_info = obj.find_all('img', class_="origin_image zh-lightbox-thumb")
for j in range(len(pics_info)):
    pics_url = pics_info[j]['src']
    if not os.path.exists('E:\papapa\zhihu'):
        os.makedirs('E:\papapa\zhihu')
    urlretrieve(pics_url, 'E:\papapa\zhihu\ '+ str(title_text).rstrip('?') + str(j) + '.png')
    print('downloading')

