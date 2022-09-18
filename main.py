# python 홈페이지로 가서 python 3.7버전(자신의 컴퓨터 비트에 맞는 것으로..디폴트는 32비트임)을 설치함, 최신버전을 설치하면 tensorflow 라이브러리가 설치가 되지 않으니 주의할 것
# python의 pip로 tensorflow, PIL, numpy, cv2, pyserial을 설치함
# windows의 cmd 창을 열어 설치하면 되며, 순서대로 설치하는 명령어는 다음과 같음
# pip install tensorflow
# pip install pillow
# pip install numpy
# pip install opencv-python
# OpenCV의 확장 모듈을 설치하려면 pip install opencv-contrib-python
# pip install pyserial

# 모두 설치가 되면 아래 import가 정상적으로 동작할 것임

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import serial
import time

# 시리얼 통신 설정
# 파이썬의 시리얼 통신 라이브러리를 이용해 시리얼 통신을 연결하고 이를 사용할 때 ser로 사용할 수 있도록 변수를 지정함
ser = serial.Serial(port='COM9',baudrate=9600)
    # 아래는 윈도우에서의 시리얼 포트 설정방법임, 포트번호는 사용자의 아두이노나 마이크로비트가 연결된 포트번호로 수정해줘야 함
    # 통신속도는 9600bps, 이게 디폴트임.
    


#레이블 가져오기
labels=[]
f=open("labels.txt", "r")
for x in f:
     labels.append(x.rstrip('\n'))
label_count = len(labels)
f.close()

# e-04,e+10과 같은  과학적 표기법을 제거하고 싶을 때 사용하는 옵션
np.set_printoptions(suppress=True)

# Teachable Machine에서 학습시킨 모델 파일을 컴파일을 다시 하지 않고, model 변수에 넣음
model = tensorflow.keras.models.load_model('keras_model.h5', compile=False)

# numpy를 이용해 이미지를 1차원, 높이 224pixel, 폭 224pixel, 색상 3채널(RGB)로 변환해서 data 변수를 만듬.  형식은 float32,
# 여기서는 data 변수를 만드는 의미로 쓰임(4차원의 배열이 만들어짐)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# OpenCV를 이용해 캠으로 들어오는 영상을 cap 변수에 넣음, '0'은 컴퓨터가 인식한 첫번째 카메라를 의미함
cap = cv2.VideoCapture(0)

print('Press "q", if you want to quit')

