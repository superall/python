
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2018/6/25 0025 19:27
import requests
import random
import config
from station import station
class TicketRob:
 def __init__(self):
 self.session = requests.Session()
 self.session.headers.update({
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
 })
 self.index_url = 'https://kyfw.12306.cn/otn/login/init'
 self.captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image'
 self.login_url = 'https://kyfw.12306.cn/passport/web/login'
 self.check_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
 self.uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
 self.auth_url = 'https://kyfw.12306.cn/otn/uamauthclient'
 self.left_tickets_url = 'https://kyfw.12306.cn/otn/leftTicket/query'
 self.submit_order_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
 self.point = {
 '1': '35,43',
 '2': '108,43',
 '3': '185,43',
 '4': '254,43',
 '5': '34,117',
 '6': '108,117',
 '7': '180,117',
 '8': '258,117',
 }
 def get_point(self, nums):
 """
 拼接坐标点
 :param nums: 图片序号 '1,2'
 :return:
 """
 nums = nums.split(',')
 temp = []
 for item in nums: # ['1', '2']
 temp.append(self.point[item])
 return ','.join(temp)
 # 检查用户名密码
 def login(self, username, password):
 data = {
 'username': username,
 'password': password,
 'appid': 'otn'
 }
 self.session.get(self.index_url) # 1
 self.get_captcha() # 2
 check_res = self.check_captcha() # 3
 if check_res:
 response = self.session.post(self.login_url, data=data) # 4
 print(response.text)
 if response.json()['result_code'] == 0:
 tk = self.get_tk() # 5
 auth_res = self.get_auth(tk) # 6
 if auth_res:
 return {'status': True, 'info': '登陆成功'}
 else:
 return {'status': False, 'info': '权限获取失败!'}
 else:
 return {'status': False, 'info': '用户名密码错误'}
 else:
 return {'status': False, 'info': '验证码校验失败!'}
 # 校验验证码
 def check_captcha(self):
 data = {
 'answer': self.get_point(input('请输入正确的图片序号>>>:')),
 'login_site': 'E',
 'rand': 'sjrand'
 }
 response = self.session.post(self.check_captcha_url, data=data)
 if response.json()['result_code'] == '4':
 return True
 return False
 # 获取验证码
 def get_captcha(self):
 data = {
 'login_site': 'E',
 'module': 'login',
 'rand': 'sjrand',
 str(random.random()): ''
 }
 response = self.session.get(self.captcha_url, params=data)
 with open('captcha.jpg', 'wb') as f:
 f.write(response.content)
 # 获取权限token
 def get_tk(self):
 uamtk_data = {
 'appid': 'otn'
 }
 response = self.session.post(self.uamtk_url, data=uamtk_data)
 return response.json()['newapptk']
 # 获取权限
 def get_auth(self, tk):
 auth_data = {
 'tk': tk
 }
 response = self.session.post(self.auth_url, data=auth_data)
 if response.json()['result_code'] == 0:
 return True
 return False
 # 查余票
 def query_left_ticket(self, train_date, from_station, to_station):
 # data = { ***** 参数的顺序非常重要
 # 'leftTicketDTO.train_date': train_date, # '2018-06-30', # 是时间
 # 'leftTicketDTO.from_station': from_station, # 'BJP', # 起始站
 # 'leftTicketDTO.to_station': to_station, # 'SHH', # 到达站
 # 'purpose_codes': 'ADULT'
 # }
 url = '%s?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (
 self.left_tickets_url,train_date,from_station,to_station)
 response = self.session.get(url)
 res = response.json()
 if res['status']:
 return res['data']['result']
 # 提交订单
 def submit_order(self, secretstr):
 data = {
 'secretStr':secretstr,
 'train_date': '2018-07-01',
 'back_train_date': '2018-06-28',
 'tour_flag': 'dc',
 'purpose_codes': 'ADULT',
 'query_from_station_name': '北京',
 'query_to_station_name': '上海',
 'undefined':''
 }
 response = self.session.post(self.submit_order_url, data=data)
 print(response.text)
 # {"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":"N","messages":[],"validateMessages":{}}
if __name__ == '__main__':
 from urllib import parse
 ticket = TicketRob()
 ticket.login(config.username, config.password) # 登陆
 res = ticket.query_left_ticket('2018-07-01', station['北京'][2], station['上海'][2]) # 查票
 print(res)
 print('111111111111111111111')
 secretstr = res[2].split('|')[0]
 secretstr = parse.unquote(secretstr)
 print(secretstr)
 print('22222222222222222222')
 ticket.submit_order(secretstr)
 # res = ticket.query_left_ticket('2018-06-30', 'BJP', 'SHH')
 # print(res)
 # print(ticket.login(config.username, config.password))
 # temp = {
 # 'a': {
 # 'b': 'aaa'
 # }
 # }
