# -*- coding: cp949 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random
import numpy as np
import math

import CGGame
import Particle
#import BillTable
from PIL import Image
import time
from Timer import *
from Lighting import *

nTex = 6
texArr = None
angle = 0
spaceSize = 50

CubeCo1 = [spaceSize, 2*spaceSize, -1*spaceSize]
CubeCo2 = [spaceSize, 2*spaceSize, spaceSize]
CubeCo3 = [spaceSize, 0, spaceSize]
CubeCo4 = [spaceSize, 0, -1*spaceSize]
CubeCo5 = [-1*spaceSize, 0,spaceSize]
CubeCo6 = [-1*spaceSize, 2*spaceSize, spaceSize]
CubeCo7 = [-1*spaceSize, 2*spaceSize, -1*spaceSize]
CubeCo8 = [-1*spaceSize, 0, -1*spaceSize]
lightPos = [0, spaceSize, 0, 0]

## camera and billTable setting values ## 
cameraDistance = spaceSize - 10; 
cameraPos = [cameraDistance, cameraDistance, cameraDistance]
cameraCen = [0, spaceSize-30, 0]
billSize = [40, 20, 25]

def computeNormal(p1, p2, p3) :
    u = np.array([p2[i] - p1[i] for i in range(0, 3)])
    v = np.array([p3[i] - p1[i] for i in range(0, 3)])
    N = np.cross(u, v)
    N = N / np.linalg.norm(N)
    return N

def loadImage(imageName) :
    img = Image.open(imageName)
    img = img.rotate(90) 
    img_data = np.array(list(img.getdata()), np.uint8)
    return img.size[0], img.size[1], img_data

def setTexture(textArr, idx, fileName, option):
    glBindTexture(GL_TEXTURE_2D, textArr[idx])
    print(textArr[idx])
    imgW, imgH, myImage = loadImage(fileName)
    print(fileName) 
    print(imgW, imgH, myImage) 

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, imgW, imgH, 0, option, GL_UNSIGNED_BYTE, myImage)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP) 
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST) 

def backgroundInit() :
    global nTex, texArr;
    texArr = glGenTextures(nTex) 
    glEnable(GL_DEPTH_TEST)
    setTexture(texArr, 0, "backGround2.jpg", GL_RGB)
    setTexture(texArr, 1, "backGround4.jpg", GL_RGB)
    setTexture(texArr, 2, "backGround4.jpg", GL_RGB)
    setTexture(texArr, 3, "backGround2.jpg", GL_RGB)
    setTexture(texArr, 4, "backGround5.jpg", GL_RGB) 
    glEnable(GL_TEXTURE_2D);    

def drawSquare(point1, point2, point3, point4):
    glBegin(GL_QUADS)
    N = computeNormal(point1, point2, point3)
    glNormal3fv(N)
    glTexCoord2f(0, 0)
    glVertex3fv(point1)
    glTexCoord2f(0, 1) 
    glVertex3fv(point2)
    glTexCoord2f(1, 1)
    glVertex3fv(point3)
    glTexCoord2f(1, 0) 
    glVertex3fv(point4)
    glEnd()

def drawBackGround():
    global texArr
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texArr[0])
    drawSquare(CubeCo2, CubeCo1, CubeCo4, CubeCo3)

    glBindTexture(GL_TEXTURE_2D, texArr[1])
    drawSquare(CubeCo1, CubeCo7, CubeCo8, CubeCo4)
  
    glBindTexture(GL_TEXTURE_2D, texArr[3])
    drawSquare(CubeCo7, CubeCo6, CubeCo5, CubeCo8)

    glBindTexture(GL_TEXTURE_2D, texArr[2])
    drawSquare(CubeCo6, CubeCo2, CubeCo3, CubeCo5)

    glBindTexture(GL_TEXTURE_2D, texArr[4])
    drawSquare(CubeCo3, CubeCo4, CubeCo8, CubeCo5) 
    glPopMatrix()


