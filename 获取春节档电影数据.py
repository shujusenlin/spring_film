# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 07:08:48 2019

@author: Administrator
"""

import json
import random
import requests
import time
import pandas as pd
import os
import numpy as np
from pyecharts import Bar,Geo,Line,Overlap
import jieba
from scipy.misc import imread  # 这是一个处理图像的函数
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from collections import Counter
from bs4 import BeautifulSoup  
from pyecharts import Bar,Line,Overlap
from selenium import webdriver 
os.chdir('D:/爬虫/春节档')

## 设置headers和cookie
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32; rv:54.0) Gecko/20100101 Firefox/54.0',
'Connection': 'keep-alive'}
cookies ='v=3; iuuid=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; webp=true; ci=1%2C%E5%8C%97%E4%BA%AC; __guid=26581345.3954606544145667000.1530879049181.8303; _lxsdk_cuid=1646f808301c8-0a4e19f5421593-5d4e211f-100200-1646f808302c8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; monitor_count=1; _lxsdk_s=16472ee89ec-de2-f91-ed0%7C%7C5; __mta=189118996.1530879050545.1530936763555.1530937843742.18'
cookie = {}
for line in cookies.split(';'):
    name, value = cookies.strip().split('=', 1)
    cookie[name] = value

## 爬取数据，每次理论上可以爬取1.5W调数据，存在大量重复数据，需要多次执行，最后统一去重

def get_all_comment(name,id):
    this_comments=pd.DataFrame(columns=['name','date','score','city','comment','nick','gender'])
    for i in range(0, 1000):
        j = i
        print(str(i)+' '+str(j))
        try:
            url= 'http://m.maoyan.com/mmdb/comments/movie/'+str(id)+'.json?_v_=yes&offset=' + str(j)
            html = requests.get(url=url, cookies=cookie, headers=header).content
            data = json.loads(html.decode('utf-8'))['cmts']
            for item in data:
                try:
                    this_gender = item['gender']
                except:
                    this_gender = 'unknown'
                this_comments = this_comments.append({'name':name,'date':item['time'].split(' ')[0],'city':item['cityName'],
                                        'score':item['score'],'comment':item['content'],
                                        'nick':item['nick'],'gender':this_gender},ignore_index=True)                                     
        except:
            continue
    return this_comments
    
spring = pd.read_excel('电影清单.xlsx')
comments = pd.DataFrame(columns=['name','date','score','city','comment','nick','gender'])
for k in range(spring.shape[0]):
    this_comments = get_all_comment(spring['name'][k],spring['maoyan_id'][k])
    comments = comments.append(this_comments,ignore_index=True)

comments_all = comments.drop_duplicates()  

## 计算电影评论分数和提取关键字 

def valid_mean(df):
    return np.mean([k for k in df if k>0])

def key_words(df):
    comment_str =  ' '.join(df)
    words_list = []
    jieba.load_userdict('spring_film_dict.txt')
    word_generator = jieba.cut(comment_str)  # 返回的是一个迭代        f.close()  # stopwords文本中词的格式是'一词一行'
    for word in word_generator:
        words_list.append(word)
    words_list = Counter([k for k in words_list if len(k)>1])
    return list(dict(words_list.most_common(30)).keys())

film_stat = comments_all.groupby('name').agg({'score':valid_mean,'comment':key_words}).reset_index()
film_stat.columns = ['name','score','key_words']


## 获取预售票房
driver = webdriver.Chrome()
driver.maximize_window()    
driver.close() 
driver.switch_to_window(driver.window_handles[0])  
url = 'https://piaofang.maoyan.com/dashboard?date=2019-02-05'
js='window.open("'+url+'")'
driver.execute_script(js)
driver.close() 
driver.switch_to_window(driver.window_handles[0])


name = [k.text.split()[1] for k in driver.find_elements_by_class_name('moviename-td')][0:8]  
sale = [k.text for k in driver.find_elements_by_class_name('realtime')][0:8]
sale_stat = pd.DataFrame({'name':name,'sale':sale})

film_stat = pd.merge(film_stat,sale_stat,on='name',how='left')



drama_info=pd.DataFrame()



for i in range(spring.shape[0]):
    url = 'https://movie.douban.com/subject/'+str(spring['douban_id'][i])
    js='window.open("'+url+'")'
    driver.execute_script(js)
    driver.close() 
    driver.switch_to_window(driver.window_handles[0])
    bsObj=BeautifulSoup(driver.page_source,"html.parser")
    time.sleep(2)
    data =  json.loads(bsObj.find('script',attrs={'type':'application/ld+json'}).contents[0].replace('\n','').replace(' ',''))
    drama_image = data['image']
    drama_info = drama_info.append({'name':spring['name'][i],'image':drama_image},
                                    ignore_index=True)  
 
film_stat = pd.merge(film_stat,drama_info,on='name',how='left') 

film_stat.to_excel('春节档电影统计数据.xlsx')