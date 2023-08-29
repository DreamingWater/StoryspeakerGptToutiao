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

from Scripts.verication.canvas_img import canvas_save_img
from Scripts.verication.common import option_select, download_mp3
from Scripts.verication.vercation_src import get_uuid_from_img
from Scripts.verication.vercation_script import VericaitonReadDir, cut_the_verication, verication_ocr
from Scripts.verication.vercation_src import get_uuid_from_img

list_course = []

SPEED_LIST = [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 1.0, 1.1, 1.15, 1.2, 1.3, 1.4, 1.5, 2.0]
Volume_LIST = [1.0, 1.1, 1.2, 1.5, 1.6, 1.8, 2.0]
Pause_Time = [300, 600, 800, 1000, 1200, 1500, 1800, 2000, 3000, 5000]


class TtsMakerObject(object):
    def __init__(self):
        self.base_url = 'https://ttsmaker.com'
        self.url = 'https://ttsmaker.com/zh-cn'
        self.this_contents = ""
        path = r"/Scripts/tts/MicrosoftWebDriver.exe"
        self.browser = webdriver.Edge(path)
        self.wait = WebDriverWait(self.browser, 10)
        self.index = 0  # 用于记录多少次成功请求

    def read_cookies(self):
        self.browser.delete_all_cookies()
        if os.path.exists('cookies.txt'):
            with open('cookies.txt', 'r') as f:
                # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
                cookies_list = json.load(f)
                for cookie in cookies_list:
                    self.browser.add_cookie(cookie)

    def write_cookies(self):
        # self.browser.delete_all_cookies()
        with open('cookies.txt', 'w') as f:
            # 将cookies保存为json格式
            f.write(json.dumps(self.browser.get_cookies()))

    def request_ttsmaker(self):
        self.browser.get(self.url)  # 浏览器请求url

    # xpath 判断元素是否加载完毕
    def wait_xpath(self, xpath_pattern):
        element = (By.XPATH, xpath_pattern)
        self.wait.until(EC.presence_of_element_located(element))

    # 识别验证码，如果识别失败，就刷新验证码
    def verification_code(self):
        self.wait_xpath('//*[@id="VerifyCaptchaIMG"]')
        self.request_img()
        res = self.verication_ocr()
        if res is False:
            self.change_verication_code()
            self.verification_code()
        return res

    # 下载验证码，用于图像处理
    def request_img(self):
        canvas_save_img(self.browser)

    # 验证码本地识别
    def verication_ocr(self):
        cut_the_verication()
        result = verication_ocr()
        if result is not False:
            print('The code is {}'.format(result))
            return result
        else:
            return False  # 此验证码识别不出来，换一张

    # 换一张验证码
    def change_verication_code(self):
        a = self.browser.find_element(By.ID, 'reVerify')
        self.browser.execute_script("arguments[0].click();", a)

    # 输入验证码
    def set_verication_code(self, code):
        captcha = self.browser.find_element(By.ID, 'UserInputCaptcha')  # 获取captcha输入框
        captcha.send_keys(code)

    # 输入要转换的文本
    def set_voice_text(self, text):
        self.wait_xpath('//*[@id="UserInputTextarea"]')
        textarea = self.browser.find_element(By.ID, 'UserInputTextarea')  # 获取文本输入框
        textarea.send_keys(text)

    # submit the change
    def submit_change(self):
        a = self.browser.find_element(By.ID, 'tts_order_submit')
        self.browser.execute_script("arguments[0].click();", a)

    # advance setting click
    def advance_click(self):
        a = self.browser.find_element(By.ID, 'tts_order_more_setting')
        self.browser.execute_script("arguments[0].click();", a)

    # change the change voice
    def set_voice_user(self):
        a = self.browser.find_element(By.ID, 'RadioUserSelectAnnouncerID1501')
        self.browser.execute_script("arguments[0].click();", a)

    # set the speed
    def set_speed(self, speed):
        option_select(self.browser, 'userSelectTTSSettingSpeed', speed, SPEED_LIST)

    # set the speed
    def set_volume(self, volume):
        option_select(self.browser, 'userSelectTTSSettingVolume', volume, Volume_LIST)

    # set_pause_time
    def set_pause_time(self, pause_time):
        option_select(self.browser, 'userSelectTTSParagraphPauseTime', pause_time, Pause_Time)

    # advance setting
    def advance_setting(self, speed=1.0, volume=1.0, pause_time=300):
        self.advance_click()
        self.set_speed(speed)
        self.set_volume(volume)
        self.set_pause_time(pause_time)

    # download the mp3 file based on the url
    def get_download_mp3_url(self):
        mp3_id = self.browser.find_element(By.ID, 'tts_mp3_download_address_code')
        mp3_url = mp3_id.text
        res = download_mp3(mp3_url, file_name=str(self.index))
        if res:
            self.index += 1

    def deal_toast_button(self,voice_text):
        self.wait_xpath('//div[@class="toast-message"]')
        toast_message = self.browser.find_element(By.CLASS_NAME, 'toast-message')
        text = toast_message.text
        # The verification code is incorrect. Refresh it and try again
        # Please enter the verification code
        # Conversion success is playing voice content for you
        if 'success' in text:  # 转换成功
            self.get_download_mp3_url()
        else:  # 验证码错误
            print('the toast answer is %s' % text)
            self.browser.refresh()
            self.enable_once_change(voice_text)

    # 启动一次流程 toast-container
    def enable_once_change(self, voice_text):
        captcha = self.verification_code()  # 获取验证码
        self.set_verication_code(captcha)      # 填写验证码
        self.set_voice_text(voice_text)  # 设置文本
        self.set_voice_user()  # 设置说话人
        self.advance_setting()  # 高级设置
        self.submit_change()  # 提交一次
        self.deal_toast_button(voice_text)  # 处理button结果
        # self.debug_stop()

    def debug_stop(self):
        while 1:
            pass
