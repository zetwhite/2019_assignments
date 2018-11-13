from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

#my 
# install Pilllow package, then you can use PIL
from PIL import Image
import numpy as np

class Background :
    
    def computeNormal(self, p1, p2, p3) :
        u = np.array([p2[i] - p1[i] for i in range(0, 3)])
        v = np.array([p3[i] - p1[i] for i in range(0, 3)])
        N = np.cross(u, v)
        N = N / np.linalg.norm(N)
        return N 
    
    def __init__(self):
        self.img = None
        self.img_data = None
        self.ntex = 5
        #self.texArr = glGenTextures(self.ntex)
        self.CubeCo1 = [6, 6, 6]
        self.CubeCo2 = [6, -6, 6]
        self.CubeCo3 = [6, -6, -6]
        self.CubeCo4 = [6, 6, -6]
        self.CubeCo5 = [-6, -6, -6]
        self.CubeCo6 = [-6, -6, 6]
        self.CubeCo7 = [-6, 6, 6]
        self.CubeCo8 = [-6, 6, -6] 

    def initMy(self, filename1, filename2, filename3, filename4) :
        self.texArr = glGenTextures(self.ntex)
        self.setTexture(self.texArr, 0, filename1, GL_RGB)
        self.setTexture(self.texArr, 1, filename2, GL_RGB)
        self.setTexture(self.texArr, 2, filename3, GL_RGB)
        self.setTexture(self.texArr, 3, filename4, GL_RGB)
        glEnable(GL_TEXTURE_2D) 

    def loadImage(self, filename) :
        self.img = Image.open(filename)
        self.img_data = np.array(list(self.img.getdata()), np.uint8)
        return self.img.size[0], self.img.size[1], self.img_data 
        

    def setTexture(self, textArr, idx, fileName, option) : 
        imgW, imgH, myImage = self.loadImage(fileName)
        print(fileName)
        print(imgW, imgH, myImage)
        glBindTexture(GL_TEXTURE_2D, self.texArr[idx]);
        print(idx) 
        print(self.texArr[idx])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, imgW, imgH, 0, option, GL_UNSIGNED_BYTE, myImage)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP) 
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def drawSquare(self, point1, point2, point3, point4, idx):
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glColor3f(1, 1, 1) 
        glBindTexture(GL_TEXTURE_2D, self.texArr[idx]) 
        glBegin(GL_QUADS)
        N = self.computeNormal(point1, point2, point3)
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
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING) 

    def drawBackGround(self):
        print("binding")
        glPushMatrix()
       # glBindTexture(GL_TEXTURE_2D, self.texArr[0])
       # print(self.texArr[0]) 
        self.drawSquare(self.CubeCo2, self.CubeCo1, self.CubeCo4, self.CubeCo3, 0)
    
        #glBindTexture(GL_TEXTURE_2D, self.texArr[1])
        #print(self.texArr[1])
        self.drawSquare(self.CubeCo1, self.CubeCo7, self.CubeCo8, self.CubeCo4, 1)

        #glBindTexture(GL_TEXTURE_2D, self.texArr[3])
        #print(self.texArr[2])
        self.drawSquare(self.CubeCo7, self.CubeCo6, self.CubeCo5, self.CubeCo8, 3)

        #glBindTexture(GL_TEXTURE_2D, self.texArr[2])
        #print(self.texArr[3])
        self.drawSquare(self.CubeCo6, self.CubeCo2, self.CubeCo3, self.CubeCo5, 2)
        glPopMatrix()
        
