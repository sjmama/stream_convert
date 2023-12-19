import cv2 as cv
import subprocess
import numpy as np

command1 = ['ffmpeg',                                           
           '-y',                                                                  
           '-f', 'rawvideo',                                                       
           '-c:v', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(1280, 720),
           '-r', '30',
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           "rtmp://streamip/live/0001"]
command2 = ['ffmpeg',                                           
           '-y',                                                                  
           '-f', 'rawvideo',                                                       
           '-c:v', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(1280, 720),
           '-r', '30',
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           "rtmp://streamip/live/0002"]

# using subprocess and pipe to fetch frame data
p1 = subprocess.Popen(command1, stdin=subprocess.PIPE)#720p 0000
p2 = subprocess.Popen(command2, stdin=subprocess.PIPE)

rtmp_url = "rtmp://streamip/live/0000"

# OpenCV VideoCapture 객체 생성
cap = cv.VideoCapture(rtmp_url)

# 비디오가 정상적으로 열렸는지 확인
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# 화면 크기 조절

while cap.isOpened():
    # 비디오 프레임 읽기
    ret, frame = cap.read()
    frame = cv.resize(frame, dsize=(1280, 720), interpolation=cv.INTER_AREA)
    frame1 = cv.GaussianBlur(frame, (0,0), 2)
    frame2=frame[:]
    retval, faces_haar_alt2 = cv.face.getFacesHAAR(frame, "./haarcascade_frontalface_alt2.xml")
    if faces_haar_alt2 is not None:
        faces_haar_alt2 = np.squeeze(faces_haar_alt2)
        if faces_haar_alt2.ndim != 1:
            for (x, y, w, h) in faces_haar_alt2:
                cv.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 3)
        else:
            cv.rectangle(frame2, (faces_haar_alt2[0], faces_haar_alt2[1]), (faces_haar_alt2[0] + faces_haar_alt2[2], faces_haar_alt2[1] + faces_haar_alt2[3]), (255, 0, 0), 3)
    p1.stdin.write(frame1.tobytes())
    p2.stdin.write(frame2.tobytes())
    # 'q' 키를 누르면 종료

# 자원 해제 및 창 닫기
cap.release()
cv.destroyAllWindows()