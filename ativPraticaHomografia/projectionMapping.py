 
import math
import numpy as np, cv2

width = 640 #comprimento
height = 480 #altura

referencePoints = np.float32([[width/6,height/6],[2*width/6,height/6],[2*width/6,2*height/6],[width/6,2*height/6], [4*width/6,height/6],[5*width/6,height/6],[5*width/6,2*height/6],[4*width/6,2*height/6], [width/6,3*height/6],[2*width/6,3*height/6],[2*width/6,4*height/6],[width/6,4*height/6]])


currentPoint = -1
calibrating = True
fullScreen = False

inputVideo1 = cv2.VideoCapture("Valvula.avi")
inputVideo2 = cv2.VideoCapture("OBR.mp4")
inputVideo3 = cv2.VideoCapture("Valvula.avi")

ret, imgVideo1 = inputVideo1.read()
ret, imgVideo2 = inputVideo2.read()
ret, imgVideo3 = inputVideo3.read()

rows1, cols1 = imgVideo1.shape[:2]
rows2, cols2 = imgVideo2.shape[:2]
rows3, cols3 = imgVideo3.shape[:2]

ptsVideo1 = np.float32([[0,0],[cols1,0],[cols1,rows1],[0,rows1]])
ptsVideo2 = np.float32([[0,0],[cols2,0],[cols2,rows2],[0,rows2]])
ptsVideo3 = np.float32([[0,0],[cols3,0],[cols3,rows3],[0,rows3]])

image = np.zeros((height, width, 3), np.uint8)

def pointColor(n):
	if n == 0:
		return (0,0,255)
	elif n == 1:
		return (0,255,255)
	elif n == 2:
		return (255,255,0)
	elif n==3:
		return (0,255,0)

def mouse(event, x, y, flags, param):
	global currentPoint
	

	
	if event == cv2.EVENT_LBUTTONDOWN:
		cp = 0
		
		for point in referencePoints:
			dist = math.sqrt((x-point[0])*(x-point[0])+(y-point[1])*(y-point[1]))
			if dist < 4:
				currentPoint = cp
				break   
			else:
				cp = cp + 1
		
		

	if event == cv2.EVENT_LBUTTONUP:
		currentPoint = -1
		
	if currentPoint != -1:
		referencePoints[currentPoint] = [x,y]

cv2.namedWindow("test", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("test", mouse)

while True:
	ret, imgVideo1 = inputVideo1.read()
	ret, imgVideo2 = inputVideo2.read()
	ret, imgVideo3 = inputVideo3.read()
	image[:] = (0,0,0)

	if calibrating:
		color = 0
		for point in referencePoints:
			cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color), -1)

			if color == 3:
				color=0
			else:
				color = color + 1


		
	
	M = cv2.getPerspectiveTransform(ptsVideo1,referencePoints[0:4])
	image2 = cv2.warpPerspective(imgVideo1, M, (cols1,rows1), image, borderMode=cv2.BORDER_TRANSPARENT)

	M2 = cv2.getPerspectiveTransform(ptsVideo2,referencePoints[4:8])
	image3 = cv2.warpPerspective(imgVideo2, M2, (cols1,rows1), image2, borderMode=cv2.BORDER_TRANSPARENT)


	M3 = cv2.getPerspectiveTransform(ptsVideo3,referencePoints[8:])
	image4 = cv2.warpPerspective(imgVideo3, M3, (cols1,rows1), image3, borderMode=cv2.BORDER_TRANSPARENT)


	cv2.imshow("test", image4)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("c"):
		calibrating = not calibrating

	if key == ord("f"):
		if fullScreen == False:
			cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		else:
			cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
		fullScreen = not fullScreen

	if key == ord("q"):
		break

cv2.destroyAllWindows()
