import time
class Message :
    groupMessages = []
    def __init__(self, type, text, author, groupname):
        self.type = type
        self.text = text
        self.author = author
        self.time = time.ctime()
        self.groupname = groupname

    def __str__(self):
        return f"[{self.time}], {self.author} : {self.text}"

    def showGroupMessages(self, groupMes):
        self.groupMessages = groupMes
