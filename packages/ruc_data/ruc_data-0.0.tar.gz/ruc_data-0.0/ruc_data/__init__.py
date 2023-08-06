import pandas as pd
import requests
#爬虫header配置
import pandas as pd
import requests
from multiprocessing.pool import Pool
from bs4 import BeautifulSoup
import re
import json
session = requests.Session()

#配置header
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8"}


#https://www.techinasia.com/wp-json/techinasia/2.0/tags/china/posts?page=18&per_page=5

def get_url_ll(url):
    try: # 引入header配置
        result = session.get(url, headers=header,timeout=10)
        #print(type(result))
        print(url)
        #return [result.text, url]
        return result.text
    except:
        pass
#https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do?date=2019/06/21
#seed_url='https://s.weibo.com/top/summary?cate=realtimehot'



import pandas as pd

def creep_guba(seed_url ):
    data=get_url_ll( seed_url ) #调用 函数
    soup = BeautifulSoup(data, 'html.parser')
    #print(soup)
    
    # 解析，获取 url 的列表
    #for n in soup.select('div[class="articleh normal_post"] '):
    res2=[]
    for n in soup.select('div[class="articleh normal_post"]'): #span[class="l3 a3"]
        #soup1 = BeautifulSoup(n,"lxml")
        # for n1 in soup1find('span'):   # = BeautifulSoup(n,"lxml")
        #print('next')
        # print(n1)
        #print(n.attrs)
        # print(n.contents[5],'content5')#children
        #print(type(n.contents[5])) #<class 'bs4.element.Tag'>
        #print(type(n.contents[5].a)) # . 访问 子标签
        # print(n.contents[5].a.attrs,'字典格式的 标签属性')
        #{'href': '/news,601162,858718684.html', 'title': '11.14成本，全部清仓了，这次亏大发了。主力可以拉了'}
        # tag['class']
        
        #print(n.contents[5].a['href'],'href') #children
        url='http://guba.eastmoney.com'+n.contents[5].a['href']
        #print(url)
        #for child in n.children:
            # print(type(child))
            # print('next')  
           # print(child.get_text())
            #print(child.string)
        #print(n.children[4],'content4')
        #soup1 = BeautifulSoup(n,'html.parser')
        #a=soup1.find('div[class="articleh normal_post span')
        #print(a)
        #print(n > span)
        #soup.find('div',attrs={"class":"l1 a1"}):#soup.select('.l1 a1'):  #('td[class="td-02"]'):  #选出 ，得到 url的列表  class="journal-item cf"
        
        #print(len(n.text.strip()))
        #print(n.text)
        #print(n.text.split('\n'))
        
        #lis=[]
        x= n.text.split('\n')
        #print(x)
        #print(type(x))
        x.append(url)
        #print( x.append(url))
        #print(x)
        #print(type(n))
        #res1.append(n.text.strip())
        res2.append(x)
        #print(n['href'])
        #results.append(getNewsDetail('http://you.ctrip.com' + n['href']))
        #getNewsDetail('http://you.ctrip.com' + n['href'])# 解析 每个url 
    #
   # print(res2)
    #二维列表data 转换成df
    #
    
    #二维列表
    #a = [['1','2','3'],['4','5','6']] #列表a中包括两个子列表
    
    #转换成df
    news=pd.DataFrame(res2)
    #print(news,'ok1')


    # 替换标题
    news.rename(columns={0:'null',1:'阅读',2:'评论',3:'标题',4:'作者',5:'最后更新',6:'null',7:'链接'},inplace=True)#注意这里0和1都不是字符串
    #print(news,'ok2')
    #news
    news.drop(labels=['null'], axis=1,inplace = True)

    
    return news

