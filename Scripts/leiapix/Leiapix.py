import json
import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from PIL import Image
import requests
from selenium.webdriver.support.select import Select
# from lxml import etree
import re
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver.support.select import Select
from decouple import config
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

from decouple import config

LEIA_DIR = '/Scripts/leiapix//'


class LeiaPixObject(object):
    def __init__(self):
        self.url = 'https://convert.leiapix.com/'
        self.this_contents = ""
        path = Service(r'./Scripts/leiapix/MicrosoftWebDriver.exe')
        edge_options = webdriver.EdgeOptions()
        edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        edge_options.add_argument('ignore-certificate-errors')
        self.browser = webdriver.Edge(service=path,options=edge_options)
        self.wait = WebDriverWait(self.browser, 10)
        self.index = 0  # 用于记录多少次成功请求

    def read_cookies(self):
        self.browser.delete_all_cookies()
        # if os.path.exists(LEIA_DIR + 'cookies.txt'):
        #     with open('cookies.txt', 'r') as f:
        #         # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        #         cookies_list = json.load(f)
        #         for cookie in cookies_list:
        #             self.browser.add_cookie(cookie)

    def write_cookies(self):
        # self.browser.delete_all_cookies()
        with open('cookies.txt', 'w') as f:
            f.write(json.dumps(self.browser.get_cookies()))

    # xpath 判断元素是否加载完毕
    def wait_xpath(self, xpath_pattern):
        element = (By.XPATH, xpath_pattern)
        self.wait.until(EC.presence_of_element_located(element))

    # login in
    def login(self):
        self.read_cookies()

        self.wait_xpath('//button[@type="submit"]')
        # 找到输入框
        user_input = self.browser.find_element(by=By.XPATH, value='//input[@type="text"]')  # user name
        pw_input = self.browser.find_element(by=By.XPATH, value='//input[@type="password"]')  # password
        login_btn = self.browser.find_element(by=By.XPATH, value='//button[@type="submit"]')  # sumbit button
        # 输入用户名和密码，点击登录
        login_user = config('LEIA_USER')
        login_password = config('LEIA_PASSWORD')
        user_input.send_keys(login_user)
        pw_input.send_keys(login_password)
        login_btn.click()

    # 这部分包括 cookie 处理 和 密码登录
    def login_or_cookie(self):
        self.browser.get(self.url)
        self.wait_xpath('//label[@for="file-input"]')
        try:
            login_button = self.browser.find_element(By.XPATH, '//button[@class="login-button ng-scope"]')
            self.browser.execute_script("arguments[0].click();", login_button)
            self.login()
            print('login sucess')
            self.write_cookies()
            self.wait_xpath('//label[@for="file-input"]')
        except Exception as e:
            print('Use cookie success')

    def upload_file(self):
        self.wait_xpath('//label[@for="file-input"]')  # 文件上传的按钮
        file_input = self.browser.find_element(By.XPATH, '//label[@for="file-input"]')
        self.browser.execute_script("arguments[0].click();", file_input)

    def debug_stop(self):
        while 1:
            pass


def main():
    leia_pix = LeiaPixObject()
    leia_pix.login_or_cookie()


if __name__ == '__main__':
    main()
    # print(get_the_result())