class myGame(CGGame.Game) :

    def __init__(self, w, h, title):
        super(myGame,self).__init__(w,h,title)
        super(myGame, self).timerStart() 
        self.setCamera(cameraPos, cameraCen , [0, 1, 0] )
       # self.setLightPos(lightPos)

    def frame(self):
        dt = self.getDt()
        super(myGame,self).frame()
        
    #def setLightPos(self, pos) :
    #    super(myGame, self).setLightPosition(pos) 

    def setCamera(self, eye, cen, up) :
        super(myGame, self).cameraAt(eye, cen, up) 
        
    def afterframe(self):
        super(myGame,self).afterFrame()


## BillTable class ##
class BillTable:
    Cube1 = [0, 0, 0]
    Cube2 = [0, 1, 0]
    Cube3 = [0, 1, 1]
    Cube4 = [0, 0, 1]
    Cube5 = [-1, 0, 0]
    Cube6 = [-1, 1, 0]
    Cube7 = [-1, 1, 1]
    Cube8 = [-1, 0, 1]
    Cube2_inside = [-0.1, 1, 0.1]
    Cube3_inside = [-0.1, 1, 0.9]
    Cube6_inside = [-0.9, 1, 0.1]
    Cube7_inside = [-0.9, 1, 0.9]
    Cube2_inside_up = [-0.1, 1.1, 0.1]
    Cube3_inside_up = [-0.1, 1.1, 0.9]
    Cube6_inside_up = [-0.9, 1.1, 0.1]
    Cube7_inside_up = [-0.9, 1.1, 0.9]   
    Cube2_up = [0, 1.1, 0]
    Cube3_up = [0, 1.1, 1]
    Cube6_up = [-1, 1.1, 0]
    Cube7_up = [-1, 1.1, 1]
    
    color_up= [0, 1, 1, 1] 
    color_side = [0.4, 0.3, 0.3, 1]

    def computeNormal(self, p1, p2, p3) :
        u = np.array([p2[i] - p1[i] for i in range(0, 3)])
        v = np.array([p3[i] - p1[i] for i in range(0, 3)])
        N = np.cross(u, v)
        N = N / np.linalg.norm(N)
        return N
 
    def drawSquare(self, color, point1, point2, point3, point4):
        glBegin(GL_QUADS)
        N = self.computeNormal(point1, point2, point3)
        glNormal3fv(N)
        glColor(color[0], color[1], color[2])
        glVertex3fv(point1)
        glVertex3fv(point2)
        glVertex3fv(point3)
        glVertex3fv(point4)
        glEnd()

    def drawCube(self) :
        self.drawSquare(BillTable.color_side, BillTable.Cube1, BillTable.Cube2, BillTable.Cube3, BillTable.Cube4)
        self.drawSquare(BillTable.color_side, BillTable.Cube1, BillTable.Cube5, BillTable.Cube6, BillTable.Cube2)
        self.drawSquare(BillTable.color_up, BillTable.Cube2, BillTable.Cube6, BillTable.Cube7, BillTable.Cube3) 
        self.drawSquare(BillTable.color_side, BillTable.Cube4, BillTable.Cube3, BillTable.Cube7, BillTable.Cube8) 
        self.drawSquare(BillTable.color_side, BillTable.Cube4, BillTable.Cube8, BillTable.Cube5, BillTable.Cube1) 
        self.drawSquare(BillTable.color_side, BillTable.Cube8, BillTable.Cube7, BillTable.Cube6, BillTable.Cube5)

    def drawBoundary(self, color, Cube_base1, Cube_base2, Cube_inside1, Cube_inside2, Cube_inside_up1, Cube_inside_up2, Cube_base_up1, Cube_base_up2) :
        self.drawSquare([0.4, 0.31, 0.2, 1], Cube_inside_up1, Cube_inside_up2, Cube_base_up2, Cube_base_up1)
        self.drawSquare(color, Cube_base_up1, Cube_base_up2, Cube_base2, Cube_base1)
        self.drawSquare(color, Cube_inside1, Cube_inside2, Cube_inside_up2, Cube_inside_up1) 
    
    def __init__(self, scale, position):
        self.scale = scale;
        self.position = position;

    def showing(self) :
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glScalef(self.scale[0], self.scale[1], self.scale[2]) # scaling 
        glTranslatef(0.5, -0.5, -0.5) #make to move central 
        self.drawCube()
        self.drawBoundary(BillTable.color_side, BillTable.Cube6, BillTable.Cube2, BillTable.Cube6_inside, BillTable.Cube2_inside, BillTable.Cube6_inside_up, BillTable.Cube2_inside_up, BillTable.Cube6_up, BillTable.Cube2_up)
        self.drawBoundary(BillTable.color_side, BillTable.Cube7, BillTable.Cube6, BillTable.Cube7_inside, BillTable.Cube6_inside, BillTable.Cube7_inside_up, BillTable.Cube6_inside_up, BillTable.Cube7_up, BillTable.Cube6_up)
        self.drawBoundary(BillTable.color_side, BillTable.Cube3, BillTable.Cube7, BillTable.Cube3_inside, BillTable.Cube7_inside, BillTable.Cube3_inside_up, BillTable.Cube7_inside_up, BillTable.Cube3_up, BillTable.Cube7_up)
        self.drawBoundary(BillTable.color_side, BillTable.Cube2, BillTable.Cube3, BillTable.Cube2_inside, BillTable.Cube3_inside, BillTable.Cube2_inside_up, BillTable.Cube3_inside_up, BillTable.Cube2_up, BillTable.Cube3_up)
        glPopMatrix()


