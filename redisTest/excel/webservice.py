#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 14:30
# @Author  : Aries
# @Site    : 
# @File    : webservice.py
# @Software: PyCharm

from urllib import request
import pickle
import threading
import time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class SwsxFbzl(object):

    def __init__(self):
        self.reqXml = r'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wwd="http://wwdzswj.webservice.com">
            <soapenv:Header/>
           <soapenv:Body>
              <wwd:getInfo>
                 <wwd:in0>%s</wwd:in0>
              </wwd:getInfo>
           </soapenv:Body>
        </soapenv:Envelope>'''

        self.gt3Url = r'http://93.12.72.122:8001/services/GetFlzlInfoService'

        self.filePath = r'swsxDm.txt'

    # 解析返回报文元素
    def parserResponseXml(self, xml) :
        root = ET.fromstring(xml)
        fbzlInfo = []
        for neighbor in root.iter():
            if neighbor.tag == "{http://wwdzswj.webservice.com}out":
                fbzlxml = ET.fromstring(neighbor.text)
                fbzls = fbzlxml.findall("flzl")
                for fbzl in fbzls :
                    flzlDm = fbzl.find('flzl_dm').text
                    flzlMc = fbzl.find('flzl_mc').text
                    isNeed = fbzl.find('is_need').text
                    order = fbzl.find('order').text
                    fbzlInfo.append({"flzl_dm":flzlDm,"flzl_mc":flzlMc,"is_need":isNeed,"order":order})
        return fbzlInfo

    # 从金三webservice获取数据
    def getGt3RtnFbzl(self, swsxDm) :
        print('从电子档案webservice获取资料配置, swsx_dm:%s'% swsxDm)
        requestXml = self.reqXml%swsxDm
        req = request.Request(self.gt3Url)
        with request.urlopen(req, data=requestXml.encode('utf-8')) as f:
            rtnXml = f.read().decode('utf-8')
        return rtnXml

    def getAndParserData(self, swsxDm):
        rtnXml = self.getGt3RtnFbzl(swsxDm)
        if rtnXml is None:
            return
        rtn = self.parserResponseXml(rtnXml)
        dictMap = {'swsx':swsxDm , 'data':rtn}
        with open('SwsxFbzl/' + swsxDm + '.txt', 'wb+') as file:
            pickle.dump(dictMap, file)
        print('swsx_dm : %s , 获取数据成功'% swsxDm)



    def getSwsxDm(self):
        with open(self.filePath) as file:
            swsxDmList = file.read().splitlines()

        for swsxDm in swsxDmList:
            tred = threading.Thread(target=self.getAndParserData,  args=(swsxDm,))
            tred.start()
            time.sleep(1)

    def parseResultDto(self):
        with open(self.filePath) as file:
            swsxDmList = file.read().splitlines()

        for swsxDm in swsxDmList:
            with open('SwsxFbzl/' + swsxDm + '.txt', 'rb+') as file:
                d = pickle.load(file)
                print(str(d))


if __name__ == '__main__':
    s = SwsxFbzl()
    s.parseResultDto()