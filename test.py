# 导入时间库
import time
# 导入bs4.BeautifulSoup
from bs4 import BeautifulSoup
# 导入selenium.webdriver
from selenium import webdriver
# 导入By
from selenium.webdriver.common.by import By
dri = webdriver.Chrome()
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
    time.sleep(10)


def parseWeb():
    htmlInfo = BeautifulSoup(dri.page_source, 'html.parser')
    # 获取网页的所有漫画信息
    comicsInfo = htmlInfo.select('#glo_wrapper > div > div > div > div > div > ul > li > div')
    allComicsUrl = {}
    #urlHref = []
    #Title = []
    for comicInfo in comicsInfo:
        comicsUrl = comicInfo.select('a')
        comicsTitle = comicInfo.select('h4')
        for comicUrl in comicsUrl:
            urlHref = comicUrl.get('href')
        for comicTitle in comicsTitle:
            Title = comicTitle.get_text()
        allComicsUrl[urlHref] = Title
    print(allComicsUrl)
    # 获取网页上所有的图片
    # pics_info1 = htmlInfo.find_all('img', class_='img-responsive center-block lazy loaded')  # 已经加载的
    # pics_info2 = htmlInfo.find_all('img', class_='img-responsive center-block lazy')  # 未经加载的


loginToomics()
parseWeb()
