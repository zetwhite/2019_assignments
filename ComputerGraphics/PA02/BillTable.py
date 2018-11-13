from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

class BillTable:
    def __init__(self, scale, position, color):
        self.color = color; 
        self.scale = scale;
        self.position = position;
        glPushMatrix()
        glcolor3fv(self.color) 
        glTranslatef(self.position[0], self.postion[1], self.position[2])
        glScalef(self.scale[0], self.scale[1], self.scale[2])
        glutSolidCube(1.0)
        glPopMatrix() 
        
