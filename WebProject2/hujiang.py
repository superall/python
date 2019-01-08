# -*- coding:utf-8 -*-  
"""
  @author Deyong Liu 
"""  
from splinter.browser import Browser  
from time import sleep  
import traceback  
import time,sys  
import os  
    
class Hujiang(object):  
      """docstring for Train"""  
      driver_name=''  
      executable_path=''  
      #用户名 密码  
      username = u"Peters_mom"  
      passwd = u"wydycg98"  
      """网址"""  
      #查询课程URL  
      ticket_url = "https://class.hujiang.com/talk/kids/calendar?classId=17380104"  
      #登录URL  
      login_url = "https://login.hujiang.com/"  
      #登陆成功，我的URL  
      initmy_url = "https://my.hujiang.com/account/"  
      #需要定课的星期几在page中对应的index
      indexs = []
      #需要定课的时间在page中对应的坐标列
      times = ['41', '42']  #20点的课程的纵坐标为41；20:30的课程纵坐标为42
    
      def __init__(self):  
          self.driver_name = 'chrome'  
          #self.executable_path = os.getcwd()+'/chromedriver'  
          print("Welcome To Use The Tool")  
        
      def login(self):  
          try:  
              self.driver.visit(self.login_url)  
              #填充密码  
              self.driver.fill("username",self.username)  
              #sleep(1)  
              self.driver.fill("password",self.passwd)  
              self.driver.find_by_tag("button").click()
              #self.driver.find_by_text(u"登陆").first().click()  
              #self.driver.find_element_by_xpath('//*[@id="hp-login-normal"]/button').first().click()
              print("登陆成功")  
              while True:  
                  if self.driver.url != self.initmy_url:  
                    sleep(1)  
                  else :  
                    break  
          except Exception as e:  
              print(e)  

      def start(self):  
          self.driver = Browser(driver_name=self.driver_name)  
          self.driver.driver.set_window_size(1400,1000)  
          self.login()  
          #sleep(1)  

          print("查询课程开始....")  
          self.driver.visit(self.ticket_url)  
          try:  
              #sleep(1)  
              self.driver.find_link_by_text("按老师预约").click()  
              print("找第一个老师并预约")  
              self.driver.find_link_by_text(u"预约").click()  

              weekday=self.driver.find_by_xpath('//div[@class="_3fqOfVfQ"]').first.value
              if (weekday == u'周一'):  #今天是周一,预约周2、5的课程的横向坐标索引
                  self.indexs = ['2', '5']
              elif (weekday == u'周二'):
                  self.indexs = ['1', '4']
              elif (weekday == u'周三'):
                  self.indexs = ['7', '3']
              elif (weekday == u'周四'):
                  self.indexs = ['6', '2']
              elif (weekday == u'周五'):
                  self.indexs = ['5', '1']
              elif (weekday == u'周六'):
                  self.indexs = ['4', '7']
              elif (weekday == u'周日'):
                  self.indexs = ['3', '6']
              else:
                  self.indexs = ['0', '0']  #无效值
              print("周二index={0}, 周五index={1}", format(self.indexs[0], self.indexs[1]))  
              print("20:00 time={0}, 20:30 time={1}", format(self.times[0], self.times[1]))  

          except Exception as e:  
              print(e)  
          self.subByTeacher()

      def subByTeacherPage(self):  
          for index in self.indexs:
              for time in self.times:
                  xpath_20='//*[@id="timeList"]/ul/li[' + index + ']/div/div[' + time + ']/a'  #20点的课程xpath
                  #xpath_20='//*[@id="timeList"]/ul/li[' + index + ']/div/div[' + time + ']'  #20点的课程空的xpath
                  #xpath_20_span='//*[@id="timeList"]/ul/li[' + index + ']/div/div[' + time + ']/span'  #20点的课程"已预约""约满"的xpath
                  canBeSubscribeds=self.driver.find_by_xpath(xpath_20)
                  if canBeSubscribeds:
                      try:
                          print("找到老师并预约对应时间index={0},time={1}", format(index, time))  
                          canBeSubscribeds.click()
                          self.driver.find_link_by_text("确认预约").click()  

                          confirm = self.driver.find_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[5]/div/div[2]/div[3]/div[2]/a[1]')
                          confirm.click()
                          print("预约成功")  
                          return True
                      except Exception as e:  
                          print(e)  
                  else:                      
                      continue
                  #if (canBeSubscribeds.first.value == u'可预约'):
              return False
              
      def subByTeacher(self):  
          success = self.subByTeacherPage()
          if (success):
              return
          else:
              print("找到下一页")  
              success = False
              try:
                  nextpage=self.driver.find_by_xpath('//div[@class="js_next trace_1 _1jM3tRIW"]')
                  #nextpage=self.driver.find_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]')
                  #nextpage=self.driver.find_by_xpath('//i[@class="hui-icon hui-icon-carat-r-small"]')
                  nextpage.click()
              except Exception as e:  
                  print(e)  
    
              success = self.subByTeacherPage()
              return success
 
    
      def subClass(self):  
          print("查询课程开始....")  
          for i in range(3):  #前3个老师
              self.driver.visit(self.ticket_url)  
              print("查询第{0}个老师的课程：",  format(str(i)))  
              self.driver.find_link_by_text(u"预约")[i].click()  #第3个老师预约
              self.subByTeacher()
    
if __name__=="__main__":  
      hujiang = Hujiang()  
      hujiang.start()
      hujiang.subClass()
          

