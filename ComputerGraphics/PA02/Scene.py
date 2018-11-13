import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

class VisualObj :
    def __init__(self):
        self.T = np.array([0., 0., 0.]) # translation
        self.R = np.array([0., 0., 0.]) # yaw, roll, pitch
        self.S = np.array([1., 1., 1.]) # x-, y-, z-scale

        self.col = np.array([1., 1., 1., 1.])
        self.name = b"None"
        self.type = b"None"
        self.children = set([])

    def translate(self, x,y,z):
        self.T = np.array([x,y,z])
    def rotate(self, yaw, pitch, roll):
        self.R = np.array([yaw, pitch, roll])
    def scale(self, x,y,z):
        self.S = np.array([x,y,z])
    def color(self, r, g, b, a=1.0):
        self.col = np.array([r,g,b,a])

    def setNameAndType(self, name, type):
        self.name = name
        self.type = type

    def addChild(self, name, type):
        obj = VisualObj()
        obj.setNameAndType(name, type)
        self.children.add(obj)
        return obj

    def find(self, name):
        if self.name is name :
            return self
        else :
            for e in self.children :
                found = e.find(name)
                if found is not None :
                    return found
        return None

    def drawObject(self):

        glColor4fv(self.col)
        glPushMatrix()

        if self.type is 0 :
            glTranslatef(self.T[0], self.T[1], self.T[2])
            glRotatef(self.R[0], 0, 1, 0) # yaw
            glRotatef(self.R[1], 0, 0, 1) # roll
            glRotatef(self.R[2], 1, 0, 0) # pitch
            glPushMatrix()
            glScalef(self.S[0], self.S[1], self.S[2])
            glutSolidSphere(1.0, 20, 20)
            glPopMatrix()

        elif self.type is 1 :
            glTranslatef(self.T[0], self.T[1], self.T[2])
            glRotatef(self.R[0], 0, 1, 0)  # yaw
            glRotatef(self.R[1], 0, 0, 1)  # roll
            glRotatef(self.R[2], 1, 0, 0)  # pitch
            glPushMatrix()
            glScalef(self.S[0], self.S[1], self.S[2])
            glutSolidCube(1.0)
            glPopMatrix()

        for child in self.children :
            child.drawObject()

        glPopMatrix()


class Scene :
    def __init__(self):
        self.lights = set([])
        self.opaqueChildren = set([])
        self.transChildren = set([])

    def addObject(self, name, type, scale, pos):
        obj = VisualObj()
        obj.setNameAndType(name, type)
        self.opaqueChildren.add(obj)
        self.S = scale
        self.T = pos 
        return obj

    def addTransparentObject(self, name, type):
        obj = VisualObj()
        obj.setNameAndType(name, type)
        self.transChildren.add(obj)
        return obj

    def find(self, name):
        for obj in self.opaqueChildren:
            found = obj.find(name)
            if found is not None :
                return found

        for obj in self.transChildren:
            found = obj.find(name)
            if found is not None:
                return found

        return None


    def draw(self):

        glEnable(GL_LIGHTING)
        glPushMatrix()
        for obj in self.opaqueChildren :
            obj.drawObject()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        for obj in self.transChildren :
            obj.drawObject()
        glDisable(GL_BLEND)
        glPopMatrix()
        
