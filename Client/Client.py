import cv2
import socket
import threading
import datetime
import re

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1' # local host
port = 55555
client.connect((host, port))


face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def is_datetime(text):
        reg = r"^([0][1-9]|[3][01]|[12][0-9])([ \/\-])([0][1-9]|[1][012])([ \/\-])([0-9][0-9])([ ])([0-1][0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])$"
        return re.match(reg, text)

def is_rectangle(text):
        reg = r"^[\d]{1,4}[ ][\d]{1,4}[ ][\d]{1,4}[ ][\d]{1,4}$"
        return re.match(reg, text)

def recive():
    while True:
        try:
            message = client.recv(1024).decode('utf8')
        except:
            print("An error occured!")
            client.close()
            break
        
recive_thread = threading.Thread(target=recive)
recive_thread.start()


cap = cv2.VideoCapture(0)


while True:

    ret,frame = cap.read()
    
    if ret:
        
        face_rect = face_cascade.detectMultiScale(frame,minNeighbors = 20)
        
        for (x,y,w,h) in face_rect:
            
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)
        
        cv2.imshow("face detect",frame)
        
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%x %X')
        
        if is_datetime(dtime) and is_rectangle(str(face_rect)[2:-2]):
            message = f': {dtime + " " + str(face_rect)[2:-2]}'
            client.send(message.encode('utf8'))
            
    if cv2.waitKey(1) & 0xFF == ord("q"):
        client.close()
        break

cap.release()
cv2.destroyAllWindows()