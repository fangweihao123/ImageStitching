import numpy as np
import cv2
import matplotlib.pyplot as plt
from multibending import multi_band_blending
from utils import resize,img_padding,approx,check_border,xi,Recorver


def left_blending(left_img,warped_img,disx,disy):

    points_left =approx(left_img)
    left_y,left_x =check_border(points_left)
    points_warped=approx(warped_img)
    warped_y, warped_x =check_border(points_warped)
    min_y_a =min(left_y)
    min_x_a =min(left_x)
    max_x_a =max(left_x)
    max_x =max(warped_x)
    max_y =max(warped_y)
    # 左图
    A = left_img[0:max_x_a,min_y_a:disx,:].copy()
    A0 = left_img[disy+200:disy+300,disx:disx+150,:] # 光照补偿块

    # 右图
    B = np.zeros((A.shape[0],max_y,3),np.uint8)
    B[disy:disy+max_x,0:max_y,:] = warped_img[0:max_x,0:max_y,:]

    # 右图
    B0 = B[disy+200:disy + 300, 0:150, :] # 光照补偿参照块

    k = xi(A0,B0)
    left_img = Recorver(left_img,k)
 
    #import sys
    #sys.exit()
    A_shape = A.shape[:2]
    B_shape = B.shape[:2]
    padding=8
    if padding%2!=0:
        padding=padding+1
    A1 = left_img[0:max_x_a, min_y_a:disx + 2*padding, :].copy()
    std_size = resize(A_shape, B_shape, padding*2)
    #print(std_size)  # 标准大小
    left_padding = img_padding(A1, std_size,padding, bi='left')
    right_padding = img_padding(B, std_size,padding, bi='right')

    #plt.imshow(left_padding)
    #plt.show()
    #plt.imshow(right_padding)
    #plt.show()
    result = multi_band_blending(left_padding, right_padding, padding*2, 3, False)
    #print(left_padding.shape,right_padding.shape,result.shape)
    #plt.imshow(result)
    #plt.show()

    re=left_padding.shape[1]-A.shape[1]
    result1=result[min_x_a:,re:,:].copy()

    return result1

def right_blending(left_img, warped_img):
    points_left = approx(left_img)
    left_y, left_x = check_border(points_left)
    points_warped = approx(warped_img)
    warped_y, warped_x = check_border(points_warped)
    min_y_a = min(left_y)
    max_x_a = max(left_x)
    max_x = max(warped_x)
    max_y = max(warped_y)
    padding = 32
    #print('x:',left_img.shape,min_y_a,warped_y[1])
    A = left_img[0:max_x_a, min_y_a:warped_y[1]+padding, :].copy()

    B = warped_img[0:max_x, warped_y[1]:max_y, :].copy()

    #print('A and B shape:', A.shape, B.shape)
    A_shape = A.shape[:2]
    B_shape = B.shape[:2]
    # 左图
    
    A0 = left_img[int(max_x_a/2):int(max_x_a/2)+150,warped_y[1]:warped_y[1]+200,:] # 光照补偿块

    B0 = B[int(max_x_a/2):int(max_x_a/2)+150, 0:200, :] # 光照补偿参照块
    k=xi(B0,A0)
    warped_img=Recorver(warped_img,k)

    if padding % 2 != 0:
        padding = padding + 1
    
    A1 = left_img[0:max_x_a, min_y_a:warped_y[1]+padding*2, :].copy()
    std_size = resize(A_shape, B_shape, padding * 2)
    #print('A1.shape:', A1.shape)

    #print(std_size)
    B = warped_img[0:max_x, warped_y[1]:max_y, :].copy()
    left_padding = img_padding(A1, std_size, padding, bi='left')
    right_padding = img_padding(B, std_size, padding, bi='right')

    #print(left_padding.shape, right_padding.shape)
    result = multi_band_blending(left_padding, right_padding, padding * 2, 3, False)
    #print(result.shape)
    re = left_padding.shape[1] - A.shape[1]
    result1 = result[:, re:, :].copy()
    # plt.imshow(result)
    # plt.show()
    return result
