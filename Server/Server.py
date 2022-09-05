import re
import threading
import socket
from database import Database

host = '127.0.0.1' # local host
port = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()

reg = r"^([0][1-9]|[3][01]|[12][0-9])([ \/\-])([0][1-9]|[1][012])([ \/\-])([0-9][0-9])([ ])([0-1][0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])([ ])([\d]{1,4}[ ][\d]{1,4}[ ][\d]{1,4}[ ][\d]{1,4})$"


def control(reg,txt):
    ret = False
    if re.match(reg, txt):
        ret = True
    return ret

def handle(client):
  while True:
    try:
      message = client.recv(1024)
      if control(reg, str(message)[4:-1]):
        print(str(message)[4:-1])
        ths = open("file.txt", "a")
        ths.write(str(message)[4:-1]+"\n")
        ths.close()
        
    except:
      client.close()
      dt = Database()
      break

def recive():
  while True:
    client, address = server.accept()
    print(f'Connected with {str(address)}')

    client.send('connected to the server!'.encode('utf8'))

    thread = threading.Thread(target=handle, args=(client,))
    thread.start()

print("Server is listening...")
recive()