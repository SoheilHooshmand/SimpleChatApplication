import socket
import pickle
from message import Message
import redis
class Cient:

    def __init__(self, name):
        self.name = name
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((socket.gethostname(), 6002))


    def listenig(self):
        while True:
            msg = self.client.recv(2024)
            message = pickle.loads(msg)
            if isinstance(message, list):
                for a in message:
                    print(a)
            else:
             if message == "1":
                 print("Enter enter from you subscribes or subscribes a new group:")
             elif message == "2":
                 print("Enter group name and description one by one;")
             else:
                 print(message)


    def send(self, *k):
        if len(k) == 3:
            message = Message(k[0], k[2], self.name, "")
            self.client.send(pickle.dumps(message))
        else:
            mesg = ""
            if len(k) > 1:
                mesg = input(f"Enter your message({k[1]}): ")
            else:
                mesg = input(f"Enter you message:")
            type = k[0]
            message = Message(type, mesg, self.name, "")
            self.client.send(pickle.dumps(message))
