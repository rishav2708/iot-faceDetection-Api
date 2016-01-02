from flask import Flask,render_template
import sys
import cv2
from PIL import Image
import numpy as np
import os
import urllib
cascadePath="haarcascade_frontalface_default.xml"
faceCascade=cv2.CascadeClassifier(cascadePath)
recognizer=cv2.createLBPHFaceRecognizer()
recognizer.load("rec.xml")
#urllib.urlretrieve("http://192.168.0.100:81/snapshot.cgi?user=admin&pwd=googlevirus","detected.jpg")
#predict_image_pil=Image.open("detected.jpg").convert('L')
predict_image_pil=Image.open(sys.argv[1]).convert('L')
predict_image=np.array(predict_image_pil)
faces = faceCascade.detectMultiScale(
				predict_image,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            )
for (x,y,w,h) in faces:
    nbr_predicted,conf=recognizer.predict(cv2.resize(predict_image[y:y+h,x:x+w],(40,40),interpolation=cv2.INTER_CUBIC))
    print nbr_predicted,conf
    if conf<50.0:
    	if nbr_predicted==1:
    		os.system(" espeak 'hi rishu'")
    	elif nbr_predicted==2:
    		os.system("espeak 'hi bholu' ")
        else:
            os.system("espeak 'hi maa'")
    cv2.rectangle(predict_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("facefound",predict_image)
    cv2.waitKey(1) 
