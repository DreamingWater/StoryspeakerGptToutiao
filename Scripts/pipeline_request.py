from Scripts.verication.vercation_script import cut_the_verication, verication_ocr
from tts.TtsMaker_request import TtsMaker


def request_ttsmaker():
    ttsmaker = TtsMaker()
    vercation_code = request_verication(ttsmaker) # 获取验证码
    ttsmaker.set_input_captcha(vercation_code)
    ttsmaker.set_input_text('你好呀，我是无极剑圣。')
    res = ttsmaker.post_text()
    print('result:{}'.format(res))
# 获取验证码
def request_verication(ttsmaker):
    ttsmaker.request_page()
    cut_the_verication()
    result = verication_ocr()
    if result is not False:
        print('The code is {}'.format(result))
        return result
    else:
        request_verication(ttsmaker)


# Ttsmaker的网页来实现语音合成
def ttsmaker_process():
    request_ttsmaker()



