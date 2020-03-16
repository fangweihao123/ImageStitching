import numpy as np
import cv2
from matchers import matchers,ORB_Matcher
import time
from classifier import  Classifier
from blending import left_blending,right_blending

class Stitch:
    def __init__(self):
        self.matcher_obj = matchers()

    def set_image_list(self,img_list):
        self.images = [cv2.resize(cv2.imread(each),(480, 320)) for each in img_list]
        self.count = len(self.images)
        self.left_list, self.right_list, self.center_im = [], [],None
        self.prepare_lists()

    def prepare_lists(self):
        print("Number of images : %d"%self.count)
        self.centerIdx = self.count/2
        print("Center index image : %d"%self.centerIdx)
        self.center_im = self.images[int(self.centerIdx)]
        for i in range(self.count):
            if(i<=self.centerIdx):
                self.left_list.append(self.images[i])
            else:
                self.right_list.append(self.images[i])
        print("Image lists prepared")

    def leftshift(self):
        # self.left_list = reversed(self.left_list)
        a = self.left_list[0]
        for b in self.left_list[1:]:
            H = self.matcher_obj.match(a, b, 'left')
            print("Homography is : ", H)
            xh = np.linalg.inv(H)
            print("Inverse Homography :", xh)
            ds = np.dot(xh, np.array([a.shape[1], a.shape[0], 1]));
            ds = ds/ds[-1]
            print("final ds=>", ds)
            f1 = np.dot(xh, np.array([0,0,1]))
            f1 = f1/f1[-1]
            xh[0][-1] += abs(f1[0])
            xh[1][-1] += abs(f1[1])
            ds = np.dot(xh, np.array([a.shape[1], a.shape[0], 1]))
            offsety = abs(int(f1[1]))
            offsetx = abs(int(f1[0]))
            dsize = (int(ds[0])+offsetx, int(ds[1]) + offsety)
            print("image dsize =>", dsize)
            tmp = cv2.warpPerspective(a, xh, dsize)# 透视变换
            # cv2.imshow("warped", tmp)
            # cv2.waitKey()
            tmp = left_blending(tmp, b, offsetx, offsety)
            a = tmp

        self.leftImage = tmp
        return self.leftImage


    def rightshift(self):
        for each in self.right_list:
            H = self.matcher_obj.match(self.leftImage, each, 'right')
            print("Homography :", H)
            txyz = np.dot(H, np.array([each.shape[1], each.shape[0], 1]))
            txyz = txyz/txyz[-1]
            dsize = (int(txyz[0])+self.leftImage.shape[1], int(txyz[1])+self.leftImage.shape[0])
            tmp = cv2.warpPerspective(each, H, dsize)
            #cv2.imshow("tp", tmp)
            #cv2.waitKey()
            # tmp[:self.leftImage.shape[0], :self.leftImage.shape[1]]=self.leftImage
            tmp = self.mix_and_match(self.leftImage, tmp)
            print("tmp shape",tmp.shape)
            print("self.leftimage shape=", self.leftImage.shape)
            self.leftImage = tmp
        return self.leftImage


    def mix_and_match(self, leftImage, warpedImage):
        warpedImage = right_blending(leftImage, warpedImage)
        return warpedImage



if __name__ == '__main__':
    c = Classifier('./image')
    c.classify()
    re = c.getImageSet()
    s = Stitch()
    cnt = 0
    for each in re:
        s.set_image_list(each)
        left = s.leftshift()
        right = s.rightshift()
        cv2.imwrite(str(cnt) + '.jpg',right)
        cnt = cnt + 1
        cv2.imshow('right', right)
        print("image written")
        if cv2.waitKey(3000):
            cv2.destroyAllWindows()

