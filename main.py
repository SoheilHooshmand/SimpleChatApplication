from client import Cient
import threading


name = input("Enter your name: ")
c = Cient(name)
c.send("login", "", name)
t = threading.Thread(target=c.listenig)
t.start()
while True:
     print("1-chat")
     print("2-create group")
     while True:
      c.send("start", "")

