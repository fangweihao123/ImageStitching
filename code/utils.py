import cv2
import numpy as np
def getFatherIndex(union,index):
    if union[index] == index:
        return index
    else:
        return getFatherIndex(union,union[index])
# 统一图像大小，保证多尺度融合时不出错
def resize(size_A, size_B, padding):
    a, b = size_A
    c, d = size_B
    if a >= c:
        max_x = a
    else:
        max_x = c
    if b >= d:
        max_y = b
    else:
        max_y = d
    img_y = 2 * max_y - padding
    while (img_y % 16 != 0):
        max_y = max_y + 1
        img_y = 2 * (max_y) - padding
        #print(img_y, max_y)
    img_x = max_x
    while (img_x % 16 != 0):
        img_x = img_x + 1
    return (img_x, max_y)


# 补全图像大小
def img_padding(img, std_size, padding, bi='left'):
    # value=[0,0,0]
    w, h = img.shape[:2]
    std_w, std_h = std_size[:2]
    #print('std size:', std_w, std_h)
    bottom = std_w - w  # 底部距离
    horizontal = std_h - h  # 水平距离
    #print('distance:', bottom, horizontal)
    new_img = np.zeros((std_w, std_h + padding, 3), np.uint8)
    #print(new_img.shape, img.shape)
    if bi == 'left':
        new_img[0:w, horizontal + padding:, :] = img
        # constant = cv2.copyMakeBorder(img,0, bottom,horizontal,0 ,cv2.BORDER_CONSTANT,value)
    else:
        new_img[0:w, 0:h, :] = img
        # constant = cv2.copyMakeBorder(img, 0, bottom, 0,horizontal, cv2.BORDER_CONSTANT, value)
    return new_img
"""
approx,计算边界点（正常情况下得到4个顶点，但是由于拼接不是完全规则矩形，也会得到大于4个的点）
需要配合check_border 返回4个顶点坐标
"""
def approx(img):
    #img = cv2.imread(image_path, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    # 图片轮廓
    try:
        contours, hierarchy = cv2.findContours(thresh, 2, 1)
    # opencv4.11 返回两个参数,opencv3返回三个参数   img,contours, hierarchy = cv2.findContours(thresh, 2, 1) 
    except:
        img,contours, hierarchy = cv2.findContours(thresh, 2, 1)
    cnt = contours[0]
    # 寻找凸包并绘制凸包（轮廓）
    #hull = cv2.convexHull(cnt)
    #print(hull)
    approx = cv2.approxPolyDP(cnt, 50, True)
    return approx

def check_border(points):
    x=[]
    y=[]
    out_x =[]
    out_y =[]
    for point in points:
        x.append(point[0][0])
        y.append(point[0][1])
        #print(point[0][0],point[0][1])
    if len(x)<4:
        import sys
        print('there some error')
        sys.exit()
    elif len(x)>4:
        print('there are more than 4 points')
        out_x.extend(x[:2])
        out_x.extend(x[-2:])
        out_y.extend(y[:2])
        out_y.extend(y[-2:])
    else:
        out_x=x
        out_y=y
    out_x.sort()
    out_y.sort()
    return out_x,out_y
# 曝光补偿，计算重叠部分光场差，得到光场差系数
def xi(A,B):
    w,h = A.shape[:2]
    va = 0
    vb = 0
    for i in range(w):
        for j in range(h):
            Ia = 0.59 * A[i,j,0] + 0.11 * A[i,j,1] + 0.3*A[i,j,2]
            Ib = 0.59 * B[i, j, 0] + 0.11 * B[i, j, 1] + 0.3 * B[i, j, 2]
            va = va+Ia
            vb = vb+Ib
    k = vb/va
    return k
#补光
def Recorver(A,k):
    w, h = A.shape[:2]
    re_a= np.zeros((w,h,3),np.uint8)
    for i in range(w):
        for j in range(h):
            re_a[i, j, 0] = 255 if k * A[i, j, 0] > 255 else int(k*A[i,j,0])
            re_a[i, j, 1] = 255 if k * A[i, j, 1] > 255 else int(k*A[i,j,1])
            re_a[i, j, 2] = 255 if k * A[i, j, 2] > 255 else int(k*A[i,j,2])
            
    return re_a
