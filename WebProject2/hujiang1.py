#import requests
import time
#import dmpt
import re
import random
#from copyheaders import headers_raw_to_dict
 
DEFAULT_HEADERS={
'Host':'kyfw.12306.cn',
'Connection':'keep-alive',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Language':'zh-CN,zh;q=0.9',
}
def get_random():
  return str(random.random()) #生产一个18位的随机数
def get_13_time(): #一个十三位的时间戳
  return str(int(time.time()*1000))
class hujiang(object):
  def __init__(self):
    #self.chufa='2018-02-03'
    self.s=requests.session()
    self.s.verify = False  # 忽略https 证书验证
  def get_init(self): #请求了一个首页,登录URL
    url='https://login.hujiang.com/'
    r=self.s.get(url)
    print('首页获取成功，状态码：',r)
 
  
  def login(self):
    url='https://kyfw.12306.cn/passport/web/login'
    data={
    'username' : '12306帐号',
    'password' : '12306密码',
    'appid' : 'otn',
    }
    r=self.s.post(url=url,data=data)
    self.uamtk=r.json()["uamtk"]
 
    print(r.text)
 
  def userLogin(self):
    url='https://kyfw.12306.cn/otn/login/userLogin'
    r=self.s.post(url=url)
    # print(r.text)
  def getjs(self):  #不知道是干啥的，但是也提交吧
    url='https://kyfw.12306.cn/otn/HttpZF/GetJS'
    r=self.s.get(url)
  def post_uamtk(self):
    url='https://kyfw.12306.cn/passport/web/auth/uamtk'
    data={ 'appid':'otn'}
    r=self.s.post(url=url,data=data,allow_redirects=False)
    self.newapptk=r.json()["newapptk"]
    r.encoding='utf-8'
    print(r.text)
  def post_uamauthclient(self):
    url='https://kyfw.12306.cn/otn/uamauthclient'
    data={
      'tk':self.newapptk
    }
    r=self.s.post(url=url,data=data)
    self.apptk = r.json()["apptk"]
    r.encoding='utf-8'
    print(r.text)
  def get_userLogin(self):
    url='https://kyfw.12306.cn/otn/login/userLogin'
    r=self.s.get(url)
    r.encoding='utf-8'
    # print(r.text)
  def get_leftTicket(self):
    url='https://kyfw.12306.cn/otn/leftTicket/init'
    r=self.s.get(url)
    r.encoding='utf-8'
    # print(r.text)
  def get_GetJS(self):
    url='https://kyfw.12306.cn/otn/HttpZF/GetJS'
    self.s.get(url)
 
  def get_qufzjql(self):
    url = 'https://kyfw.12306.cn/otn/dynamicJs/qufzjql'
    self.s.get(url)
 
  def get_queryZ(self):
    url='https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}'.format(self.chufa,'BJP','TBP','ADULT')
    r=self.s.get(url)
    r.encoding='utf-8'
    # print(r.text)
    cheliang=r.json()["data"]["result"]
    for i in cheliang:
      dandulist=str(i).split('|')
      if len(str(dandulist[0]))>=100:
        self.secretStr=dandulist[0]
        # secretStr = str(x[0])
        车次=str(dandulist[3])
        出发时间=str(dandulist[8])
        到达时间 = str(dandulist[9])
        历时=str(dandulist[10])
        软卧 = str(dandulist[23])
        硬卧=str(dandulist[28])
        print(i)
        print('可预订车次列表，','车次：',车次,'出发时间：', 出发时间,'到达时间：', 到达时间,'历时：', 历时,'软卧剩余： ',软卧,' 硬卧剩余： ',硬卧)
        if (软卧 != '' and 软卧 != '0' and 软卧 != '无' and 软卧 != '空') or (硬卧 != '' and 硬卧 != '0' and 硬卧 != '无' and 硬卧 != '空'):
          #执行下单操作
          self.post_submitOrderRequest()
          self.post_initDc()
          self.post_getPassengerDTOs()
          return False
 
      print('*****************************************************')
    return True
 
 
  # 点击预定下单
  def post_submitOrderRequest(self):
    url='https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    data={
      'secretStr':self.secretStr,
      'train_date':self.chufa, #出发时间
      'back_train_date':self.chufa ,#返回时间
      'tour_flag':'dc',
      'purpose_codes':'ADULT',
      'query_from_station_name':'北京',
      'query_to_station_name':'天津北',
      'undefined':''
       }
    r=self.s.post(url=url,data=data)
    print(r.text)
  def post_initDc(self):
    url='https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    r=self.s.post(url)
    # r.text
    self.REPEAT_SUBMIT_TOKEN=re.findall("globalRepeatSubmitToken = '(.*?)';",r.text)[0]
  def post_getPassengerDTOs(self): #获取乘客信息
    url='https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    data={
      'REPEAT_SUBMIT_TOKEN':self.REPEAT_SUBMIT_TOKEN,
      '_json_att':''
    }
    r=self.s.post(url=url,data=data)
    r.encoding='utf-8'
    print(r.text)
 
if __name__ == '__main__':
  print(get_random())
  cn=CN12306()
  cn.get_init()
  cn.get_newpasscode()
  if cn.get_auth_code():
    #如果验证码获取成功，就调用打码平台
    print('验证码获取成功')
    print('正在调用打码平台...')
    cn.analysis_auth_code()
    if cn.auth_auth_code(): #验证验证码是否正确
      cn.login()
      cn.userLogin()
      cn.getjs()
      cn.post_uamtk()
      cn.post_uamauthclient()
      cn.get_userLogin()
      cn.get_leftTicket()
      cn.get_GetJS()
      cn.get_qufzjql()
 
      while cn.get_queryZ():
        time.sleep(30)
