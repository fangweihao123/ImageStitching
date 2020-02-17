import os
import re
import cv2
from matchers import matchers,ORB_Matcher
from utils import getFatherIndex

class Classifier:
    def __init__(self,img_folder):
        # 需要跳过其他文件夹和其他类型的文件 目前就jpg jpeg png三种格式把
        # 这里用orb特征子来做把
        self.real_img = []
        for file_name in os.listdir(img_folder):
            type = file_name.split('.')[-1]
            if type == 'jpg' or type=='jpeg' or type=='png':
                self.real_img.append((img_folder + '/' + file_name))
        self.solo_img = []
        self.img_set = []
        self.images = [cv2.resize(cv2.imread(each), (480, 320)) for each in self.real_img]
        self.orb_match = ORB_Matcher()

    def classify(self):
        union = []
        tmp_result = []
        for i in range(len(self.images)):
            union.append(i)
            tmp_result.append([])
        for i in range(len(self.images)):
            for j in range(i+1,len(self.images)):
                flag = self.orb_match.match(self.images[i],self.images[j])
                # false 为不同一组 接下来使用并查集进行
                if flag:
                    f1 = getFatherIndex(union,i)
                    f2 = getFatherIndex(union,j)
                    if f1!=f2:
                        union[f1] = f2
        for i in range(len(self.images)):
            tmp = getFatherIndex(union,i)
            tmp_result[tmp].append(self.real_img[i])
        for i in range(len(tmp_result)):
            l = len(tmp_result[i])
            if l==0:
                continue
            elif l==1:
                self.solo_img.extend(tmp_result[i])
            else:
                self.img_set.append(tmp_result[i])

    def getSoloImg(self):
        #返回完整路径
        return self.solo_img

    def getImageSet(self):
        return self.img_set