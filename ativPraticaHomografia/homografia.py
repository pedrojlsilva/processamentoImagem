import argparse
import cv2 # OpenCV
import numpy as np # Numpy

refPt = []
refPt2 = []
count=0
controle = False


def clickCoord(event, x, y, flags, param):
    global refPt, cropping, count, controle
    
    if event == cv2.EVENT_LBUTTONDOWN and count<4:
        refPt.append([x, y])
        count=count+1
    elif(event == cv2.EVENT_LBUTTONDOWN) and (count>=4):
        refPt2.append([x,y])
        count = count + 1  
    elif(count == 8):
        controle = True


pjImg = cv2.imread('download.jpg')
galvaoImg = cv2.imread('galvao.jpg')
peppaImg = cv2.imread('peppa.jpg')


cv2.namedWindow('peppaImg')
cv2.setMouseCallback('peppaImg', clickCoord)
cv2.imshow('peppaImg', peppaImg)
while not controle:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        break


ptsPJ = np.float32([[0,0], [365,0],[365, 399],[0,399]]) #[x,y]
ptsGalvao = np.float32([[0,0], [840,0],[840, 560],[0,560]])
refPt = np.float32(refPt)
refPt2 = np.float32(refPt2)
matrizPJ = cv2.getPerspectiveTransform(ptsPJ,refPt)
matrizGalvao = cv2.getPerspectiveTransform(ptsGalvao,refPt2)

perspectiva = cv2.warpPerspective(pjImg,matrizPJ,(peppaImg.shape[1],peppaImg.shape[0]), peppaImg, borderMode=cv2.BORDER_TRANSPARENT)
perspectiva2 = cv2.warpPerspective(galvaoImg,matrizGalvao,(perspectiva.shape[1],perspectiva.shape[0]), perspectiva, borderMode=cv2.BORDER_TRANSPARENT)
cv2.imshow('peppaImg', perspectiva2)


while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        break


