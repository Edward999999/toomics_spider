# coding:utf-8
import os
import traceback
import urllib
from urllib.request import urlretrieve
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

dri = webdriver.Chrome()
dri.implicitly_wait(10)
dri.get('https://global.toomics.com')


# 登录comics
def loginToomics():
    dri.find_element(By.ID, 'toggle-login').click()
    dri.find_element(By.XPATH, "//div[@class='section_sns_sign_wrap01']/button").click()
    dri.find_element(By.ID, 'user_id').send_keys('fantimeng@gmail.com')
    dri.find_element(By.ID, 'user_pw').send_keys('ti199058')
    dri.find_element(By.XPATH, "//fieldset[@id='login_fieldset']/button").click()
    dri.find_element(By.CLASS_NAME, 'section_19plus').click()
    dri.find_element(By.LINK_TEXT, '分类').click()
    print('登录成功')


# 解析网站所有漫画栏目页面，获取漫画地址的href和标题
def parseWeb():
    htmlInfo = BeautifulSoup(dri.page_source, 'html.parser')  # 解析网站所有漫画页面
    comicsInfo = htmlInfo.select('#glo_wrapper > div > div > div > div > div > ul > li > div')  # 找到所有漫画信息
    allComicsHrefAndTitle = []
    for comicInfo in comicsInfo:
        comicsUrl = comicInfo.select('a')  # 从漫画信息里面获取网址标签
        comicsTitle = comicInfo.select('h4')  # 从漫画信息里面获取漫画名称标签
        for comicUrl in comicsUrl:
            Href = comicUrl.get('href')  # 从网址标签获取漫画可拼接地址
        for comicTitle in comicsTitle:
            Title = comicTitle.get_text()  # 从漫画信息里面获取漫画名称
        allComicsHrefAndTitle.append([Href, Title])  # 将地址和名称存入List列表
    print('获取漫画地址的href和标题成功')
    return allComicsHrefAndTitle


# 获取所有漫画目录地址href
def getInfoFromDetailPage(url):
    picPageUrls = []
    url = 'https://global.toomics.com' + url  # 拼接漫画目录网址
    dri.get(url)
    htmlInfo = BeautifulSoup(dri.page_source, 'html.parser')  # 解析漫画目录网址页面
    # picPageUrl = htmlInfo.select('#glo_wrapper > div > div > div > div > div > ul > li > div')
    pagesInfo = htmlInfo.find_all('li', class_='normal_ep')  # 获取所有目录信息
    for pageinfo in pagesInfo:
        pagesUrl = pageinfo.select('a')  # 获取目录信息中的网址标签
        for pageUrl in pagesUrl:
            pageHref = pageUrl.get('onclick')  # 获取标签中的onclick属性，因为漫画详情地址在这个属性里面
            picPageUrls.append(pageHref[35:-1])  # 处理该属性，使其变为可以拼接状态
    print('获取所有漫画目录地址href成功')
    return picPageUrls


# 获取所有漫画信息
def getPicsInfo(url, dire):
    url = 'https://global.toomics.com' + url
    # 模拟浏览器请求网站
    dri.get(url)
    # 跳过成人页面，注册之后是否去掉该步骤
    # dri.find_element(By.CLASS_NAME, 'button_yes').click()
    # 判断是否免费章节
    isFree = True
    try:
        dri.find_element(By.ID, 'charge_btn')
    except Exception:  # try捕获异常执行异常下面的操作,未发现充值按钮才能进行下载操作
        isFree = True
        print(traceback.print_exc())
        htmlInfo = BeautifulSoup(dri.page_source, 'html.parser')
        # 解析网页
        # 获取网页的title
        title = htmlInfo.find('div', class_='viewer-title').get_text().strip()
        # 获取网页上所有的图片
        pics_info1 = htmlInfo.find_all('img', class_='img-responsive center-block lazy loaded')  # 已经加载的
        pics_info2 = htmlInfo.find_all('img', class_='img-responsive center-block lazy')  # 未经加载的
        pics_info = pics_info1 + pics_info2  # 图片连接拼合进一个list
        # 根据List中的图片连接下载图片
        for j in range(len(pics_info)):
            img_src = pics_info[j]['src']
            isDownloaded = download_pics(img_src, j + 1, dire, title)
            print('{0}下载进度{1:.2%}'.format(title, (j + 1) / len(pics_info)))
            if isDownloaded is True:
                continue
    else:  # try未捕获异常进入else
        isFree = False
    finally:
        return isFree


# 下载功能
def download_pics(image_src, i, dire, title):
    dirPath = 'D:\spider\ziman\ ' + dire + '\\' + title  # 拼接文件目录路径
    if not os.path.exists(dirPath):  # 如果不存在创建该路径
        os.makedirs(dirPath)  # 创建多层目录makedirs（），创建单层目录mkdir（）
    filename = os.path.basename(str(i) + '.png')
    filepath = os.path.join(dirPath, filename)  # 拼接文件存储路径
    isDownloaded = False  # 新增是否已经下载过变量，没有下载过继续下载，下载过不再下载
    if not os.path.exists(filepath):  # 判断该文件是否已存在
        isDownloaded = False
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Referer': 'https://global.toomics.com/sc/age_verification?cancel_return=L3Nj&return_url=L3NjL3dlYnRvb24vZGV0YWlsL2NvZGUvMTMwNjkzL2VwLzEvdG9vbi81Njc5'}
        request = urllib.request.Request(url=image_src, headers=headers)  # 对该图片发起请求
        res = urllib.request.urlopen(request)  # 打开图片
        # res.encoding = 'utf-8'
        with open(filepath, 'wb') as fp:
            fp.write(res.read())  # 存储图片
        return isDownloaded

    else:
        isDownloaded = True
        print('{0}文件已存在'.format(filepath))
        return isDownloaded








