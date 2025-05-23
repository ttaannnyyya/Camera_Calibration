# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18azZVgf2W1Krz3KENOJOcKwBkuGLKBKM
"""

import cv2
import numpy as np
import urllib.request
import matplotlib.pyplot as plt

# Download image
url = 'https://raw.githubusercontent.com/opencv/opencv/master/samples/data/left01.jpg'
file = 'left01.jpg'
urllib.request.urlretrieve(url, file)

# Chessboard settings
dims = (9, 6)
square_size = 1.0

# Prepare object points
obj_pts = np.zeros((dims[1] * dims[0], 3), np.float32)
obj_pts[:, :2] = np.indices(dims).T.reshape(-1, 2)
obj_pts *= square_size

# Load image
img = cv2.imread(file)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find chessboard corners
found, corners = cv2.findChessboardCorners(gray, dims, None)
if found:
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    refined_corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
else:
    raise ValueError("Chessboard corners not found")

# Camera calibration
obj_pts_list = [obj_pts]
img_pts_list = [refined_corners]
_, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_pts_list, img_pts_list, gray.shape[::-1], None, None)

#  Visualize the reprojected points
img_reproj = cv2.drawChessboardCorners(img.copy(), chessboard_size, img_points2, True)
plt.figure(figsize=(8, 6))
plt.imshow(cv2.cvtColor(img_reproj, cv2.COLOR_BGR2RGB))
plt.title('Reprojected Corners')
plt.axis('off')
plt.show()

# Print intrinsic matrix and distortion coefficients
print("Intrinsic Matrix:\n", K)
print("\nDistortion Coefficients:\n", dist.ravel())

# Extrinsic parameters
for i, (rvec, tvec) in enumerate(zip(rvecs, tvecs)):
    R, _ = cv2.Rodrigues(rvec)
    print(f"\nRotation Matrix for Image {i+1}:\n{R}")
    print(f"Translation Vector for Image {i+1}:\n{tvec}")
    ext_matrix = np.hstack((R, tvec))
    print(f"Extrinsic Matrix for Image {i+1}:\n{ext_matrix}")