
class User :
    groupin = ""
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.subscibes = []

    def __str__(self):
        return self.name

    def addToSubscribe(self, group):
        self.subscibes.append(group)



