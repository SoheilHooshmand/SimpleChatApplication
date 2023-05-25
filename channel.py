channels = []
import time
class Channels:
    def __init__(self, name, creator, description):
        self.name = name
        self.creator = creator
        self.description = description
        self.created = time.ctime()
        self.users = []
        self.messages = []

    def __str__(self):
        return self.name

    def addUsers(self, user):
        self.users.append(user)

    def addMessage(self, message):
        self.messages.append(message)

    def exisitChannel(self, channel):
        if channel in channels:
            return False
        else:
            channels.append(channel)
            return True
