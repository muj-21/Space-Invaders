class Invader:
    def __init__(self):
        self.__alienPosX = 0
        self.__alienPosY = 0

    def setPosX(self, x):
        self.__alienPosX = x

    def setPosY(self, y):
        self.__alienPosY = y

    def getPosX(self):
        return self.__alienPosX

    def getPosY(self):
        return self.__alienPosY

    def getPosition(self):
        return (self.__alienPosX, self.__alienPosY)

    def moveHorizontal(self, amount):
        self.__alienPosX = self.__alienPosX + amount

    def moveVertical(self, amount):
        self.__alienPosY = self.__alienPosY + amount    
