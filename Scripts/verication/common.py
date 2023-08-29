# Lenovo-"Xie Yan"
import requests
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

from Scripts.verication.vercation_script import OutputReadDir


# 选择 option 点击
def option_select(browser, element_id, value, _LIST):
    speed_index = _LIST.index(value)  # 将具体的速度值转化为对于的index
    select_speed = browser.find_element(By.ID, element_id)
    select_speed = Select(select_speed)
    select_speed.select_by_index(speed_index)


# 下载mp3文件
def download_mp3(url,file_name:str):
    down_res = requests.get(url)
    if not file_name.endswith('.mp3'):
        file_name += '.mp3'
    filename = OutputReadDir + file_name
    with open(filename, 'wb') as file:
        file.write(down_res.content)
        return True
    return False


# 删除存储文件夹下留存的文件
def remove_last_mp3():
    import os
    filelist = os.listdir(OutputReadDir)
    for file in filelist:
        if file.endswith('.mp3'):
            del_file = OutputReadDir + file  # 当代码和要删除的文件不在同一个文件夹时，必须使用绝对路径
            os.remove(del_file)  # 删除文件
    print('delete the last mp3 success!!!')
