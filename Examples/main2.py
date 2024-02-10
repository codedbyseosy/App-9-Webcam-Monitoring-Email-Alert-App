# To create an image
import numpy
import cv2

a = numpy.array(
[[[255, 0, 0],
  [255, 255, 255],
  [255, 255, 255],
  [187, 41, 160]],

 [[255, 255, 255],
  [255, 255, 255],
  [255, 255, 255],
  [255, 255, 255]],

 [[255, 255, 255],
  [0, 0, 0],
  [47, 255, 173],
  [255, 255, 255]]]
)

cv2.imwrite("/Users/eseoseodion/Documents/Python 2023/Visual Code/UDEMY_PROJECTS/app-9/Examples/image2.png", a)