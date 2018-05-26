class Missile:
    def __init__(self, xInitialPos, yInitialPos):
        self.__missilePosX = xInitialPos
        self.__missilePosY = yInitialPos

    def move(self):
        self.__missilePosY = self.__missilePosY - 6

    def getPosX(self):
        return self.__missilePosX

    def getPosY(self):
        return self.__missilePosY
    
    def getPosition(self):
        return (self.__missilePosX, self.__missilePosY)

