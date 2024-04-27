import cv2 as cv

img = cv.imread("G:\WebDeveloper\MyProject\python-api-nodejs\public\image\CoinsA.png")
cv.imshow("Coin", img)
k = cv.waitKey(0)