## Ball for billTable ##
class Ball:
    def __init__(self, billTableSize, initLoc, color, radius = 1.0) :
        self.loc = np.array([0, billTableSize[1] + radius, initLoc])
        self.vel = np.array([0, 0, 0])
        self.radius = radius
        self.mass = 1.0
        self.force = np.array([0., 0., 0.])
        self.gravity = np.array([0., 0., 0.])
        self.friction = 0.3
        self.color = color
        self.hit = False 
        return

    def colHandlePair(self, other):
        l0 = self.loc
        l1 = other.loc
        m0 = self.mass
        m1 = other.mass
        v0 = self.vel
        v1 = other.vel
        r0 = self.radius
        r1 = other.radius
        R = r0+r1
        N = l0 - l1
        dist = np.linalg.norm(N)
        N = N/dist
        e = 0.1;

        if dist < R : # collision
            penetration = R - dist
            l0 += (0.5+0.5*e)*penetration * N
            l1 -= (0.5+0.5*e)*penetration * N
            Vrel = v0 - v1
            if np.dot(Vrel, N) < 0:
                M = m0 + m1
                vp0 = np.dot(N, v0)
                vp1 = np.dot(N, v1)
                J = (1 + e) * (vp1 - vp0) * m0 * m1 / (m0 + m1)
                v0new =  J / m0 + vp0;
                v1new = -J / m1 + vp1;
                self.vel = self.vel - vp0 * N + v0new * N
                other.vel = other.vel - vp1 * N + v1new * N


    def collisionDetection(self, tableSize):
        if(self.loc[0]<0 and self.loc[0] - self.radius <= tableSize[0]/(-2.0)) :
            delta = tableSize[0] / (-2.0) - self.loc[0] + self.radius
            self.loc[0] = self.loc[0] + delta 
            return True, 0
        elif(self.loc[0]>0 and self.loc[0] + self.radius >= tableSize[0]/2.0) :
            delta = tableSize[0]/2.0 - self.loc[0] -self.radius
            self.loc[0] = self.loc[0] + delta 
            return True, 0
        if(self.loc[2]<0 and self.loc[2] - self.radius <= tableSize[2]/(-2.0)) :
            delta = tableSize[2] / (-2.0) - self.loc[2] + self.radius
            self.loc[2] = self.loc[2] + delta 
            return True, 2 
        elif(self.loc[2] > 0 and self.loc[2]+self.radius >= tableSize[2]/2.0) :
            delta = tableSize[2]/2.0 - self.loc[2] - self.radius
            self.loc[2] = self.loc[2] + delta 
            return True, 2
        return False, 0 

    def collisionHandle(self, index, time) :
        self.vel[index] = -self.vel[index]
        print("==== HANDLE CONLLISION ====")
        self.simulate(time) 

    def draw(self):
        glPushMatrix()
        glColor(self.color) 
        glTranslatef(self.loc[0], self.loc[1], self.loc[2])
        glutSolidSphere(self.radius, 20, 20)
        glPopMatrix()
        if(self.hit) is True :
            self.hitEnd() 

    def hitting(self, f, time) :
        if(self.hit is False): 
            self.force = np.array(f)
            print("hitted") 
            self.hit = True
            acc = self.gravity + self.force / self.mass
            self.vel = self.vel + acc*0.1
            self.loc = self.loc + self.vel*time

    def hitEnd(self):
        self.force = np.array([0., 0., 0.])
        print("hit end") 
        self.hit = False 

    def updateForce(self):
        if(abs(self.vel[0]) > 0.1 and abs(self.vel[2]) > 0.1) :
            print("force updated")
            totalVel = self.vel[0] + self.vel[1] + self.vel[2] 
            if(self.vel[0] > 0) :
                self.force[0] = -self.friction*self.mass
                print("new Force = ", self.force[0])
            elif(self.vel[0] < 0) :
                self.force[0] = self.friction*self.mass
                print("new Force = ", self.force[0])
            if(self.vel[2] > 0) :
                self.force[2] = -self.friction*self.mass
            elif(self.vel[2] < 0) :
                self.force[2] = self.friction*self.mass
        else:
            self.vel = np.array([0., 0., 0.])
            self.force = np.array([0., 0., 0.]) 
            print("yes it stoppped!!!!") 

    def simulate(self, time) :
        self.updateForce()
        print(self.vel[0])
        print("\n") 
        acc = self.gravity + self.force / self.mass
        self.vel = self.vel + acc*time
        self.loc = self.loc + self.vel*time

