# Lenovo-"Xie Yan"
from Scripts.tts.TtsMaker import TtsMakerObject

# Ttsmaker的网页来实现语音合成
def ttsmaker_process():
    ttsmaker = TtsMakerObject()
    ttsmaker.request_ttsmaker()
    text = '''
    2000年出生的黄琴是重庆人
    一年多前来到浙江桐乡工作
    虽然辛苦，但能为家里减轻负担
    还能补贴弟弟上学所需
    她觉得很有成就感
    你好呀((⏱️=200))超级人物
    '''
    ttsmaker.enable_once_change(text)
