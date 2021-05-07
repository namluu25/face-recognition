import os
import numpy as np
import cv2
import math
import random

from keras.models import load_model
from keras.utils import CustomObjectScope

import tensorflow as tf
from mtcnn import MTCNN

import glob
import time
from imutils.video import VideoStream
import imutils
import pyttsx3

# while True:
with CustomObjectScope({'tf': tf}):
        model = load_model('./nn4.small2.lrn.h5')
                           # , compile=False)
# add text-to-speech
tts = pyttsx3.init()

while True:
    def image_to_embedding(image, model):
        image = cv2.resize(image, (96, 96))
        img = image[..., ::-1]
        img = np.around(np.transpose(img, (0, 1, 2)) / 255.0, decimals=12)
        x_train = np.array([img])
        embedding = model.predict_on_batch(x_train)
        return embedding


    def recognize_face(face_image, input_embeddings, model):
        embedding = image_to_embedding(face_image, model)

        minimum_distance = 200
        name = None

        # Loop over  names and encodings.
        for (input_name, input_embedding) in input_embeddings.items():

            euclidean_distance = np.linalg.norm(embedding - input_embedding)
            print(embedding.shape)
            print('Euclidean distance from %s is %s' %(input_name, euclidean_distance))

            if euclidean_distance < minimum_distance:
                minimum_distance = euclidean_distance
                name = input_name

        if minimum_distance < 0.68:
            return str(name)
        else:
            return None


    def create_input_image_embeddings():
        input_embeddings = {}

        for file in glob.glob("dataset/*"):
            person_name = os.path.splitext(os.path.basename(file))[0]
            image_file = cv2.imread(file, 1)
            input_embeddings[person_name] = image_to_embedding(image_file, model)

        return input_embeddings



    detector = MTCNN()
    face_cascade = cv2.CascadeClassifier('utils/haarcascade_frontalface_alt.xml')

    #liveness check
    def check_right(righteye,lefteye,nose,orig_eye_dist, orig_nose_x):
        dist = math.sqrt((righteye[0]-lefteye[0])**2 + (righteye[1]-lefteye[1])**2)
        if dist<=orig_eye_dist*0.52 and nose[0]<orig_nose_x:

            return True
        else:
            return False
    def check_left(righteye,lefteye,nose,orig_eye_dist,orig_nose_x):
        dist = math.sqrt((righteye[0]- lefteye[0])**2 + (righteye[1]- lefteye[1])**2)
        if dist<=orig_eye_dist*0.52 and nose[0]>orig_nose_x:
            return True
            while True:
                tts.say("Turn to the left")
                tts.runAndWait()

        else:
            return False

    # Function for Real Time Tests
    def real_time_tests(name):
        tasks = ['Right','Left']
        tasks = random.sample(tasks, 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        count,tasks_completed,out = 0,0,0
        status = False
        # cam = cv2.VideoCapture(0)
        cam = VideoStream(src=0).start()

        while True:
            # image extraction from android phone camera using IP Webcam
            image = cam.read()
            image = imutils.resize(image, width=320)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = detector.detect_faces(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


            if len(result) != 0:
                bounding_box = result[0]['box']
                keypoints = result[0]['keypoints']
                cv2.rectangle(image,(bounding_box[0], bounding_box[1]),(bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),(0,155,255),2)
                cv2.circle(image,(keypoints['left_eye']), 2, (0,155,255), 2)
                cv2.circle(image,(keypoints['right_eye']), 2, (0,155,255), 2)
                cv2.circle(image,(keypoints['nose']), 2, (0,155,255), 2)
                cv2.circle(image,(keypoints['mouth_left']), 2, (0,155,255), 2)
                cv2.circle(image,(keypoints['mouth_right']), 2, (0,155,255), 2)

                # Storing Defaults
                if count==0:
                    original_eye_dist = math.sqrt((keypoints['right_eye'][0]-keypoints['left_eye'][0])**2 + (keypoints['right_eye'][1]-keypoints['left_eye'][1])**2)
                    #print("Original Eye Distance = ",original_eye_dist)
                    original_mouth_dist = math.sqrt((keypoints['mouth_right'][0]-keypoints['mouth_left'][0])**2 + (keypoints['mouth_right'][1]-keypoints['mouth_left'][1])**2)
                    #print("Original Lip Distance = ",original_mouth_dist)
                    original_nose_x = keypoints['nose'][0]
                    count+=1
                    continue

                task = tasks[0]
                image = cv2.resize(image,(800,800))
                image = cv2.putText(image, task, (350,25), font,0.75, (255,255,255), 2)
                cv2.imshow("Test",image)
                if task == 'Right':
                    # tts.say("Turn to the right")
                    # tts.runAndWait()
                    status = check_right(keypoints['right_eye'],keypoints['left_eye'],keypoints['nose'],original_eye_dist,original_nose_x)
                elif task == 'Left':
                    # tts.say("Turn to the left")
                    # tts.runAndWait()
                    status = check_left(keypoints['right_eye'],keypoints['left_eye'],keypoints['nose'],original_eye_dist,original_nose_x)
                if status:
                    tasks_completed += 1
                    tasks = tasks[1:]
                count +=1
            else:
                out+=1
                continue
            if cv2.waitKey(1) == 27 or tasks_completed == 2 or out>1 :
                break
        cam.stop()
        cv2.destroyAllWindows()

        if tasks_completed == 2:
            tts.say("Test complete")
            tts.say("Welcome" + name)
            # tts.runAndWait()
        else:
            tts.say("Access Denied")
        tts.runAndWait()
        #print(out)


    def recognize_faces_in_cam_50(input_embeddings):
        count = 0
        confirmation = 0
        name = ''

        # cam = cv2.VideoCapture(0)
        cam = VideoStream(src=0).start()
        while count <= 5 and confirmation < 2:
            frame = cam.read()
            frame =  imutils.resize(frame, width=320)
            img = frame
            height, width, channels = frame.shape

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Loop through all the faces detected
            identities = ''
            if len(faces) != 0:
                for (x, y, w, h) in faces:
                    x1 = x
                    y1 = y
                    x2 = x + w
                    y2 = y + h

                    face_image = frame[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]
                    identity = recognize_face(face_image, input_embeddings, model)

                    if identity is not None:
                        confirmation += 1
                        name = identity
                count += 1
            else:
                tts.say("Please be infront of the camera")
            tts.runAndWait()
        cam.stop()
        cv2.destroyAllWindows()

        if confirmation == 2:
            print("Face Verification done")
            print("Testing.")
            # tts.runAndWait()
            real_time_tests(name)
        else:
            tts.say("Access Denied")
        tts.runAndWait()


    # main
    input_embeddings = create_input_image_embeddings()
    if input_embeddings != {}:
        print("Face Verification in process")
        # tts.runAndWait()
        recognize_faces_in_cam_50(input_embeddings)
    else:
        print("No User Found")
    time.sleep(5)