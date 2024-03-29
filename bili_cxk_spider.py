import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser=webdriver.Chrome()
WAIT=WebDriverWait(browser,10)
book= xlwt.Workbook(encoding='utf-8',style_compression=0)
# 新建工作表
sheet=book.add_sheet('唱跳Rap篮球',cell_overwrite_ok=True)
sheet.write(0,0,'名称')
sheet.write(0,1,'地址')
sheet.write(0,2,'描述')
sheet.write(0,3,'观看次数')
sheet.write(0,4,'弹幕数')
sheet.write(0,5,'发布时间')
n=1

def search():
    try:
        print('访问bilibili')
        browser.get('https://www.bilibili.com/')
        # 通过刷新取消登录框
        index = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#app > div.bili-header-m.report-wrap-module > div.nav-menu > div.nav-wrapper.clearfix.bili-wrapper > div.nav-con.fl > ul > li.nav-item.home > a')))
        index.click()
        # 找到输入框
        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#banner_link>div>div>form>input')))
        # 找到提交按钮
        submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="banner_link"]/div/div/form/button')))
        input.send_keys('蔡徐坤 篮球')
        submit.click()
        print('跳转窗口')
        all_h = browser.window_handles
        browser.switch_to.window(all_h[1])
        get_source()
        # 找到页数
        total = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#server-search-app > div.contain > div.body-contain > div > div.page-wrap > div > ul > li.page-item.last > button')))
        return int(total.text)
    except TimeoutException:
        return search()

def next_page(page_num):
    try:
        print('获取下一页数据')
        next_btn=WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#server-search-app > div.contain > div.body-contain > div > div.page-wrap > div > ul > li.page-item.next > button')))
        next_btn.click()
        WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#server-search-app > div.contain > div.body-contain > div > div.page-wrap > div > ul > li.page-item.active > button'),str(page_num)))
        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)

def save_to_excel(soup):
    list=soup.find(class_='all-contain').find_all(class_='info')
    # 获取视频的标题、链接、简介、观看数、弹幕数、上传时间
    for item in list:
        item_title=item.find('a').get('title')
        item_link=item.find('a').get('href')
        item_dec=item.find(class_='des hide').text
        item_view=item.find(class_='so-icon watch-num').text
        item_biubiu=item.find(class_='so-icon hide').text
        item_date=item.find(class_='so-icon time').text

        print('爬取:'+item_title)

        global n
        #在表单中写入数据
        sheet.write(n,0,item_title)
        sheet.write(n,1,item_link)
        sheet.write(n,2,item_dec)
        sheet.write(n,3,item_view)
        sheet.write(n,4,item_biubiu)
        sheet.write(n,5,item_date)

        n=n+1

def get_source():
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#server-search-app > div.contain > div.body-contain > div > div.result-wrap.clearfix')))
    html=browser.page_source
    soup=BeautifulSoup(html,'lxml')
    save_to_excel(soup)

def main():
    try:
        total=search()
        print(total)

        for i in range(2,int(total+1)):
            next_page(i)
    finally:
        browser.close()

if __name__ == '__main__':
    main()
    book.save('唱跳Rap篮球.xls')