#matplotlib inline
import cv2 # OpenCV
import matplotlib.pyplot as plt # Matplotlib
import numpy as np # Numpy


img = plt.imread('mila.jpg')
plt.imshow(img)

face_cascade = cv2.CascadeClassifier('lbp_class/lbpcascade_frontalface.xml')

cinza = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
plt.imshow(cinza, cmap="gray")

faces = face_cascade.detectMultiScale(cinza, scaleFactor=1.3, minNeighbors=5)

img_c = img.copy()
for (x,y,w,h) in faces:
    cv2.rectangle(img_c,(x,y),(x+w,y+h),(255,0,0),8)
    plt.imshow(img_c)