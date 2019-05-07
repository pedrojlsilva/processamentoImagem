import pafy
import cv2 as cv
import numpy as np

class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv.imshow(self.windowname, self.dests[0])
        cv.imshow(self.windowname + ": mask", self.dests[1])

    # onMouse function for Mouse Handling
    def on_mouse(self, event, x, y, flags, param):
        pt = (x, y)
        if event == cv.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv.EVENT_LBUTTONUP:
            self.prev_pt = None

        if self.prev_pt and flags & cv.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv.line(dst, self.prev_pt, pt, color, 5)
            self.dirty = True
            self.prev_pt = pt
            self.show()


capture=cv.VideoCapture('videoCasseta.mp4')
ret, frame = capture.read()
img_mask = frame.copy()
inpaintMask = np.zeros(frame.shape[:2], np.uint8)
sketch = Sketcher('image', [img_mask, inpaintMask], lambda : ((255, 255, 255), 255))

inpaintOn = True

while True:
    if cv.waitKey(22) & 0xff == ord('r'):
            break


while(True):
    ret, frame = capture.read()
    if ret == True:
        if cv.waitKey(15) & 0xff == ord('m'):
            inpaintOn = not inpaintOn
        if cv.waitKey(15) & 0xff == ord('q'):
            cv.imwrite('inpaintMask.png',inpaintMask)
            break

        if inpaintOn:
            res = cv.inpaint(src=frame, inpaintMask=inpaintMask, inpaintRadius=10, flags=cv.INPAINT_TELEA)
            cv.imshow('Frame', res)
            
        else:
            cv.imshow('Frame', frame)
        
    
    else:
        print('nao esta capturando')
        break