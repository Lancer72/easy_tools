from queue import Queue
from threading import Thread

import os
from time import time

import requests
from bs4 import BeautifulSoup


class DownloadBiaoqingbao(Thread):
    def __init__(self,queue,path):
        Thread.__init__(self)
        self.queue= queue
        self.path='home/biaoqingbao/'
        # 新建文件夹
        if not os.path.exists(path):
            os.makedirs(path)

    def run(self):
        while True:
            url=self.queue.get()
            try:
                # print(url)
                download_bqb(url,self.path)
            finally:
                self.queue.task_done()


def download_bqb(url,path):
    response= requests.get(url)
    # print(response.status_code)
    soup=BeautifulSoup(response.content,'lxml')
    # print(soup)
    img_list=soup.find_all('img',class_='ui image lazy')
    # print(img_list)
    for img in img_list:
        image=img.get('data-original')
        title=img.get('title')
        print('下载图片：%s' % title)

        try:
            with open(path+title+os.path.splitext(image)[-1],'wb') as f:
                img=requests.get(image).content
                f.write(img)
        except OSError:
            print('length failed')

if __name__ == '__main__':
    start=time()

    _url='https://fabiaoqing.com/biaoqing/lists/page/{page}.html'
    urls = [_url.format(page=page) for page in range(1, 200 + 1)]

    queue=Queue()
    path='home/biaoqingbao/'
    # 创建线程
    for x in range(10):
        worker=DownloadBiaoqingbao(queue,path)
        worker.daemon=True
        worker.start()
    # 加入队列
    for url in urls:
        queue.put(url)

    queue.join()
    print('下载完毕耗时:',time()-start,'s')