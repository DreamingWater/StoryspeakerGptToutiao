# Lenovo-"Xie Yan"

import base64
import os
import re
from io import BytesIO
from PIL import Image

from Scripts.verication.vercation_script import VericaitonReadDir


def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img


this_js = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
     "let img =  document.getElementsByClassName('sc-cSHVUG kckaJv'); /*找到图片*/ " \
     "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
     "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
     "let base64String = c.toDataURL();return base64String;"

def canvas_save_img(driver):
    base64_str = driver.execute_script(this_js)
    img = base64_to_image(base64_str)
    im = img.convert('RGB')
    img_dir = '' + '1.jpg'
    im.save(img_dir)