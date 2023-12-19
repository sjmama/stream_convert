import cv2 as cv
import time
import numpy as np
import threading

rtmp_url = "rtmp://streamip/live/0000"
convert_url1 = 'rtmp://streamip/live/0001'
convert_url2 = 'rtmp://streamip/live/0002'
url={'0':"rtmp://streamip/live/0000", '1':'rtmp://streamip/live/0001', '2':'rtmp://streamip/live/0002'}
a=input("0:raw, 1:gausianblur, 2: face\n")
print(url[a])
cap = cv.VideoCapture(url[a])
ttt = time.localtime(time.time()).tm_sec
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()
count=0
while a!='x':
    while cap.isOpened():
        # 비디오 프레임 읽기
        if ttt != time.localtime(time.time()).tm_sec:
            print('calculated',count)
            count=0
            ttt = time.localtime(time.time()).tm_sec
        ret, frame=cap.read()
        cframe = cv.GaussianBlur(frame, (0,0), 2)
        cv.imshow(" ", frame)
        count+=1
        # 화면에 비디오 프레임 표시
        # 'q' 키를 누르면 종료
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    a=input("0:raw, 1:gausianblur, 2: face\n")
    print(url[a])
    cap = cv.VideoCapture(url[a])
# 자원 해제 및 창 닫기
cap.release()
cv.destroyAllWindows()