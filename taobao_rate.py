# -*- coding: utf-8 -*-
# coding=gbk

import codecs
import requests
import json
import re

#  根据天猫商品的详情页面url,打开其源代码，寻找商品的三个属性
def get_ids_from_url(url):

    flag = True
    while flag:
        try:
            req = requests.get(url, verify=False)
            data = req.text

            itemId = re.findall(r'itemId=[0-9]+', data)[0]
            spuId = re.findall(r'spuId=[0-9]+', data)[0]
            sellerId = re.findall(r'sellerId=[0-9]+', data)[0]
            # flag = False
            return itemId, spuId, sellerId
        except Exception,ex:  
            pass


# 查询所有page数量
def get_total_page(ids):
    url = r'https://rate.tmall.com/list_detail_rate.htm? %s&%s&%s'%(ids[0], ids[1], ids[2])
    req = requests.get(url+'&currentPage=100000000', verify=False)  # 取一个极大数10000000，去试探最后一个页面的值
    data = req.text[15:]            # 删除页面内容的前14个字符，为了下一步可以转为json 格式文件
    jsondata = json.loads(data)
    total_page = jsondata["paginator"]["lastPage"]      #最后一个页面以后的页面的内容中，lastPage值即为最大值
    return total_page

# 查询指定页面的评论
def get_rate_from_index(ids, index):

    f = codecs.open(r'd:\text.txt','a','utf-8')
    url = r'https://rate.tmall.com/list_detail_rate.htm? %s&%s&%s'%(ids[0], ids[1], ids[2])
    rate_url = url + r"&currentPage=%d"%(index)     #  天猫商品评价页面存储的url
    #print rate_url
    f.write(rate_url)
    f.write('\n')
    req = requests.get(rate_url, verify=False)
    data = req.text[15:]            # 删除页面内容的前14个字符，为了下一步可以转为json 格式文件
    jsondata = json.loads(data)
    rateList = jsondata["rateList"]  # 获取评论列表
    for item in rateList:
        print "Comment: " ,item["rateContent"] 
        f.write(item["rateContent"])
        f.write('\n')
        if item["appendComment"]:
            print "appendComment: ", item["appendComment"]["content"]
            f.write(item["appendComment"]["content"])
            f.write('\n')
    f.close()


# 根据商品的属性值和页面数量，对商品的所有评论进行爬虫
def get_rate(ids, total_page):
    error_page = []  # 由于会随机出现错误，导致部分页面无法获取，用来记录出现错误的页面
    for index in range(1,total_page+1):  # 所有的页面的评论内容进行提取
        try:
            get_rate_from_index(ids, index)
        except Exception,ex:               # 若此页面无法提取，记录到 error_page中
            error_page.append(index)

    while len(error_page) != 0:             # 如果有未提取的页面，就一直提取该页面，直至 error_page为0
        pages = [i for i in error_page]
        error_page = []
        for page in pages:
            try:
                get_rate_from_index(ids, page)
            except Exception,ex:
                error_page.append(index)

    print "total page count: ",total_page
    print "------------------------finshed!-------------------------------"



if __name__ == "__main__":
    url = r"https://detail.tmall.com/item.htm?spm=a1z10.4-b.w5003-11468429403.2.lLWtOQ&id=43609016187&sku_properties=5919063:6536025&scene=taobao_shop"
    ids = get_ids_from_url(url)
    total = get_total_page(ids)
    get_rate(ids, total)
    #get_rate_from_index(ids, 75)
    #f = open(r'd:\text.txt','a')
    #f.write('huang'+'黄涛根据商品的属性值和页面数量，对商品的所有评论进行爬虫根据商品的属性值和页面数量，对商品的所有评论进行爬虫根据商品的属性值和页面数量，对商品的所有评论进行爬虫根据商品的属性值和页面数量，对商品的所有评论进行爬虫根据商品的属性值和页面数量，对商品的所有评论进行爬虫根据商品的属性值和页面数量，对商品的所有评论进行爬虫根据商品的属性值和页面数量，对商品的所有评论进行爬虫根据商品的属性值和页面数量，对商品的所有评论进行爬虫根据商品的属性值和页面数量，对商品的所有评论进行爬虫')

