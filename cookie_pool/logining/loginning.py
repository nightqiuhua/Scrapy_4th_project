import __init__
from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
import time
from logining.zjt_login import ZJT_Login
from DB.DbClient import DbClient
import os
import json


#1.获取cookies
#2.保存cookies
#3.提取/查询cookies
#4.删除cookies
#5.检验cookies


#登录步骤
#1.进入登录界面
#2.执行相关操作，输入账户名，密码或验证码
#3.登录跳转

#http://www.hzfyggzy.org.cn/web_news/WebNewsView.aspx?ViewID=27&ID=14766
class LoginCore:
    def __init__(self):
        self.db = DbClient()

    def cookie_login(self,driver,worker,account_dict):
        """
        网站登录并获取cookies
        """
        cookies = worker.login(driver,account_dict)
        return cookies


    def check_cookies(self,driver,worker,cookies):
        result = worker.check_cookies(driver,cookies)
        return result

    def save_cookies(self,cookies,account_dict,cookie_queue):
        """
        保存cookie到cookie池里面
        """
        try:
            self.db.put(account_dict['account'],data=cookies)
        except Exception as e:
            raise e

    def run(self,driver,worker,account_dict):
        cookies = self.cookie_login(driver,worker,account_dict)
        time.sleep(2)
        result = self.check_cookies(driver,worker,cookies)
        if result:
            self.save_cookies(cookies,account_dict,worker.cookie_queue)
        driver.quit()

if __name__ == '__main__':
    

    account_list = [
                    {'account':'Terry2','password':'Terry2'},
                    {'account':'csdc12','password':'csdc12'},
                    {'account':'pocd02','password':'pocd02'},
                    ]

    for account in account_list:
        driver = webdriver.Chrome('C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe')
        worker = ZJT_Login('https://member.zjtcn.com/common/login.html?url=https://xunjia.zjtcn.com/solved/0429_a广东_c广州市_p1_g_s_t_o1.html')
        login_process = LoginCore()
        try:
            login_process.run(driver,worker,account)
        except Exception as e:
            print("{} 登陆异常".format(account))
        
