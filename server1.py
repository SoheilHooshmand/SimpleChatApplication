import socket
import threading
from clientHandler import ClientHandler


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 6002))
server.listen(5)
print("server is listening...")
while True:
    client, address = server.accept()
    print(f"{address} is connected")
    clienthandler = ClientHandler(client)
    t = threading.Thread(target=clienthandler.handle)
    t.start()
