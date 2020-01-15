from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
import time
#造价通账号 一个月
#15527927113
#123456qq

class ZJT_Login:
    cookie_queue = 'wangban:zjt_xunjia:cookie_queue'
    def __init__(self,login_url):
        self.login_url = login_url


    def login(self,driver,account_dict):
        driver.get(self.login_url)
        time.sleep(2)
        driver.find_element_by_xpath('//ul[@class="login-tab-deition"]/li[@class="border_l cur"]').click()
        driver.find_element_by_id('memberID').send_keys(account_dict.get('account'))
        time.sleep(1)
        driver.find_element_by_id('pwd').send_keys(account_dict.get('password'))
        time.sleep(1)
        self.deal_captcha(driver)
        driver.find_element_by_xpath('//div[@class="bluebtn"]/a').click()
        time.sleep(3)
        try:
            driver.find_element_by_xpath('//div[@class="pop-jc-kuang clearfix"]//a[@class="pop-jc-btn-close"]').click()
        except Exception as e:
            pass
        
        time.sleep(1)
        driver.get('https://xunjia.zjtcn.com/solved/0429_a%E5%B9%BF%E4%B8%9C_c%E5%B9%BF%E5%B7%9E%E5%B8%82_p1_g_s_t_o1.html')
        time.sleep(2)


        cookies = driver.get_cookies()

        return cookies

    def deal_captcha(self,driver):
        div = driver.find_element_by_xpath('//div[@class="ui-slider-btn init ui-slider-no-select"]')
        ActionChains(driver).click_and_hold(on_element=div).perform()
        time.sleep(0.15)
        ActionChains(driver).move_to_element_with_offset(to_element=div, xoffset=30, yoffset=10).perform()
        time.sleep(1)
        ActionChains(driver).move_to_element_with_offset(to_element=div, xoffset=100, yoffset=200).perform()
        time.sleep(0.5)
        ActionChains(driver).move_to_element_with_offset(to_element=div, xoffset=400, yoffset=300).release().perform()
        time.sleep(2)

    def check_cookies(self,driver,cookies):
        return True
        #try:
        #    elem = driver.find_element_by_xpath('//div[@id="unLogin"]//a[@class="header-login"]')
        #except Exception as e:
        #    pass 
        #else:
        #    raise LoginException
        
