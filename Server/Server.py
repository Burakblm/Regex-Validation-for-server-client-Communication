import threading
import socket
from database import Database

host = '127.0.0.1' # local host
port = 55555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()

def handle(client):
  while True:
    try:
      message = client.recv(1024)
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