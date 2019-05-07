import cv2
import numpy as np

img = cv2.imread('quadrados2.png')


img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
borrado = cv2.blur(img_cinza, (3, 3))
et, binarizada = cv2.threshold(borrado, 100, 255, cv2.THRESH_BINARY)
contornos, hierarquia = cv2.findContours(binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
hull = []
for i in range(len(contornos)):
    hull.append(cv2.convexHull(contornos[i], False))

resultado = np.zeros((binarizada.shape[0], binarizada.shape[1], 3), np.uint8)
for i in range(len(contornos)):
    cv2.drawContours(resultado, contornos, i, (0, 255, 0), 2, 8, hierarquia)
    #cv2.drawContours(resultado, hull, i, (255, 255, 255), 2, 8)

cv2.imshow('img', resultado)
cv2.waitKey(0)