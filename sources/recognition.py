import cv2,os,sys
import numpy as np
import pickle
from PIL import Image

def get_images_and_labels(db_path):
    labels=[]
    images=[]
    #nbr=[1,2,3,4]
    paths=[os.path.join(db_path,f) for f in os.listdir(db_path)]
    print len(paths)

    for path in paths:
        print path
        image_pil=Image.open(path).convert('L')
        image=np.array(image_pil,'uint8')
        nbr = int(os.path.split(path)[1].split(".")[0].replace("subject", ""))
        faces = faceCascade.detectMultiScale(
                image,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            )

        for (x,y,w,h) in faces: 
            images.append(cv2.resize(image[y:y+h,x:x+w],(40,40),interpolation=cv2.INTER_CUBIC))
            labels.append(nbr)
            print nbr
            cv2.imshow("Adding faces to traning set...",cv2.resize(image[y:y+h,x:x+w],(20,20),interpolation=cv2.INTER_CUBIC))
            cv2.waitKey(1)
    return images,labels

    
cascadePath="haarcascade_frontalface_default.xml"
faceCascade=cv2.CascadeClassifier(cascadePath)
recognizer=cv2.createLBPHFaceRecognizer()
#recognizer=cv2.createEigenFaceRecognizer()
#recognizer=cv2.createFisherFaceRecognizer()
images,labels=get_images_and_labels("/Users/RISHAV/Desktop/detection/db")
#cv2.imshow("show",predict_image)
recognizer.train(images,np.array(labels))
recognizer.save("rec.xml")
print images,np.array(labels)
predict_image_pil=Image.open(sys.argv[2]).convert('L')
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
    cv2.rectangle(predict_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("facefound",predict_image)
    cv2.waitKey(5000) 