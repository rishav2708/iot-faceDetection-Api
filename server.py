from flask import Flask
import urllib
from PIL import Image
import json
import cv2
import numpy as np
app=Flask(__name__)
@app.route("/")
def intro():
    cascadePath="haarcascade_frontalface_default.xml"
    faceCascade=cv2.CascadeClassifier(cascadePath)
    recognizer=cv2.createLBPHFaceRecognizer()
    recognizer.load("rec.xml")
    urllib.urlretrieve("http://192.168.0.100:81/snapshot.cgi?user=admin&pwd=googlevirus","detected.jpg")
    predict_image_pil=Image.open("detected.jpg").convert('L')
    predict_image=np.array(predict_image_pil)
    faces = faceCascade.detectMultiScale(
				predict_image,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            )
    print faces
    d={"results":[]}
    for (x,y,w,h) in faces:
    	nbr_predicted,conf=recognizer.predict(cv2.resize(predict_image[y:y+h,x:x+w],(40,40),interpolation=cv2.INTER_CUBIC))
    	print nbr_predicted,conf
    	if conf<=50.0:
    		print "hi"
    		if nbr_predicted==1:
    			data={"name":"Rishav","message":"hi master"}
    			print data
    			d["results"].append(data)
    		elif nbr_predicted==2:
    			data={"name":"Kushagra","message":"hi bhole"}
    			d["results"].append(data)
    return json.dumps(d)
if __name__=="__main__":
	app.run()
