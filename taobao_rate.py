# -*- coding: utf-8 -*-
# coding=gbk

import codecs
import requests
import json
import re

#  ������è��Ʒ������ҳ��url,����Դ���룬Ѱ����Ʒ����������
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


# ��ѯ����page����
def get_total_page(ids):
    url = r'https://rate.tmall.com/list_detail_rate.htm? %s&%s&%s'%(ids[0], ids[1], ids[2])
    req = requests.get(url+'&currentPage=100000000', verify=False)  # ȡһ��������10000000��ȥ��̽���һ��ҳ���ֵ
    data = req.text[15:]            # ɾ��ҳ�����ݵ�ǰ14���ַ���Ϊ����һ������תΪjson ��ʽ�ļ�
    jsondata = json.loads(data)
    total_page = jsondata["paginator"]["lastPage"]      #���һ��ҳ���Ժ��ҳ��������У�lastPageֵ��Ϊ���ֵ
    return total_page

# ��ѯָ��ҳ�������
def get_rate_from_index(ids, index):

    f = codecs.open(r'd:\text.txt','a','utf-8')
    url = r'https://rate.tmall.com/list_detail_rate.htm? %s&%s&%s'%(ids[0], ids[1], ids[2])
    rate_url = url + r"&currentPage=%d"%(index)     #  ��è��Ʒ����ҳ��洢��url
    #print rate_url
    f.write(rate_url)
    f.write('\n')
    req = requests.get(rate_url, verify=False)
    data = req.text[15:]            # ɾ��ҳ�����ݵ�ǰ14���ַ���Ϊ����һ������תΪjson ��ʽ�ļ�
    jsondata = json.loads(data)
    rateList = jsondata["rateList"]  # ��ȡ�����б�
    for item in rateList:
        print "Comment: " ,item["rateContent"] 
        f.write(item["rateContent"])
        f.write('\n')
        if item["appendComment"]:
            print "appendComment: ", item["appendComment"]["content"]
            f.write(item["appendComment"]["content"])
            f.write('\n')
    f.close()


# ������Ʒ������ֵ��ҳ������������Ʒ���������۽�������
def get_rate(ids, total_page):
    error_page = []  # ���ڻ�������ִ��󣬵��²���ҳ���޷���ȡ��������¼���ִ����ҳ��
    for index in range(1,total_page+1):  # ���е�ҳ����������ݽ�����ȡ
        try:
            get_rate_from_index(ids, index)
        except Exception,ex:               # ����ҳ���޷���ȡ����¼�� error_page��
            error_page.append(index)

    while len(error_page) != 0:             # �����δ��ȡ��ҳ�棬��һֱ��ȡ��ҳ�棬ֱ�� error_pageΪ0
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
    #f.write('huang'+'���θ�����Ʒ������ֵ��ҳ������������Ʒ���������۽������������Ʒ������ֵ��ҳ������������Ʒ���������۽������������Ʒ������ֵ��ҳ������������Ʒ���������۽������������Ʒ������ֵ��ҳ������������Ʒ���������۽������������Ʒ������ֵ��ҳ������������Ʒ���������۽������������Ʒ������ֵ��ҳ������������Ʒ���������۽������������Ʒ������ֵ��ҳ������������Ʒ���������۽������������Ʒ������ֵ��ҳ������������Ʒ���������۽������������Ʒ������ֵ��ҳ������������Ʒ���������۽�������')

