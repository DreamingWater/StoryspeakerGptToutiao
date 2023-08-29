# 导入requests和BeautifulSoup库
import requests
from lxml import etree

from Scripts.verication.vercation_script import VericaitonReadDir
from Scripts.verication.vercation_src import get_uuid_from_img


class TtsMaker:
    def __init__(self):
        self.base_url = 'https://ttsmaker.com'
        self.url = 'https://ttsmaker.com/zh-cn'
        self.this_contents = ""
        # self.session = requests.session()
        self.index = 1
        self.post_data = {
            "user_uuid_text": "",
            "user_input_text": "",
            "user_select_language_id": "zh-cn",  # 中文
            "user_select_announcer_id": "203",  # 说话人
            "user_select_tts_setting_audio_format": "mp3",  # 输出格式
            "user_select_tts_setting_speed": "1.0",  # 语速
            "user_select_tts_setting_volume": "1",  # tts_setting_volume
            "user_input_captcha_text": "",  # 验证码
            "user_input_paragraph_pause_time": "0"  # 句子与句子之间的间隙
        }

    # 填充验证码
    def set_input_captcha(self, code):
        self.post_data['user_input_captcha_text'] = code

    # 设置文字
    def set_input_text(self, text):
        self.post_data['user_input_text'] = text

    def request_page(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

        response = requests.get(self.url, headers=headers)
        html = etree.HTML(response.content)
        self.verification_code(html)
        # print(response.content)

    def verification_code(self, html):
        code_img_src = html.xpath('//*[@id="VerifyCaptchaIMG"]/@src')[0]
        print(self.base_url + code_img_src)
        uuid = get_uuid_from_img(code_img_src)
        if uuid:
            self.post_data['user_uuid_text'] = uuid
        else:
            # self.request_img() #重新发出请求
            pass
        self.request_img(self.base_url + code_img_src)

    def request_img(self, img_url):
        img_bytes = requests.get(img_url)
        base_dir = VericaitonReadDir
        with open(base_dir + '1.jpg', 'wb') as f:
            f.write(img_bytes.content)

    def post_text(self):
        tts_url = 'https://ttsmaker.com/api/create-tts-order'
        from fake_useragent import UserAgent
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        requests.post(tts_url, data=self.post_data, headers=headers, timeout=100)
    # def cookie_deal(self):
    #     headers = {
    #         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    #     # 开启一个session会话
    #     session = self.session
    #     # 设置请求头信息
    #     session.headers = headers
    #
    #     res = session.get(self.base_url)
    #     # 申明一个用于存储手动cookies的字典
    #     manual_cookies = {}
    #     # 将CookieJar转为字典：
    #     print(res.cookies)
    #     res_cookies_dic = requests.utils.dict_from_cookiejar(res.cookies)
    #     print(res_cookies_dic)
    #     # 将新的cookies信息更新到手动cookies字典
    #     for k in res_cookies_dic.keys():
    #         manual_cookies[k] = res_cookies_dic[k]
    #
    #     # 重新将新的cookies信息写回文本
    #     res_manual_cookies_txt = ""
    #
    #     # 将更新后的cookies写入到文本
    #     for k in manual_cookies.keys():
    #         res_manual_cookies_txt += k + "=" + manual_cookies[k] + ";"
    #
    #     # 将新的cookies写入到文本中更新原来的cookies
    #     with open('manual_cookies.txt', "w", encoding="utf-8") as fwcookie:
    #         fwcookie.write(res_manual_cookies_txt)
    #     return res

'''
{
    "status": 200,
    "post_data": {
        "user_uuid_text": "7bc89a63-9369-4a89-a3f0-041eb2d09c0f",
        "user_input_text": "你好呀，我",
        "user_select_language_id": "zh-cn",
        "user_select_announcer_id": "999",
        "user_select_tts_setting_audio_format": "mp3",
        "user_select_tts_setting_speed": "1.0",
        "user_select_tts_setting_volume": "0",
        "user_input_captcha_text": "0554",
        "user_input_paragraph_pause_time": "0"
    },
    "is_enable_user_limit_func": false,
    "public_ip": "",
    "user_tts_used_count": 0,
    "user_history_text_count": 0,
    "user_tts_available_count": 0,
    "user_next_reset_time": 0,
    "user_can_use_max_text_count": 0,
    "enable_user_limit_tts_tips_panel_text_count": 6000,
    "update_times": "2023-04-04 22:23:17",
    "website_name": "https://ttsmaker.com",
    "auto_base_url": "https://s3.ttsmaker.com/file/2023-04-04-222316_181438.mp3",
    "auto_stand_url": "https://s3.ttsmaker.com/file/2023-04-04-222316_181438.mp3",
    "errcode": 0,
    "errmsg": "success",
    "audio_format": "mp3"
}


'''