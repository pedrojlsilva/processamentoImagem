import vrep
import cv2
import array
import numpy as np
import time
from PIL import Image as I

leftPot=0
rightPot=0

print('program started')
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)
print ('Connected to remote API server')
r, colorCam = vrep.simxGetObjectHandle(clientID, "kinect_rgb", vrep.simx_opmode_oneshot_wait);
r, leftmotor = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_leftMotor", vrep.simx_opmode_oneshot_wait);
r, rightmotor = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor", vrep.simx_opmode_oneshot_wait);

vrep.simxSetJointTargetVelocity(clientID, leftmotor, 0, vrep.simx_opmode_streaming);
vrep.simxSetJointTargetVelocity(clientID, rightmotor, 0, vrep.simx_opmode_streaming);

r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_streaming);
time.sleep(0.5)


while True:
	r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_buffer);
	mat = np.asarray(image, dtype=np.uint8) 
	mat2 = mat.reshape(resolution[1], resolution[0], 1)  #resolution[1] = y
	mat2_bin = cv2.threshold(mat2,127,255,cv2.THRESH_BINARY)
	mat3 = cv2.flip(mat2_bin[1],0)
	count=0
	fatorMultDir=10
	fatorMultEsq=10
	countAnt=0
	while (count<=639 and mat3[470,count]>0) :
		count+=1
		
	if(count<150):
		fatorMultDir=3.5
		fatorMultEsq=0
		
	elif(count>450):
		fatorMultDir=0
		fatorMultEsq=3.5
	else:
		fatorMultDir=7
		fatorMultEsq=7

	if(count==640):
		if(countAnt>400):
			count=640
		else:
			count=count
	else:
		countant=count
		
	leftPot=(count/640) 
	rightPot=((640-count)/640)
	
	
	vrep.simxSetJointTargetVelocity(clientID, leftmotor, (leftPot*fatorMultEsq), vrep.simx_opmode_streaming);
	vrep.simxSetJointTargetVelocity(clientID, rightmotor, (rightPot*fatorMultDir), vrep.simx_opmode_streaming);	
	print(leftPot*fatorMultEsq)
	print(fatorMultDir*rightPot)
	cv2.imshow('robot camera', mat3)

	cv2.waitKey(1)
