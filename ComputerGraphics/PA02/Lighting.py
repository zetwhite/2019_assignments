# -*- coding: cp949 -*-
from OpenGL.GL import *
from OpenGL.GLU import *

class Lighting:
    def __init__(self, position1):
        self.Ld = [1., 1., 1., 1.]
        self.Ls = [1., 1., 1., 1.]
        self.La = [1., 1., 1., 1.] 
        self.Md = [1., 1., 1., 1.]
        self.Ms = [1., 1., 1., 1.]
        self.Ma = [0., 0., 0., 1.]
        self.Lpos1 = position1
        self.shininess = [120]


    def LightSet(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.Ld)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.Ls)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.La)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.Md)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.Ms)
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.Ma)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.shininess)
		
		
    def LightPosition(self):
	glLightfv(GL_LIGHT0, GL_POSITION, self.Lpos2)

    def Lightoff(self):
        glDisable(GL_LIGHT0)

    def Lighton(self):
        glEnable(GL_LIGHT0) 