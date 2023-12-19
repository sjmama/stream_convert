import cv2 as cv
import time
import numpy as np
import threading
# rtmp 주소
rtmp_url = "rtmp://streamip/live/0000"

# OpenCV VideoCapture 객체 생성
cap = cv.VideoCapture(rtmp_url)
frame=cv.imread('./face_test.png')
# 비디오가 정상적으로 열렸는지 확인
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

count = 0
def show_detection(image, faces):
    """Draws a rectangle over each detected face"""

    x, y, w, h = faces
    cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)
    return image
# 화면 크기 조절


ttt=time.localtime(time.time()).tm_sec

def frameread():
    global frame
    global cap
    tcount=0
    tt=time.localtime(time.time()).tm_sec
    while cap.isOpened():
        if tt != time.localtime(time.time()).tm_sec:
            print('recive:',tcount)
            tcount=0
            tt = time.localtime(time.time()).tm_sec
        ret, framex = cap.read()
        frame = cv.resize(framex, dsize=(1280, 720), interpolation=cv.INTER_AREA)
        tcount+=1
    
t= threading.Thread(target=frameread)
t.start()
while cap.isOpened():
    # 비디오 프레임 읽기
    if ttt != time.localtime(time.time()).tm_sec:
        print('calculated',count)
        count=0
        ttt = time.localtime(time.time()).tm_sec
    
    cframe = cv.GaussianBlur(frame, (0,0), 2)
    count+=1
    # 화면에 비디오 프레임 표시
    # 'q' 키를 누르면 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제 및 창 닫기
cap.release()
cv.destroyAllWindows()