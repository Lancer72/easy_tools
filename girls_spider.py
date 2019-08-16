import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import os
import concurrent
import random
import time
import requests

# 代理池
PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

# 启动多线程时会有大量403

def header(referer):
    # 请求头
    headers={
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-encoding': 'gzip, deflate,',
        'Accept-language': 'zh-CN,zh;q=0.9',
        'Cache-control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers
def headers_2():
    headers=[
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    ]
    return random.choice(headers)
def request_page(url):
    try:
        response= requests.get(url,headers={'User-Agent':headers_2()},proxies={'proxy':get_proxy()})
        if response.status_code==200:
            return response.text
    except requests.RequestException:
        return None

def get_page_urls():
    # 获取每一页每组图片的链接
    for i in range(1,2):
        baseurl='https://www.mzitu.com/page/{}'.format(i)
        html=request_page(baseurl)
        soup=BeautifulSoup(html,'lxml')
        list=soup.find(class_='postlist').find_all('li')
        # 创建链接列表
        urls=[]
        for item in list:
            url=item.find('span').find('a').get('href')
            print('页面链接：%s' % url)
            urls.append(url)
    return urls

def download_pic(title,image_list):
    # 新建文件夹
    os.mkdir(title)
    j=1
    # 下载图片
    for item in image_list:
        filename='%s/%s%s.jpg' % (title,title,str(j))
        print('downloading...%s:(%s)' % (title,str(j)))
        with open(filename,'wb') as f:
            img=requests.get(item,headers=header(item)).content
            f.write(img)
        j+=1

def download(url):
    # 内页图片下载
    html=request_page(url)
    time.sleep(0.01)
    print(type(html))
    soup=BeautifulSoup(html,'lxml')
    total=soup.find(class_='pagenavi').find_all('a')[-2].find('span').string
    title=soup.find('h2').string
    img_list=[]
    # 获取内页每一页的图片地址
    for i in range(int(total)):
        html=request_page(url + '/%s' % (i + 1))
        print('获取内页每一页的图片地址:'+str(type(html))+url + '/%s' % (i + 1))
        soup=BeautifulSoup(html,'lxml')
        img_url=soup.find('img').get('src')
        img_list.append(img_url)
        # 减少访问频率
        time.sleep(0.01)

    download_pic(title,img_list)

def download_all_images(list_page_urls):
    # 多线程下载图片
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for url in list_page_urls:
            time.sleep(random.randint(1,3))
            executor.submit(download,url)

if __name__ == '__main__':
    list_page_urls=get_page_urls()
    download_all_images(list_page_urls)
    # for url in list_page_urls:
        # download(url)