import cv2 # OpenCV
#import matplotlib.pyplot as plt # Matplotlib
import numpy as np # Numpy
import math


video = cv2.VideoCapture(0)

while True:
    ret, camFrame = video.read()
    camFrame = cv2.flip(camFrame, 1)
    bordas = cv2.Canny(camFrame, 50, 200)
    
    linhas = cv2.HoughLines(bordas, 1, np.pi / 180, 150, None, 0, 0)
    bordas_copia = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)
    if not linhas is None:
        for i in range(0, len(linhas)):
            rho = linhas[i][0][0]
            theta = linhas[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(bordas_copia, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
    
    linhas_P = cv2.HoughLinesP(bordas, 1, np.pi / 180, 50, None, 50, 10)
    bordas_copia2 = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)
    if not linhas_P is None:
        for linha in linhas_P:
            x1, y1, x2, y2 = linha[0]
            cv2.line(bordas_copia2, (x1, y1), (x2, y2), (0, 255, 0), 3)

    cv2.imshow('camFrame2', bordas_copia2)
    cv2.imshow('camFrame', bordas_copia)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camFrame.release()
cv2.destroyAllWindows()