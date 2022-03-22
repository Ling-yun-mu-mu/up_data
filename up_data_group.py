import requests
from bs4 import BeautifulSoup
import lxml
import numpy as np
import xlrd
import datetime

proxies = {
   "http": '42.194.232.51:8088'
}

login_url = "http://yiqing.ctgu.edu.cn/wx/index/loginSubmit.do"
updata_url = "http://yiqing.ctgu.edu.cn/wx/health/saveApply.do"
imformation_url = "http://yiqing.ctgu.edu.cn/wx/health/toApply.do"
Excel_url = "https://docs.qq.com/v1/export/export_office"

login_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Referer": "http://yiqing.ctgu.edu.cn/wx/index/logout.do"
}

updata_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Referer":"http://yiqing.ctgu.edu.cn/wx/health/toApply.do"
}

Excel_headers = {
    'referer': 'https://docs.qq.com/sheet/DWVpQTHJ3VmN4Qk5C?fileMD5=3262633033616234306134613137663536626138623433383066306132663163&chatId=951564501&chatType=2&groupUin=9lzDdM8tOHnedBT8ESZPsA%25253D%25253D&ADUIN=2115605867&ADSESSION=1609820418&ADTAG=CLIENT.QQ.5785_.0&ADPUBNO=27077&tab=BB08J2',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
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


Excel_data = {
    'docId': '300000000$YZPLrwVcxBNB',
    'content': 'eJztnU9vG0UYh7/LcB2qXdtxHN/aQqEILgRxsa1q2h3bq453o9kxSbF8ILQhkdqqCBT+liKE1F6aHBAU0tB+mo3rU78C78yuHUfh0BbibeEXryYz784888y7m9k9OQPWlSKQmtUbAxYGrM7OnPFq75QYZ5HoSWoHwghqdcMgkBGrt4VK5LDFJ/3qg6xHvdFg6d0v0ls3qPPoy3sHmw+yerq7MfrxExv83pbp7+u2vPn46f5men3v6f4WNcfrO6P9bTfw1ye7txmP+kqdXNHi5Lr59cHtRzRlyfNrvu+Xy3bNfqVS8m3l4I/t9PpXmfL44dV0YzMTH+39lO5skT7VK5Wy53l2VK20SMNqS+XqPNTHn94/+OZeem3r0L7iV22j5i8ct7+6nj74IbO39Ts3Ke1H7MtLtWqlVFv0yvNK/PZn6Y1vGc/lKXW8VKWGdyzvozu/5DfMz3fTjd+y+sScBi/61apXWSifvPfJTgARiEAEIhCBCEQgAhGIQAQiEIEIRCACEYhABCIQgQhECneACEQgAhGIQAQiECnaASIQgQhEIAIRiECkaAeIQAQiEIEIRCACkaIdIAIRiEAEIhCBCESKdoAIRCACEYhABCIQKdoBIhCBCEQgAhGIQKRoB4hABCIQgQhEIAKRoh0gAhGIQAQiEIEIRIp2gAhEIAIRiEAEIhAp2gEiEIHIKy7S4iwxV5RM7P/y8vjRz+v+ix20vJcT5fMSfXz3sbV/gHrRoUACCSSQQAIJJJBAAgkkkEACCSSQQAIJJJBAAgkkkEACCSSQQAIJJJBAAgkkkEACCSSQQAIJJJBAAgkkkEACCSSQQAIJJJBAAgkkkEAC+d9EtjgzsreihHHfYkDNntQdeVYqlZyP2nEW0/Hq2zLsdI3tU6pwHDj+7YNus0uxOrzNalXuewunlnxOtdnD97xT1WPRZz7y2zkMJKsPhtmk04YRF5VclsaEUYckBqwdrsngbKz6vSh5V7YNq3s8C74fryYfxCsUoHHtWPf6Shz+xSTduK+C90TUF4oibaESyVGiRInypS/dBiZWJq8EgTDiQ6mTMI5YvcSZ6Jv4XKiM1HaL1LKddWu7ULZZZpFuGAQyop3SNocOqmWwbHS2vTYaZU7baWPQZIkR2pyPArnWtFts0+2owlCDTtIWHeusSsPzDh0tZZTXL6q+zKtCrXQF1X2qdx2tyV7z3E+TUeyyvOJigzw4bLKhmy4y50QvVNnZ0zoUyvW3J5bDjy3ed1PFyhpkyWqy0AgVXpoJJLS4y9J0ddzvdGfifVqbVmFkQe4bpGZUpi7czUtPuL+5MLnodJDHn3GcHdhi9PJY5mUke37JriDZ80v2ApI9n2RPHgfkS7/piZBMX3hXOzoMWN3ovuQs7EQxZflNrWOdTLZ/+2V5b0gjQvtOPHBJYHXmJmA8uz7UznUYd1lru3RSeHR/a7T3OI8mlEtKpc/zK3zBzuxNW1aRhrwlI6npBTwbc5zfvUDL6NDDinWmPbNLMaOVXQqb85mgkWtmVQt6/WdR7Cr88NrM9PtoOkOPnoVKUvKfd93uohxdtvc/WHb6aOfJn7vj766NH37+yq++NfwLT7qOxg==',
    'comments': [{"id":"BB08J2","anchors":[]}],
    'version': '2'
}


class Read_Ex():
    def read_excel(self,filename):
        #打开excel表，填写路径
        book = xlrd.open_workbook(filename)
        #找到sheet页
        table = book.sheet_by_name("data")
        #获取总行数总列数
        row_Num = table.nrows
        col_Num = table.ncols

        s =[]
        key =table.row_values(0)# 这是第一行数据，作为字典的key值

        if row_Num <= 1:
            print("没数据")
        else:
            j = 1
            for i in range(row_Num-1):
                d ={}
                values = table.row_values(j)
                for x in range(col_Num):
                    # 把key值对应的value赋值给key，每行循环
                    d[key[x]]=values[x]
                j+=1
                # 把字典加到列表中
                s.append(d)
            return s





if __name__ == '__main__':
    r = Read_Ex()
    s=r.read_excel('data.xls')
    for i in s:
        print(i['姓名'])
        login_data['username'] = str(int(i['用户名']))
        login_data['password'] = str('%06d'%int(i['密码']))
        updata_data['province'] = i['省']
        updata_data['city'] = i['市']
        updata_data['district'] = i['县（区）']
        updata_data['adcode'] = str(int(i['邮编']))
        updata_data['szdz'] = i['省']+' '+i['市']+' '+i['县（区）']
        updata_data['sjh'] = str(int(i['电话']))
        print(login_data)

        req = requests.session()
        req.post(login_url,headers=login_headers,data=login_data,proxies=proxies)

        res = req.get(imformation_url,headers=updata_headers,proxies=proxies)
        soup = BeautifulSoup(res.content.decode('utf-8'),'lxml')

        try:
            tokens = soup.find_all("input")[0]
            token_value = tokens.attrs['value']
            updata_data['ttoken'] = token_value

            res = req.post(updata_url,headers=updata_headers,data=updata_data,proxies=proxies)
        except Exception as e:
            with open('log.txt','a') as f:
                f.write(i['姓名']+'：失败 '+str(e))
            print(e)
        else:
            with open('log.txt','a') as f:
                f.write(i['姓名']+'：成功 '+res.text)
            print(res.text)
        finally:
            localtime = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
            with open('log.txt','a') as f:
                f.write(' '+localtime+'\n')
            print(localtime,"\n")
