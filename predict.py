import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import serial
import time

ser = serial.Serial(port='COM9', baudrate=9600)

labels = []
f = open("labels.txt", "r")
for x in f:
    labels.append(x.rstrip('\n'))
label_count = len(labels)
f.close()

np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model('keras_model.h5', compile=False)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
cap = cv2.VideoCapture(1)

print('Press "q", if you want to quit')

while (True):
    ret, frame = cap.read()
    flip_frame = cv2.flip(frame, 1)
    h = flip_frame.shape[0]
    w = flip_frame.shape[1]
    crop_image = flip_frame[0:h, int((w - h) / 2):int(w - ((w - h) / 2))]
    image = cv2.resize(crop_image, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    font = cv2.FONT_HERSHEY_TRIPLEX
    fontScale = 1
    fontColor = (0, 255, 0)
    lineThickness = 1

    scoreLabel = 0
    score = 0
    result = ''

    for x in range(0, label_count):
        line = ('%s=%0.0f' % (labels[x], int(round(prediction[0][x] * 100)))) + "%"
        cv2.putText(crop_image, line, (10, (x + 1) * 35), font, fontScale, fontColor, lineThickness)

        if score < int(round(prediction[0][x] * 100)):
            scoreLabel = labels[x]
            score = int(round(prediction[0][x] * 100))
            result = str(scoreLabel) + " : " + str(score) + "%"

    print(result)
    crop_image = cv2.putText(crop_image, result, (10, int(label_count + 1) * 35), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    if prediction[0, 0] > 0.7:
        send = (str('a') + '\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 1] > 0.7:
        send = (str('b') + '\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 2] > 0.7:
        send = (str('c') + '\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 3] > 0.7:
        send = (str('d') + '\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 4] > 0.7:
        send = (str('e') + '\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 5] > 0.7:
        send = (str('f') + '\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 6] > 0.7:
        send = (str('g') + '\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 7] > 0.7:
        send = (str('h') + '\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 8] > 0.7:
        print('None')

    print()

    cv2.imshow('crop_image', crop_image)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        print('Quit')
        break

cap.release()
cv2.destroyAllWindows()
