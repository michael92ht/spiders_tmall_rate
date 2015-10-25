# -*- coding: utf-8 -*-
# coding=gbk

import codecs
import requests
import json
import re

#  ¸ù¾ÝÌìÃ¨ÉÌÆ·µÄÏêÇéÒ³Ãæurl,´ò¿ªÆäÔ´´úÂë£¬Ñ°ÕÒÉÌÆ·µÄÈý¸öÊôÐÔ
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


# ²éÑ¯ËùÓÐpageÊýÁ¿
def get_total_page(ids):
    url = r'https://rate.tmall.com/list_detail_rate.htm? %s&%s&%s'%(ids[0], ids[1], ids[2])
    req = requests.get(url+'&currentPage=100000000', verify=False)  # È¡Ò»¸ö¼«´óÊý10000000£¬È¥ÊÔÌ½×îºóÒ»¸öÒ³ÃæµÄÖµ
    data = req.text[15:]            # É¾³ýÒ³ÃæÄÚÈÝµÄÇ°14¸ö×Ö·û£¬ÎªÁËÏÂÒ»²½¿ÉÒÔ×ªÎªjson ¸ñÊ½ÎÄ¼þ
    jsondata = json.loads(data)
    total_page = jsondata["paginator"]["lastPage"]      #×îºóÒ»¸öÒ³ÃæÒÔºóµÄÒ³ÃæµÄÄÚÈÝÖÐ£¬lastPageÖµ¼´Îª×î´óÖµ
    return total_page

# ²éÑ¯Ö¸¶¨Ò³ÃæµÄÆÀÂÛ
def get_rate_from_index(ids, index):

    f = codecs.open(r'd:\text.txt','a','utf-8')
    url = r'https://rate.tmall.com/list_detail_rate.htm? %s&%s&%s'%(ids[0], ids[1], ids[2])
    rate_url = url + r"&currentPage=%d"%(index)     #  ÌìÃ¨ÉÌÆ·ÆÀ¼ÛÒ³Ãæ´æ´¢µÄurl
    #print rate_url
    f.write(rate_url)
    f.write('\n')
    req = requests.get(rate_url, verify=False)
    data = req.text[15:]            # É¾³ýÒ³ÃæÄÚÈÝµÄÇ°14¸ö×Ö·û£¬ÎªÁËÏÂÒ»²½¿ÉÒÔ×ªÎªjson ¸ñÊ½ÎÄ¼þ
    jsondata = json.loads(data)
    rateList = jsondata["rateList"]  # »ñÈ¡ÆÀÂÛÁÐ±í
    for item in rateList:
        print "Comment: " ,item["rateContent"] 
        f.write(item["rateContent"])
        f.write('\n')
        if item["appendComment"]:
            print "appendComment: ", item["appendComment"]["content"]
            f.write(item["appendComment"]["content"])
            f.write('\n')
    f.close()


# ¸ù¾ÝÉÌÆ·µÄÊôÐÔÖµºÍÒ³ÃæÊýÁ¿£¬¶ÔÉÌÆ·µÄËùÓÐÆÀÂÛ½øÐÐÅÀ³æ
def get_rate(ids, total_page):
    error_page = []  # ÓÉÓÚ»áËæ»ú³öÏÖ´íÎó£¬µ¼ÖÂ²¿·ÖÒ³ÃæÎÞ·¨»ñÈ¡£¬ÓÃÀ´¼ÇÂ¼³öÏÖ´íÎóµÄÒ³Ãæ
    for index in range(1,total_page+1):  # ËùÓÐµÄÒ³ÃæµÄÆÀÂÛÄÚÈÝ½øÐÐÌáÈ¡
        try:
            get_rate_from_index(ids, index)
        except Exception,ex:               # Èô´ËÒ³ÃæÎÞ·¨ÌáÈ¡£¬¼ÇÂ¼µ½ error_pageÖÐ
            error_page.append(index)

    while len(error_page) != 0:             # Èç¹ûÓÐÎ´ÌáÈ¡µÄÒ³Ãæ£¬¾ÍÒ»Ö±ÌáÈ¡¸ÃÒ³Ãæ£¬Ö±ÖÁ error_pageÎª0
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
    #f.write('huang'+'»ÆÌÎ¸ù¾ÝÉÌÆ·µÄÊôÐÔÖµºÍÒ³ÃæÊýÁ¿£¬¶ÔÉÌÆ·µÄËùÓÐÆÀÂÛ½øÐÐÅÀ³æ¸ù¾ÝÉÌÆ·µÄÊôÐÔÖµºÍÒ³ÃæÊýÁ¿£¬¶ÔÉÌÆ·µÄËùÓÐÆÀÂÛ½øÐÐÅÀ³æ¸ù¾ÝÉÌÆ·µÄÊôÐÔÖµºÍÒ³ÃæÊýÁ¿£¬¶ÔÉÌÆ·µÄËùÓÐÆÀÂÛ½øÐÐÅÀ³æ¸ù¾ÝÉÌÆ·µÄÊôÐÔÖµºÍÒ³ÃæÊýÁ¿£¬¶ÔÉÌÆ·µÄËùÓÐÆÀÂÛ½øÐÐÅÀ³æ¸ù¾ÝÉÌÆ·µÄÊôÐÔÖµºÍÒ³ÃæÊýÁ¿£¬¶ÔÉÌÆ·µÄËùÓÐÆÀÂÛ½øÐÐÅÀ³æ¸ù¾ÝÉÌÆ·µÄÊôÐÔÖµºÍÒ³ÃæÊýÁ¿£¬¶ÔÉÌÆ·µÄËùÓÐÆÀÂÛ½øÐÐÅÀ³æ¸ù¾ÝÉÌÆ·µÄÊôÐÔÖµºÍÒ³ÃæÊýÁ¿£¬¶ÔÉÌÆ·µÄËùÓÐÆÀÂÛ½øÐÐÅÀ³æ¸ù¾ÝÉÌÆ·µÄÊôÐÔÖµºÍÒ³ÃæÊýÁ¿£¬¶ÔÉÌÆ·µÄËùÓÐÆÀÂÛ½øÐÐÅÀ³æ¸ù¾ÝÉÌÆ·µÄÊôÐÔÖµºÍÒ³ÃæÊýÁ¿£¬¶ÔÉÌÆ·µÄËùÓÐÆÀÂÛ½øÐÐÅÀ³æ')

