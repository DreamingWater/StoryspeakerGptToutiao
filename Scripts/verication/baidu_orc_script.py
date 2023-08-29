# Lenovo - "Xie Yan"
import base64
import urllib
import requests
import json


# 解析百度orc的result得到最后的数据
def get_the_result(res_dict):
    res_dict = json.loads(res_dict)
    useful = res_dict['words_result_num']
    # print('using:{}'.format(useful))
    if not useful == 1 or useful == '1':
        return False
    words_result = res_dict['words_result'][0]
    print('word_result:{}'.format(words_result))
    return words_result['words']


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    from decouple import config
    API_KEY = config('API_KEY')
    SECRET_KEY = config('SECRET_KEY')
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


# 百度OCR的识别接口
def baidu_literature_ocr(pic_location):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting?access_token=" + get_access_token()

    # image 可以通过 get_file_content_as_base64("C:\fakepath\_1.jpg",True) 方法获取
    payload = 'image=' + get_file_content_as_base64(pic_location, True)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.text
    result = get_the_result(result)
    if result == False:
        return False
    elif result.isdigit():
        return result
    else:
        return False
