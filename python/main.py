import cv2 as cv

img = cv.imread("../public/image/CoinsA.png")
cv.imshow("Coin", img)
k = cv.waitKey(0)