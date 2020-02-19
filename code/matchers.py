import cv2
import numpy as np
import sys

class matchers:
	def __init__(self):
		self.orb = cv2.ORB_create()
		self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
		self.surf = cv2.xfeatures2d.SURF_create()
		FLANN_INDEX_KDTREE = 0  # FLANN 参数
		index_params = dict(algorithm=0, trees=5)
		search_params = dict(checks=50)
		self.flann = cv2.FlannBasedMatcher(index_params, search_params)

	def match(self, i1, i2, direction=None):
		# TODO 更新为ORB特征提取
		imageSet1 = self.getORBFeatures(i1)
		imageSet2 = self.getORBFeatures(i2)
		# imageSet1 = self.getSURFFeatures(i1)
		# imageSet2 = self.getSURFFeatures(i2)
		print("Direction : ", direction)
		matches = self.bf.knnMatch(
			imageSet2['des'],
			imageSet1['des'],
			k=2
			)
		good = []
		for i , (m, n) in enumerate(matches):
			if m.distance < 0.8*n.distance:
				good.append((m.trainIdx, m.queryIdx))

		if len(good) > 4:
			pointsCurrent = imageSet2['kp']
			pointsPrevious = imageSet1['kp']

			matchedPointsCurrent = np.float32(
				[pointsCurrent[i].pt for (__, i) in good]
			)
			matchedPointsPrev = np.float32(
				[pointsPrevious[i].pt for (i, __) in good]
				)

			H, s = cv2.findHomography(matchedPointsCurrent, matchedPointsPrev, cv2.RANSAC, 4)
			return H
		return None

	def getSURFFeatures(self, im):
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		kp, des = self.surf.detectAndCompute(gray, None)
		return {'kp':kp, 'des':des}

	def getORBFeatures(self,im):
		kp ,des = self.orb.detectAndCompute(im, None)
		return {'kp': kp, 'des': des}

class ORB_Matcher:
	def __init__(self):
		self.orb = cv2.ORB_create()
		self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

	def match(self,i1,i2):
		# 在matcher中做到两个不同场景的图可以没有交叉或者很少
		# 这个相同场景的条件需要严格 这个matches的个数需要大于或等于5
		kp1, des1 = self.orb.detectAndCompute(i1, None)
		kp2, des2 = self.orb.detectAndCompute(i2, None)
		min_dist = sys.float_info.max
		knn_matches = self.bf.knnMatch(des1, des2, k=2)
		# matches = self.bf.match(des1, des2)
		for (d1,d2) in knn_matches:
			if d1.distance > 0.6*d2.distance:
				continue
			if d1.distance < min_dist:
				min_dist = d1.distance
		matches = []
		for (d1,d2) in knn_matches:
			if d1.distance > 0.6*d2.distance or d1.distance > 5*min(min_dist,10.0):
				continue
			matches.append(d1)
		return len(matches)>= 5
		# matches = sorted(matches, key=lambda x: x.distance)
		# # 通过两个knn来消除误判的点
		# img3 = cv2.drawMatches(i1, kp1, i2, kp2, matches[:80], i2, flags=2)
		# cv2.imshow('right', img3)
		# cv2.waitKey()

