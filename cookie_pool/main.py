# -*- coding: utf-8 -*-
from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
import time
from logining.zjt_login import ZJT_Login
from logining.loginning import LoginCore
from DB.DbClient import DbClient


#def main():
#    db = DbClient()
#    db.changeTable('useful_proxy')
#    #db.changeTable('useful_proxy')
#    db.put('127.0.5.1:6379',value=1)
#
#
if __name__ == '__main__':
    account_list = [

                    {'account':'Terry2','password':'Terry2'},
                    {'account':'csdc12','password':'csdc12'},
                    {'account':'pocd02','password':'pocd02'},
                    ]

    for account in account_list:
        driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe')
        worker = ZJT_Login('https://member.zjtcn.com/common/login.html?url=https://xunjia.zjtcn.com/solved/0429_a广东_c广州市_p1_g_s_t_o1.html')
        login_process = LoginCore()
        try:
            login_process.run(driver,worker,account)
        except Exception as e:
            print(e)
            print("{} 登陆异常".format(account))