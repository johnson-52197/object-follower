import cv2
import serial
import time
import numpy as np
import RPi.GPIO as GPIO

cap = cv2.VideoCapture(0)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
p = GPIO.PWM(3, 100)
time.sleep(1.0)

p.start(0)

def process(cnt):
    c = max(cnt, key=cv2.contourArea)
    
    x,y,w,h = cv2.boundingRect(c)
    end_cord_x = x+w
    end_cord_y = y+h
    center_cord_x = int((end_cord_x + x)/2)
    center_cord_y = int((end_cord_y +y)/2)
    cv2.rectangle(img,(x,y), (end_cord_x, end_cord_y), (0,255,0), 1)
    cv2.circle(img, (center_cord_x, center_cord_y), 5,(0,255,0),3)
    distance = center_cord_x - c_x
    if distance < -50:
        GPIO.output(2, GPIO.HIGH)
        p.ChangeDutyCycle(30)
    if distance > 50:
        GPIO.output(2, GPIO.LOW)
        p.ChangeDutyCycle(30)
    if distance > -50 and distance < 50:
        p.ChangeDutyCycle(0)
    print("detected")

while True:
    _, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    height, width , _ = img.shape
    c_y = int(height/2)
    c_x = int(width/2)
    weaker = np.array([30, 100, 100])
    stronger = np.array([50, 255, 255])
    cv2.circle(img, (c_x, c_y), 5, (0,0,255), 3)
    
    mask = cv2.inRange(hsv, weaker, stronger)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        process(contours)
    if len(contours) == 0:
#        print("not")
        
        p.ChangeDutyCycle(0)
        
        
    cv2.imshow('img',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        p.ChangeDutyCycle(0)
        break
    
video.release()
video.isOpened()
cv2.destroyAllWindows()
        

