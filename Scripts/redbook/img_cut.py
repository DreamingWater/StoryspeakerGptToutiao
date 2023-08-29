# Lenovo-"Xie Yan"
import math
import cv2


def img_cut_four(img_thre):
    height = img_thre.shape[0]
    width = img_thre.shape[1]
    cut_pic(im=img_thre[0:math.floor(height/2),0:math.floor(width/2)],index=11)
    cut_pic(im=img_thre[math.floor(height/2):height,0:math.floor(width/2)],index=12)
    cut_pic(im=img_thre[0:math.floor(height/2),math.floor(width/2):width],index=13)
    cut_pic(im=img_thre[math.floor(height/2):height,math.floor(width/2):width],index=14)

# 切割图片
def cut_pic(im,index):
    save_path_file = 'D:\\' + str(index) + ".png"
    cv2.imwrite(save_path_file, im)


orgimg = cv2.imread('D:\\' + '1.png')
img_cut_four(orgimg)