## initialize object ##
game = myGame(750, 750, "201724515 윤승희 assigment02")
game.grid(True)
table = BillTable(billSize, [0, billSize[1]/2.0, 0])
ball1 = Ball(billSize, 5, [1, 0, 0, 1])
ball2 = Ball(billSize, -5, [0, 0, 1, 1]) 
clock = Timer()
clock.start()
light = Lighting([0, 100, 0, 0])
light.LightSet() 

## toggle setting ##
round = False;
lightON = True;

def draw():
    global angle 
    game.frame()
    drawBackGround()
    if(round is True) : 
        angle = angle + 0.02
    game.setCamera([cameraPos[0]*math.cos(angle) , cameraPos[1], cameraPos[2]*math.sin(angle)], cameraCen, [0, 1, 0])
    table.showing()
    ball1.simulate(clock.getDt())
    insideBillSize = [billSize[0]*0.8, billSize[1]*0.8, billSize[2]*0.8]
    coll, index = ball1.collisionDetection(insideBillSize)
    if(coll) :
        ball1.collisionHandle(index, clock.getDt())
    ball2.simulate(clock.getDt())
    coll, index = ball2.collisionDetection(insideBillSize)
    if(coll) :
        ball2.collisionHandle(index, clock.getDt())
    ball1.colHandlePair(ball2) 
    ball1.draw()
    ball2.draw()
    game.afterframe() 


def key(k, x, y):
    global round
    global cameraDistance
    global cameraPos
    global lightON
    if k is 'n' :
        if(lightON is False) :
            lightON = True
            light.Lighton()
            
    if k is 'f' :
        if(lightON is True) :
            lightON = False
            light.Lightoff()
            
    if k is 'h' :
        randomNum = math.radians(random.random()*360.0) 
        ball1.hitting([50.0*math.sin(randomNum), 0., 50.0*math.cos(randomNum)], clock.getDt())
        randomNum = math.radians(random.random()*360.0)
        ball2.hitting([50.0*math.sin(randomNum), 0., 50.0*math.cos(randomNum)], clock.getDt())
    if k is 'i' : #zoom in 
        if(cameraDistance-1 >= spaceSize - 20):
            cameraDistance = cameraDistance -1
            cameraPos = [cameraDistance, cameraDistance, cameraDistance]
            print("zoom in")
    if k is 'o' : #zoom out 
        if(cameraDistance+1 < spaceSize) :
            cameraDistance = cameraDistance + 1
            cameraPos = [cameraDistance, cameraDistance, cameraDistance]
            print("zoom out")
    if k is 'r' : #camera rotating 
        if(round is False):
            round = True
        else :
            round = False 
        
              

def main() :
    backgroundInit()
    game.start(draw, key)
    
if __name__ == "__main__" :
    main() 
