# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 20:02:17 2019

@author: Caiyunbin
"""

import requests
from bs4 import BeautifulSoup
import pymysql
 
#获取网页的源代码
def get_html(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    res = requests.get(url,headers = headers)
    return res.text
 
#解析网页，返回字典
def parse_html(html):#这里返回字典的生成器
    soup = BeautifulSoup(html,'lxml')
    items = soup.find_all('dd')
    for item in items:
        yield {
            'inde':item.select('.board-index')[0].get_text(),
            'img':item.select('.board-img')[0]['data-src'],
            'name':item.select('.name a')[0].get_text(),
            'star':item.select('.star')[0].get_text().strip(),
            'time':item.select('.releasetime')[0].get_text(),
            'score':item.select('.integer')[0].get_text()+item.select('.fraction')[0].get_text()
            }
            
#保存到mysql，字段的数据类型直接在mysql中已经设置      
def save_mysql(dicts):
    db = pymysql.connect("localhost", "root", "caiyunbin3344", "maoyanmovies",charset="gb18030")
    cursor = db.cursor()
    sql = "insert into maoyan values('{}',{},'{}','{}',{},'{}')".format(dicts['name'],dicts['inde'],dicts['star'],dicts['img'],dicts['score'],dicts['time'])
    cursor.execute(sql)
    db.commit()
    

def main():
    for i in range(10):
        url = 'http://maoyan.com/board/4?offset='+str(i*10)
        html = get_html(url)
        for item in parse_html(html):
            save_mysql(item)#save_mysql(item)#保存文本或mysql#save_mongodb(item)
    #save_csv()#保存为csv
         
if __name__ == '__main__':
    main()












