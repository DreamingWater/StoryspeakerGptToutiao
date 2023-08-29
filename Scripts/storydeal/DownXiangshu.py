# 导入requests和BeautifulSoup库
import requests
from bs4 import BeautifulSoup
from lxml import etree


class DownXiangshu:
    def __init__(self):
        self.base_url = 'https://www.ibiquge.la/62/62561/'
        self.this_contents = ""

    # 25274611.html

    def down_one_page(self, page=25274611):

        response = requests.get(self.base_url + str(page) + '.html')
        html = etree.HTML(response.content)
        content_text = html.xpath('//div[@id="content"]/text()')
        # print(content_text)
        # print(''.join(content_text))
        for para_text in content_text:
            if not para_text.startswith('\r'):
                # print(para_text)
                self.this_contents += para_text.replace('\xa0', '').replace('\r', '')
        return self.this_contents

    def down_several_pages(self):
        down_text = ''
        for i in range(25274611, 25274611 + 15):
            down_text += self.down_one_page(i)
        return down_text

    # def clean_data(self, data:str):
    #     data = data.replace('')

