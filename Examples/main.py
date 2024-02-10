# To read an image
import cv2

array = cv2.imread("/Users/eseoseodion/Documents/Python 2023/Visual Code/UDEMY_PROJECTS/app-9/Examples/image.png")
print(array.shape)
a, b, c = array.shape
print(f"{a} is the number of vertical pixels, {b} is the number of horizontal pixels, and {c} is the number of channels.")
print(array)