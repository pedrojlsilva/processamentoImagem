import vrep
import cv2
import array
import numpy as np
import time
from PIL import Image as I

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

soma=0

while True:
	r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_buffer);
	mat = np.asarray(image, dtype=np.uint8) 
	mat2 = mat.reshape(resolution[1], resolution[0], 1)  #resolution[] = y
	mat2_bin = cv2.threshold(mat2,127,255,cv2.THRESH_BINARY)
	#array_lin = mat2_bin[300][:]
	mat3 = mat2_bin[1]
	x=-318

	for count_for in range (0, 640):
		soma = soma+mat3[10,count_for]*x
		x+=1


	
	soma=soma*0.0000007
	print(soma)
	vrep.simxSetJointTargetVelocity(clientID, leftmotor, 2+soma, vrep.simx_opmode_streaming);
	vrep.simxSetJointTargetVelocity(clientID, rightmotor, 2-soma, vrep.simx_opmode_streaming);	
	cv2.imshow('robot camera', cv2.flip( mat2, 0 ))
	#cv2.imshow('robotLimiar', mat2_bin[1])
	soma=0

	cv2.waitKey(1)