import json

import requests
import re

def request_dandan(url):
    try:
        response= requests.get(url)
        if response.status_code==200:
            return response.text
    except requests.RequestException:
        return None

def parse_result(html):
    pattern=re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            '排位':item[0],
            '书名': item[2],
            '作者':item[4],
            '推荐度': item[3],
            '五星评分':item[5],
            '价格':"¥"+item[6],
            '封面': item[1]
        }

def write_item_to_file(item):
    print('开始写入数据===>'+str(item))
    with open('book.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')
        f.close()

def main(page):
    url='http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    html=request_dandan(url)
    items=parse_result(html)
    for item in items:
        write_item_to_file(item)

if __name__ == '__main__':
    for i in range(1,26):
        main(i)