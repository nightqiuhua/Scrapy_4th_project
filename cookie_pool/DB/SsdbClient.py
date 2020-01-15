# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     SsdbClient.py
   Description :  封装SSDB操作
   Author :       JHao
   date：          2016/12/2
-------------------------------------------------
   Change Activity:
                   2016/12/2:
                   2017/09/22: PY3中 redis-py返回的数据是bytes型
                
-------------------------------------------------
"""
__author__ = 'JHao'

from Config.setting import PY3
import json
from redis.connection import BlockingConnectionPool
from redis import Redis


class SsdbClient(object):
    """
    SSDB client

    SSDB中代理存放的结构为hash：
        原始cookie存放在name为raw_cookie的hash中, key为账号的acount_name 用户名, value为cookie属性的字典;
        验证后的cookie存放在name为useful_cookie的hash中, key为cookie的acount_name 用户名, value为cookie属性的字典;

    """
    def __init__(self, name, **kwargs):
        """
        init
        :param name: hash name
        :param host: host
        :param port: port
        :param password: password
        :return:
        """
        self.name = name
        self.__conn = Redis(connection_pool=BlockingConnectionPool(**kwargs))

    def get(self, acount_name):
        """
        从hash中获取对应的cookie, 使用前需要调用changeTable()
        :param proxy_str: proxy str
        :return:
        """
        data = self.__conn.hget(name=self.name, key=acount_name)
        if data:
            return data.decode('utf-8') if PY3 else data
        else:
            return None

    def put(self, acount_name,**kwargs):
        """
        将代理放入hash, 使用changeTable指定hash name
        :param proxy_str 'ip:port' ; info_json dict 默认值 None 
        :return:
        """
        if not len(kwargs):
            info_json = {}
        else:
            info_json = json.dumps(kwargs)
        data = self.__conn.hset(self.name, acount_name, info_json)
        return data

    def delete(self, acount_name):
        """
        移除指定代理, 使用changeTable指定hash name
        :param proxy_str: proxy str
        :return:
        """
        self.__conn.hdel(self.name, acount_name)

    def exists(self, acount_name):
        """
        判断指定代理是否存在, 使用changeTable指定hash name
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hexists(self.name, acount_name)

    def update(self,  acount_name,**kwargs):
        """
        更新 proxy 属性
        :param proxy_str 'ip:port' ; info_json dict 默认值 None 
        :return:
        """
        if not len(kwargs):
            info_json = {}
        else:
            info_json = json.dumps(kwargs)
        self.__conn.hset(self.name, acount_name, info_json)

    def pop(self):
        """
        弹出一个代理
        :return: dict {proxy: value}
        """
        # proxies = self.__conn.hkeys(self.name)
        # if proxies:
        #     proxy = random.choice(proxies)
        #     value = self.__conn.hget(self.name, proxy)
        #     self.delete(proxy)
        #     return {'proxy': proxy.decode('utf-8') if PY3 else proxy,
        #             'value': value.decode('utf-8') if PY3 and value else value}
        return None

    def getAll(self):
        """
        列表形式返回所有代理, 使用changeTable指定hash name
        :return:
        """
        item_dict = self.__conn.hgetall(self.name)
        if PY3:
            return [value.decode('utf8') for key, value in item_dict.items()]
        else:
            return item_dict.values()

    def clear(self):
        """
        清空所有代理, 使用changeTable指定hash name
        :return:
        """
        return self.__conn.execute_command("hclear", self.name)

    def getNumber(self):
        """
        返回代理数量
        :return:
        """
        return self.__conn.hlen(self.name)

    def changeTable(self, name):
        """
        切换操作对象
        :param name: raw_cookie/useful_cookie
        :return:
        """
        self.name = name
