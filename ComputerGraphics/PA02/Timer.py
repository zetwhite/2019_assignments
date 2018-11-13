import time

class Timer:

    def __init__(self):
        self.dt = -1.0
        self.et = 0.0
        self.currentTime = 0.0
        self.lastTime = 0.0
        self.timerRunning = False

    def isTimerOn(self):
        if self.dt > 0:
            return True
            return False

    def start(self):
        if self.timerRunning is not True:
            self.currentTime = time.clock()
            self.lastTime = self.currentTime

        self.timerRunning = True

    def stop(self):
        self.timerRunning = False


    def reset(self):
        self.dt = -1.0
        self.et = 0.0
        self.currentTime = 0.0
        self.lastTime = 0.0
        self.timerRunning = False

    def getDt(self):
        if self.timerRunning is not True :
            return 0.0

        self.currentTime = time.clock()
        self.dt = self.currentTime - self.lastTime
        self.lastTime = self.currentTime
        self.et += self.dt
        return self.dt

    def getEt(self):
        self.getDt()
        return self.et
    
