# -*- coding: utf-8 -*-
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
def getList():
    self.s=requests.session()
    self.s.verify = False  # 忽略https 证书验证
    
    #登录URL  
    login_url = "https://login.hujiang.com/"  
    #登陆成功，我的URL  

    req = urllib.request.Request('https://class.hujiang.com/webapi/v1/hitalkkids/reserve/teachertime?startTime=2018-04-18T00%3A00%3A00%2B08%3A00&endTime=2018-04-25T00%3A00%3A00%2B08%3A00&classId=17380104&teacherId=90037790')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    html = urllib.request.urlopen(req).read()
    return html
print (getList())