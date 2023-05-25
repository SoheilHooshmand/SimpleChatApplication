import json
import pickle
import redis
from channel import Channels
from user import User
from message import Message

clients = []
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)


class ClientHandler:
    name = ""
    groupName = ""
    inGroup = False
    def __init__(self, clientsocket):
        self.clientsocket = clientsocket
        clients.append(self)


    def handle(self):
        username = pickle.loads(self.clientsocket.recv(1024)).text
        self.name = username
        user = User(username, 'sf477777')
        while True:
            choice = pickle.loads(self.clientsocket.recv(1024)).text
            self.clientsocket.send(pickle.dumps(choice))
            if choice == "1":
                self.intiaoChannel(user)
            else:
                self.createGroup(user)


    def broadcast(self, members, groupname, user):
       mess = Message("exit", "Enter Exit to exit and left to LEFT to group", "sever", "")
       self.clientsocket.send(pickle.dumps(mess))
       while True:
           mes = self.clientsocket.recv(1024)
           r.select(5)
           messages = r.hget(groupname, "messages")
           messages1 = pickle.loads(messages)
           messages1.append(mes)
           r.hset(groupname, "messages", pickle.dumps(messages1))
           message = pickle.loads(mes)
           if message.text != 'Exit' and message.text != "LEFT":
               key = f"{groupname}-{message.author}-{message.time}"
               r.select(4)
               r.set(key, mes)
               for a in range(0, len(members)):
                   if members[a].groupin != groupname:
                       members.remove(members[a])
               usernames = []
               for a in members:
                   usernames.append(a.name)
               for client in clients:

                   if client.clientsocket != self.clientsocket and client.name in usernames and client.inGroup == True and client.groupName == groupname:
                       client.clientsocket.send(mes)
           elif message.text == "LEFT":
               r.select(6)
               u = pickle.loads(r.get(user.name))
               u.subscibes.remove(groupname)
               r.set(user.name, pickle.dumps(u))
               r.select(5)
               members = pickle.loads(r.hget(groupname, "members"))
               mebers1 = []
               for m in members:
                   mebers1.append(pickle.loads(m))
               for m in mebers1:
                   if m.name == user.name:
                       mebers1.remove(m)
               mebers2 = []
               for m in mebers1:
                   mebers2.append(pickle.dumps(m))
               r.hset(groupname, "members" ,pickle.dumps(mebers2))
               backMessages = Message("back", "1-chat \n 2-create group", "server", "")
               self.clientsocket.send(pickle.dumps(backMessages))
               break
           elif message.text == "Exit":
               backMessages = Message("back", "1-chat \n 2-create group", "server", "")
               self.clientsocket.send(pickle.dumps(backMessages))
               break


    def createGroup(self, user):
        channelName = (pickle.loads(self.clientsocket.recv(1024))).text
        description = (pickle.loads(self.clientsocket.recv(1024))).text
        channel = Channels(channelName, user.name,description)

        r.select(5)
        if r.exists(channelName):
            accept = Message("varify", "This channel is currently exist:((", "server", "")
            self.clientsocket.send(pickle.dumps(accept))
        else:
            channel.addUsers(pickle.dumps(user))
            r.hset(channel.name, "creator", channel.creator)
            r.hset(channel.name, "creator_at", channel.created)
            r.hset(channel.name, "description", channel.description)
            r.hset(channel.name, "members",pickle.dumps(channel.users))
            r.hset(channel.name, "messages", pickle.dumps(channel.messages))
            user.addToSubscribe(channelName)
            r.select(6)
            u = r.get(user.name)
            if u != None:
                u1 = pickle.loads(u)
                u1.subscibes.append(channel.name)
                r.set(user.name, pickle.dumps(u1))
            else:
                us = User(user.name, "")
                us.subscibes.append(channel.name)
                r.set(user.name, pickle.dumps(us))
            vaify = Message("varify", "Channel create successfully:))", user.name, "")
            self.clientsocket.send(pickle.dumps(vaify))
            backMessages = Message("back", "1-chat \n 2-create group", "server", "")
            self.clientsocket.send(pickle.dumps(backMessages))






    def creatUser(self):
        name = self.clientsocket.recv(1024)
        password = self.clientsocket.recv(1024)
        realName = pickle.loads(name).text
        realpassword = pickle.loads(password).text
        r.select(2)
        if r.exists(realName):
            varify = Message("varify", "This user is already exits:((", "server", "")
            self.clientsocket.send(pickle.dumps(varify))
        else:
            varify = Message("varify", "create successfully:))", "server", "")
            self.clientsocket.send(pickle.dumps(varify))
            user = User(realName, realpassword)
            r.set(realName, pickle.dumps(user))


    def intiaoChannel(self, user):
        r.select(6)
        u = r.get(user.name)
        u1 = None
        if u != None:
            u1 = pickle.loads(u)
        subscirbes = []
        if u1 != None and len(u1.subscibes) == 0:
            subscirbes.append("subscribe is empty")
        elif u1 != None:
            subscirbes = u1.subscibes
        else:
            subscirbes.append("subscribe is empty")
        r.select(5)
        chennels = r.keys("*")
        c = str(chennels)
        d = []
        if subscirbes[0] != "subscribe is empty":
            for a in subscirbes:
                b = f", b'{a}'"
                if a in c:
                    c = c.replace(a, '')
        else:
            d.append(str(chennels))
        strsub = str(subscirbes)
        m = Message('shows', "subscribes:"+strsub, "server", "" )
        self.clientsocket.send(pickle.dumps(m))
        m1 = Message('shows', "other groups:"+c, "server", "")
        self.clientsocket.send(pickle.dumps(m1))
        mes = self.clientsocket.recv(1024)
        mess = pickle.loads(mes)
        if mess.text in subscirbes:
            user.groupin = mess.text
        else:
            user.groupin = mess.text
            if u1 != None:
                u1.subscibes.append(mess.text)
                r.select(6)
                r.set(user.name, pickle.dumps(u1))
            else:
                newuser = User(user.name, "")
                newuser.subscibes.append(mess.text)
                r.select(6)
                r.set(user.name, pickle.dumps(newuser))

            r.select(5)
            us = r.hget(mess.text, "members")
            us1 = pickle.loads(us)
            uss = []
            for a in us1:
                uss.append(pickle.loads(a))
            for a in uss:
                a.groupin = mess.text
            usss = []
            for a in uss:
                usss.append(pickle.dumps(a))
            usss.append(pickle.dumps(user))
            r.hset(mess.text, "members", pickle.dumps(usss))
        if r.exists(mess.text):
             pipline = r.pipeline(transaction=False)
             pipline.hget(mess.text, "messages")
             a = pipline.execute()
             b = []
             messages2 = []
             for c in a:
                 b.append(pickle.loads(c))
             for d in b:
                 for e in d:
                     messages2.append(pickle.loads(e))
             self.clientsocket.send(pickle.dumps(messages2))
             members = r.hget(mess.text, "members")
             members1 = pickle.loads(members)
             m = []
             for a in members1:
                 m.append(pickle.loads(a))
             self.inGroup = True
             self.groupName = mess.text
             self.broadcast(m, mess.text, user)






