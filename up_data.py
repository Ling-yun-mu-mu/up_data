import requests
from bs4 import BeautifulSoup
import lxml
import json
import socket
import re

login_url = "http://yiqing.ctgu.edu.cn/wx/index/loginSubmit.do"
updata_url = "http://yiqing.ctgu.edu.cn/wx/health/saveApply.do"
imformation_url = "http://yiqing.ctgu.edu.cn/wx/health/toApply.do"

login_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Referer": "http://yiqing.ctgu.edu.cn/wx/index/logout.do",
}

updata_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Referer":"http://yiqing.ctgu.edu.cn/wx/health/toApply.do",
}

login_data = {
    "username": "2018111332",
    "password": "144212"
}

updata_data = {
    "ttoken": "418f4d4b-fd04-4d46-aaa1-0a3f20fb8bf9",
    "province": "湖北省",
    "city": "宜昌市",
    "district": "西陵区",
    "adcode": "421122",
    "longitude": "0",
    "latitude": "0",
    "sfqz": "否",
    "sfys": "否",
    "sfzy": "否",
    "sfgl": "否",
    "status": "1",
    "sfgr": "否",
    "szdz": "湖北省 宜昌市 西陵区",
    "sjh": "18272128936",
    "lxrxm": "",
    "lxrsjh":"",
    "sffr": "否",
    "sffy": "否",
    "sfgr": "否",
    "qzglsj":"",
    "qzgldd":"",
    "glyy":"",
    "mqzz":"",
    "sffx": "否",
    "qt": "无"
}






proxies = {
    "http": 'http://222.74.202.229:9999'
}
req = requests.session()

req.post(login_url,headers=login_headers,data=login_data,proxies=proxies)

res = req.get(imformation_url,headers=updata_headers,proxies=proxies)
soup = BeautifulSoup(res.content.decode('utf-8'),'lxml')

tokens = soup.find_all("input")[0]
token_value = tokens.attrs['value']
updata_data['ttoken'] = token_value

res = req.post(updata_url,headers=updata_headers,data=updata_data,proxies=proxies)
print(res.text)
