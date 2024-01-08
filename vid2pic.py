#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File    :   vid2pic.py
# @Created :   2024/01/07 21:25:08
# @Software:   Vscode
# @Version :   1.85
# @Author  :   Joy Zhu 
# @Contact :   z1531610120@outlook.com
# @Desc    :   数据集制作1：视频转为图片
# -------------------------------------------------------------------------------


import os
import sys
import cv2 as cv
import datetime




def cmpHash(hash1, hash2):
    n = 0
    if len(hash1) != len(hash2):
        return -1
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    return n
 
# 差值哈希
def dHash(img):
    img = cv.resize(img, (9, 8))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    hash_str = ''
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j+1]:
                hash_str = hash_str+'1'
            else:
                hash_str = hash_str+'0'
 
    return hash_str


def vid2pic(input_path,output_path):

    img_fream = 50
    c = 0
    img_dif = 20        # 哈希差值<20,视为相似，去除
    previous_image = None
    current_image = None

    cap = cv.VideoCapture(input_path)
    isOpened = cap.isOpened()
    if(isOpened==True):
        FrameNumber = int(cap.get(7))
        FPS = int(cap.get(5))
        print("总帧数：%d, 帧率：%d" % (FrameNumber,FPS))
    else:
        print('cannot open vides!')


    while(True):
        flag, frame = cap.read()
        if flag:
            if(c % img_fream == 0):
                if previous_image is None:
                    previous_image = frame
                    imgName = '%03d'%c +'.jpg'
                    cv.imwrite(output_path+imgName,frame)
                    print(imgName)
                else:
                    current_image = frame
                    hash1 = dHash(previous_image)
                    hash2 = dHash(current_image)
                    similarity = cmpHash(hash1,hash2)
                    print ("相似度为%d" %similarity)

                    if similarity >= img_dif :
                        previous_image = current_image
                        imgName = '%03d'%c +'.jpg'
                        cv.imwrite(output_path+imgName,frame)
                        print(imgName)
            c += 1
            cv.waitKey(1)
        else:
            break

    cap.release()
    print('vid2img end')


class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a",encoding="utf-8")
 
    def write(self, message):
        self.log.write(message)
        self.terminal.write(message)
        self.log.flush()    #缓冲区的内容及时更新到log文件中
    
    def flush(self):
        pass

sys.stdout = Logger("G:/TITLE 001/code/log.txt")
 

if __name__ == '__main__':

    videos_folder = 'G:/TITLE 001/videos/'
    images_folder = 'G:/TITLE 001/images/'

    video_list = os.listdir(videos_folder)
    i=0
    for vid_name in video_list:
        i+=1
        input_path = videos_folder + vid_name
        output_path = images_folder + vid_name[:-4] +'/'
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("*********************第%d个视频*********************" % i)
        print('time: %s  output_path: %s' % (time,output_path))
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        vid2pic(input_path, output_path)
    