# while문 안의 내용을 계속 반복시킴. 캠에서 영상 프레임이 들어올 때마다 아래 프로그램을 실행함
while(True):
    # cap 변수에 비디오 프레임이 들어올 때마다 읽어서 frame 변수에 넣음,
    # 제대로 프레임이 읽어지면 ret값이 True, 실패하면 False가 나타남
    # ret는 True, frame.shape는 (480, 640, 3)의 배열로 생성됨.
    ret, frame = cap.read()



    # 들어온 이미지 플립, 이미지 좌우반전(1은 좌우반전, 0은 상하반전)
    flip_frame = cv2.flip(frame, 1)
  
    # 이미지 높이, 폭 추출
    h = flip_frame.shape[0] #480 행의수
    w = flip_frame.shape[1] #640 열의수

    # 이미지를 teachable machine이 학습할 때 사용하는 이미지 비율로 크롭
    # crop_image.shape =>> (480, 480, 3)
    #                       행은 그대로(0:480),   열은 (640-480)/2 : 640-(640-480)/2  => 80:560로 슬라이싱 480*480로 크기 변경
    # 너비의 좌우 80픽셀을 잘라냄.
    crop_image = flip_frame[0:h, int((w-h)/2):int(w-((w-h)/2))]

    # 바이큐빅보간법(cv2.INTER_CUBIC, 이미지를 확대할 때 주로 사용)을 이용해
    # frame변수에 들어온 비디오 프레임의 사이즈를 224, 224로 다운사이징하여 image 변수에 넣음
    # 480,480 이미지를 224, 224이미지로 리사이즈 시킴
    image = cv2.resize(crop_image, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)

    # asarray메소드를 이용해 image에 들어있는 크기가 변형된 이미지를
    # numpy가 처리할 수 있는 배열로 만들어서 image_array 변수에 넣음
    # 리스트 배열을 np배열로 변환
    # np.array는 참조본을 반환하고 np.asarray는 복사본을 반환한다.
    image_array = np.asarray(image)
    
    # image_array에 들어있는 image의 변형된 배열을 정규화(normalized)하기 위해 수식을 적용함
    # 배열값을 -1~1사이값으로 변경
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    
    # 정규화된 배열을 data[0]에 넣음
    data[0] = normalized_image_array

    # 정규화된 배열값으로 정돈된 data를 Teachable Machine으로 학습시켜서 얻은 모델을 이용해 추론하고,
    # 그 결과를 prediction 변수에 넣음
    # [[0.01828334 0.8726836  0.10874491 0.00028817]]
    prediction = model.predict(data)
    # 추론결과를 콘솔에 보여주기
    # print(prediction)
    # 글씨 넣기 준비
    font = cv2.FONT_HERSHEY_TRIPLEX
    fontScale = 1
    fontColor = (0,255,0)
    lineThickness = 1

    # 표기 문구 초기화
    scoreLabel = 0
    score = 0
    result = ''

    for x in range(0, label_count):
         #예측값 모니터링
         line=('%s=%0.0f' % (labels[x], int(round(prediction[0][x]*100)))) + "%"
         cv2.putText(crop_image, line, (10,(x+1)*35), font, fontScale, fontColor, lineThickness)
         
         # 가장 높은 예측 찾기
         if score < int(round(prediction[0][x]*100)):
              scoreLabel = labels[x]
              score = int(round(prediction[0][x]*100))
              result = str(scoreLabel) + " : " + str(score)+"%"
         
    print(result)     
    # 최고 결과치 보여주기
    crop_image = cv2.putText(crop_image, result, (10, int(label_count+1)*35), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    # prediction의 첫번째 리스트값이 0.7을 넘으면 'a'를 utf-8 형태로 인코딩하여 시리얼 통신으로 송신함
    # 학습을 시킬 때는 반드시 디폴트 이미지를 학습시키는 것이 오류를 예방할 수 있는 지름길임
    if prediction[0, 0] > 0.7 :
        send = (str('a')+'\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)


    # prediction의 두번째 리스트값이 0.7을 넘으면 'b'를 utf-8 형태로 인코딩하여 시리얼 통신으로 송신함
    if prediction[0, 1] > 0.7 :
        send = (str('b')+'\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 2] > 0.7 :
        send = (str('c')+'\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 3] > 0.7 :
        send = (str('d')+'\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 4] > 0.7 :
        send = (str('e')+'\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 5] > 0.7 :
        send = (str('f')+'\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)
        
    if prediction[0, 6] > 0.7 :
        send = (str('g')+'\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)
     
    if prediction[0, 7] > 0.7 :
        send = (str('h')+'\n').encode("utf-8")
        ser.write(send)
        print(send)
        time.sleep(2)

    if prediction[0, 8] > 0.7 :
          print('None')

    # 줄바꿈
    print()

    # 원본이미지, 플립이미지, 크롭이미지, 추론용(축소)이미지 화면에 보여주기
    #cv2.imshow('frame',frame) #원본
    #cv2.imshow('flip_frame',flip_frame) #좌우반전
    cv2.imshow('crop_image',crop_image) #좌우 잘라낸후 이미지
    #cv2.imshow('image',image)           #축소한 이미지(224*224)

    # 키 입력을 기다림
    key = cv2.waitKey(1) & 0xFF

    # q 키를 눌렀다면 반복실행에서 종료함
    if key == ord("q"):
        print('Quit')
        break

# 동작이 종료되면 비디오 프레임 캡쳐를 중단함
cap.release()
# 모든 창을 닫음
cv2.destroyAllWindows()
