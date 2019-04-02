import math
import numpy as np, cv2

width = 640
heigth = 640

dx = 80
dy = 80

refPtx = [[]]
inputVideo2 = cv2.VideoCapture("OBR.mp4")
imagem = np.zeros((width, heigth, 3), np.uint8)
referencePoints = [0,0,0,0]

col=0
line=0
lineStatus= False


while True:

    ret, imgVideo2 = inputVideo2.read()
    rows2, cols2 = imgVideo2.shape[:2]
    ptsVideo2 = np.float32([[0,0],[cols2,0],[cols2,rows2],[0,rows2]])

    if not lineStatus:
        referencePoints = np.float32(([col*dx,line*dy],[(col+1)*dx,line*dy],[(col+1)*dx,(line+1)*dy],[col*dx,(line+1)*dy]))
    else:
        referencePoints = np.float32(([(col+1)*dx,line*dy],[(col+2)*dx,line*dy],[(col+2)*dx,(line+1)*dy],[(col+1)*dx,(line+1)*dy]))


    M = cv2.getPerspectiveTransform(ptsVideo2,referencePoints)
    
    image2 = cv2.warpPerspective(imgVideo2, M, (heigth,width), imagem, borderMode=cv2.BORDER_TRANSPARENT)
    cv2.imshow("imagem", image2)


    if col == 6:
        col=0
        line+=1
        lineStatus = not lineStatus
    elif line == 8:
        line=0
    else:
        col+=2


    key = cv2.waitKey(33) & 0xFF
    if key == ord('s'):
        break



    

cv2.destroyAllWindows()


