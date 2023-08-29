import cv2
import math
import ddddocr
import glob

from Scripts.verication.baidu_orc_script import baidu_literature_ocr

OutputReadDir = r'D:\Code\Python\GptTest\Output\\'
VericaitonReadDir = r'D:\Code\Python\GptTest\Output\VerificaionCode\\'
VericaitonSplitDir = VericaitonReadDir + 'split\\'

# 获取欲切割的边界
def img_boundary(img_thre):
    height = img_thre.shape[0]
    width = img_thre.shape[1]
    # print("height:{},width:{}".format(height, width))
    each_pic_width = math.floor(width / 4)
    each_pic_boundary = [i * each_pic_width for i in range(4)]
    each_pic_boundary.append(width)
    print(each_pic_boundary)
    return height, each_pic_boundary


# 切割图片
def cut_pic(img, hight, each_pic_boundary):
    for index in range(len(each_pic_boundary) - 1):
        im = img[0:hight, each_pic_boundary[index]:each_pic_boundary[index + 1]]
        save_path_file = VericaitonSplitDir+ str(index) + ".jpg"
        cv2.imwrite(save_path_file, im)


# 根据图片的区间划分范围，切割图片
def cut_the_verication():
    orgimg = cv2.imread(VericaitonReadDir + '1.jpg')
    height, each_pic_boundary = img_boundary(orgimg)
    cut_pic(orgimg, height, each_pic_boundary)


'''
    识别图片的部分
'''


# 对ddddocr识别结果进行修正，修正的原理是验证码全是数字。
def change_2_number(file,data):
    # 0
    if data.lower() == 'o':
        return 0
    elif data.lower() == 's':
        return None   # 又可以返回 8 也有可能是 9
    elif data.lower() == 'i' or data.lower() == 'l':
        return None
    elif data.lower() == 'z':
        return 2
    elif data.lower() == '牛':
        return 4
    elif data.isdigit():
        return int(data)
    else:
        print('there is an error in {}:{}'.format(file,data))
        return None


def verication_ocr():
    ocr = ddddocr.DdddOcr(show_ad=False)
    jpg_path = glob.glob(VericaitonSplitDir + '*.jpg')
    verication_result = ''
    for index, file in enumerate(jpg_path):
        with open(file, 'rb') as f:
            img_bytes = f.read()  # 通过ddddocr进行识别验证码
            res = ocr.classification(img_bytes)
            res = change_2_number(file.split('/')[-1], data=res)
            if res is None:
                res = baidu_literature_ocr(file)
                if res is not False:
                    verication_result += res
                else:
                    return False
            else:
                verication_result += str(res)
    return verication_result

