# coding:utf-8
import os
from chars import chars
from PIL import Image as image

#灰度处理
def covergrey(img):
    return img.convert('L')

#去除干扰线并转换为黑白照片
def clearline(img):
    for y in range(img.size[1]):
        for x  in range(img.size[0]):
            if int(img.getpixel((x,y)))>=110:
                img.putpixel((x,y),0xff)
            else:
                img.putpixel((x,y),0x0)
    return img

#验证码识别
def identify(data):
	code=['']*4
	diff_min=[432]*4
	for char in chars:
		diff = [0]*4
		for i in range(4):
			for j in range(432):#逐个像素比较验证码特征
				if data[i][j] != chars[char][j]:
					diff[i] += 1
		for i in range(4):
			if diff[i]<diff_min[i]:
				diff_min[i]=diff[i]
				code[i]=char
	return ''.join(code)

#去噪/pnum-去噪效率
def del_noise(im, pnum = 3):
    w, h = im.size
    white = 255
    black = 0
    for i in range(0, w):
        im.putpixel((i, 0), white)
        im.putpixel((i, h - 1), white)
    for i in range(0, h):
        im.putpixel((0, i), white)
        im.putpixel((w - 1, i), white)
    for i in range(1, w - 1):
        for j in range(1, h - 1):
            val = im.getpixel((i, j))
            # 黑色的情况
            if val == black:
                cnt = 0
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        if im.getpixel((i + ii, j + jj)) == black:
                            cnt += 1
                if cnt < pnum:
                    im.putpixel((i, j), white)
            else:
                cnt = 0
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        if im.getpixel((i + ii, j + jj)) == black:
                            cnt += 1
                if cnt >= 7:
                    im.putpixel((i, j), black)
    return im

#图片数据二值化
def two_value(code_data):
	table = []
	for i in code_data:
		if i < 140:#二值化分界线140
			table.append(0)
		else:
			table.append(1)
	return table

#图片预处理
def pre_img(path):
    img = image.open(path)
    img = covergrey(img)#去色
    img = clearline(img)#去线
    img = del_noise(img)#去噪
    return img

#处理图片数据
def data_img(img):
    code_data=[]#验证码数据列表
    for i in range (4):#切割验证码
        x = 5 + i * 18  # 见原理图
        code_data.append(img.crop((x, 9, x + 18, 33)).getdata())
        code_data[i]=two_value(code_data[i])#二值化数据
    return code_data

#主程序开始
path = 'code.jpg'#获取图片地址
img = pre_img(path)#预处理图片
data = data_img(img)#获取图片数据
code = identify(data)#识别验证码
print('识别结果-->'+str(code))

