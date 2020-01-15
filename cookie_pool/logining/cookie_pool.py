import __init__
import random
import json 
from wangban_utils.redis_util import get_redis_conn
import time
from datetime import datetime 
from cookie_pool.zjlogining import LoginCore
from selenium import webdriver 
import os

class CookieSchedule:
    def __init__(self):
        self.redis_conn = get_redis_conn()
        self.cookie_w_queue = SETTINGS['COOKIE_WORK']
        self.cookie_c_queue = SETTINGS['COOKIE_CHECK']
        self.cookie_batch_size = 6
        self.cookie_indexes = [0,1,2,3,4,5,6,7,8,9]
        self.remain_indexes = None
        self.random_indexes = None
        #self.get_ini_random_indexes()
        self.calib_time = datetime.today()
        self.interval = 180

    def log_process(self):
        driver = webdriver.Chrome(CHROME_PATH)
        login_process = LoginCore()
        login_process.run(driver)

    def get_from_redis(self,index):
        cookies = self.redis_conn.lindex(self.cookie_c_queue,index)
        return cookies

    def get_ini_random_indexes(self):
        self.random_indexes = random.sample(self.cookie_indexes,self.cookie_batch_size)
        self.remain_indexes = list(set(self.cookie_indexes) - set(self.random_indexes))
        #print('get_ini_random_indexes',self.random_indexes,self.remain_indexes)
        return self.random_indexes
    
    def init_cookies(self):
        random_indexes = self.get_ini_random_indexes()
        for index in random_indexes:
            cookies = self.get_from_redis(index)
            self.redis_conn.sadd(self.cookie_w_queue,cookies)

    def get_random_indexes(self):
        old_number = self.cookie_batch_size - len(self.remain_indexes)
        old_indexes = random.sample(self.random_indexes,old_number)
        self.random_indexes = []
        self.remain_indexes.extend(old_indexes)
        self.random_indexes.extend(self.remain_indexes)
        self.remain_indexes = list(set(self.cookie_indexes) - set(self.random_indexes))
        return self.random_indexes

    def work_cookies(self):
        pipe = self.redis_conn.pipeline(True)
        while True:
            try:
               pipe.watch(self.cookie_w_queue)
               pipe.multi()
               pipe.delete(self.cookie_w_queue)
               random_indexes = self.get_random_indexes()
               for index in random_indexes:
                   print('index',index)
                   cookies = self.get_from_redis(index)
                   pipe.sadd(self.cookie_w_queue,cookies)
               pipe.execute()
               #pipe.unwatch()
               break
            except Exception as e:
               print('work_cookies error',e)
        print('-------------------------------------------------')

    def run(self):
        while True:
            now_time = datetime.today()
            if (now_time - self.calib_time).total_seconds() > self.interval:
                self.work_cookies()
                self.calib_time = now_time
            time.sleep(18)

if __name__ == '__main__':
    cookie_handler = CookieSchedule()
    cookie_handler.log_process()
    cookie_handler.init_cookies()
    cookie_handler.run()

