from cmu_112_graphics2 import *
from tkinter import *
import cv2
import time
import numpy as np


def appStarted(app):
    app.cap = cv2.VideoCapture(0)
 
    # Create the background subtractor object
    # Use the last 700 video frames to build the background
    app.back_sub = cv2.createBackgroundSubtractorMOG2(history=700, 
        varThreshold=25, detectShadows=True)
 
    # Create kernel for morphological operation
    # You can tweak the dimensions of the kernel
    # e.g. instead of 20,20 you can try 30,30.
    app.kernel = np.ones((20,20),np.uint8)
    app.frame = None
    app.areas = []
    app.contours = []
    app.timerDelay = 10

def timerFired(app):
    if len(app.areas) > 1:
        drawCameraHelper(app)
    else:
        print('no')
    
    
def cameraFired(app):
    ret, app.frame = app.cap.read()
    app.frame = cv2.flip(app.frame, 1)
    fg_mask = app.back_sub.apply(app.frame)
 
        # Close dark gaps in foreground object using closing
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, app.kernel)
 
        # Remove salt and pepper noise with a median filter
    fg_mask = cv2.medianBlur(fg_mask, 5) 
         
        # Threshold the image to make it either black or white
    _, fg_mask = cv2.threshold(fg_mask,127,255,cv2.THRESH_BINARY)
    fg_mask_bb = fg_mask
    app.contours, hierarchy = cv2.findContours(fg_mask_bb,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    app.areas = [cv2.contourArea(c) for c in app.contours]
    #print(app.areas)
    

def drawCameraHelper(app):
    # Find the largest moving object in the image
    max_index = np.argmax(app.areas)
    # Draw the bounding box
    cnt = app.contours[max_index]

    x,y,w,h = cv2.boundingRect(cnt)
    if ((x >= 0 and x + w < app.width) and
        (y >= 0 and y + h < app.height)):
            cv2.rectangle(app.frame,(x,y),(x+w,y+h),(0,255,0),3)

    # Draw circle in the center of the bounding box
    x2 = x + int(w/2)
    y2 = y + int(h/2)
    if ((x2 >= 0 and x2 < app.width) and
        (y2 >= 0 and y2 < app.height)):
            cv2.circle(app.frame,(x2,y2),4,(0,255,0),-1)

    # Print the centroid coordinates (we'll use the center of the
    # bounding box) on the image
            text = "x: " + str(x2) + ", y: " + str(y2)
            cv2.putText(app.frame, text, (x2 - 10, y2 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    
def keyPressed(app, event):
    if event.key == "q":
        App._theRoot.app.quit()

def redrawAll(app, canvas):
    # making a frame
    canvas.create_rectangle(app.width/5, app.height/6 - 10, 
                            4*app.width/5, 5*app.height/6 + 10,
                            width = 5)
    if len(app.areas) < 1:
    #         # Display the resulting frame
        app.drawCamera(canvas)
    else:
        drawCameraHelper(app)
    app.drawCamera(canvas)
        

runApp(width=1080, height=720)
