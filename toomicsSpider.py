# coding:utf-8
import os
import threading
import traceback
import urllib
from urllib.request import urlretrieve
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
# 命名规则
# 模块尽量使用小写命名，首字母保持小写，尽量不要用下划线(除非多个单词，且数量不多的情况)
# 类名使用驼峰(CamelCase)命名风格，首字母大写，私有类可用一个下划线开头
# 函数名一律小写，如有多个单词，用下划线隔开
# 私有函数在函数前加一个下划线_
# 变量名尽量小写, 如有多个单词，用下划线隔
# 常量采用全大写，如有多个单词，使用下划线隔开
dri = webdriver.Chrome()
dri.implicitly_wait(1)
dri.get('https://global.toomics.com')


# 登录comics
def login_toomics():
    dri.find_element(By.ID, 'toggle-login').click()
    dri.find_element(By.XPATH, "//div[@class='section_sns_sign_wrap01']/button").click()
    dri.find_element(By.ID, 'user_id').send_keys('你自己的账号')
    dri.find_element(By.ID, 'user_pw').send_keys('你自己的密码')
    dri.find_element(By.XPATH, "//fieldset[@id='login_fieldset']/button").click()
    dri.find_element(By.CLASS_NAME, 'section_19plus').click()
    print('登录成功')
    dri.find_element(By.LINK_TEXT, '分类').click()
    print('打开分类菜单成功')


# 解析网站所有漫画栏目页面，获取漫画地址的href和标题
def parse_web():
    html_info = BeautifulSoup(dri.page_source, 'html.parser')  # 解析网站所有漫画页面
    comics_info = html_info.select('#glo_wrapper > div > div > div > div > div > ul > li > div')  # 找到所有漫画信息
    all_comics_href_and_title = []  # 定义一个列表存放漫画名称和href
    for comic_info in comics_info:
        comics_url = comic_info.select('a')  # 从漫画信息里面获取网址标签
        comics_title = comic_info.select('h4')  # 从漫画信息里面获取漫画名称标签
        for comic_url in comics_url:
            href = comic_url.get('href')  # 从网址标签获取漫画可拼接地址
        for comic_title in comics_title:
            title = comic_title.get_text()  # 从漫画信息里面获取漫画名称
        all_comics_href_and_title.append([href, title])  # 将地址和名称存入List列表
    print('获取漫画地址的href和标题成功')
    return all_comics_href_and_title


# 获取所有漫画目录地址href
def get_info_from_detail_page(url):
    pic_page_urls = []
    url = 'https://global.toomics.com' + url  # 拼接漫画目录页面网址
    dri.get(url)
    html_info = BeautifulSoup(dri.page_source, 'html.parser')  # 解析漫画目录网址页面
    # picPageUrl = htmlInfo.select('#glo_wrapper > div > div > div > div > div > ul > li > div')
    pages_info = html_info.find_all('li', class_='normal_ep')  # 获取所有目录信息
    for pageinfo in pages_info:
        pages_url = pageinfo.select('a')  # 获取目录信息中的网址标签
        for page_url in pages_url:
            page_href = page_url.get('onclick')  # 获取标签中的onclick属性，因为漫画详情地址在这个属性里面
            pic_page_urls.append(page_href[35:-1])  # 处理该属性，使其变为可以拼接状态
    print('获取所有漫画目录地址href成功')
    return pic_page_urls


# 获取所有漫画信息
def get_pics_info(url, dire):
    url = 'https://global.toomics.com' + url
    # 模拟浏览器请求网站
    dri.get(url)
    # 跳过成人页面，注册之后是否去掉该步骤
    # dri.find_element(By.CLASS_NAME, 'button_yes').click()
    # 判断是否免费章节
    is_free = True
    try:
        dri.find_element(By.ID, 'charge_btn')
    except Exception:  # try捕获异常执行异常下面的操作,未发现充值按钮才能进行下载操作
        is_free = True
        # print(traceback.print_exc())
        html_info = BeautifulSoup(dri.page_source, 'html.parser')
        # 解析网页
        # 获取网页的title
        title = html_info.find('div', class_='viewer-title').get_text().strip()
        # 获取网页上所有的图片
        pics_info1 = html_info.find_all('img', class_='img-responsive center-block lazy loaded')  # 已经加载的
        pics_info2 = html_info.find_all('img', class_='img-responsive center-block lazy')  # 未经加载的
        pics_info = pics_info1 + pics_info2  # 图片连接拼合进一个list
        # 创建下载目录
        dir_path = 'D:\spider\ziman\ ' + dire + '\\' + title  # 拼接文件目录路径
        if not os.path.exists(dir_path):  # 如果不存在创建该路径
            os.makedirs(dir_path)  # 创建多层目录makedirs（），创建单层目录mkdir（）
        new_pics_info = segmentation_list(pics_info, 10)  # 把图片截取成，每10个为一个小列表
        threads = []
        for i in range(len(new_pics_info)):
            # 方法只传方法名，参数里面传递参数
            thread = threading.Thread(target=download_pics, args=(new_pics_info[i], 10 * i, dir_path, title))
            threads.append(thread)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    else:  # try未捕获异常进入else
        is_free = False
    finally:
        return is_free


# 把列表分割为n份，并返回分割后的列表组合的新列表
def segmentation_list(be_list, n):
    af_list = []
    for i in range(0, len(be_list), n):
        temp = be_list[i:i + n]
        af_list.append(temp)
    return af_list


# 判断是否已下载
def is_down(filepath):
    if not os.path.exists(filepath):  # 判断该文件是否已存在
        is_downloaded = False
    else:
        is_downloaded = True
    return is_downloaded


# 拼接下载路径
def down_path(p, dir_path):
    filename = os.path.basename(str(p) + '.png')
    filepath = os.path.join(dir_path, filename)  # 拼接文件存储路径
    return filepath


# 下载功能
def download_pics(pics_info, i, dir_path, title):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'Referer': 'https://global.toomics.com/sc/age_verification?cancel_return=L3Nj&return_url=L3NjL3dlYnRvb24vZGV0YWlsL2NvZGUvMTMwNjkzL2VwLzEvdG9vbi81Njc5'}
    # 根据List中的图片连接下载图片
    for j in range(len(pics_info)):
        img_src = pics_info[j]['src']
        p = j + 1 + i   # 第几张图片
        filepath = down_path(p, dir_path)
        if is_down(filepath) is False:
            request = urllib.request.Request(url=img_src, headers=headers)  # 对该图片发起请求
            res = urllib.request.urlopen(request)  # 打开图片
            with open(filepath, 'wb') as fp:
                fp.write(res.read())  # 存储图片
            print('{0}正在下载第{1}P'.format(title, p))
        else:
            print('{0}第{1}P已下载'.format(title, p))
            continue












