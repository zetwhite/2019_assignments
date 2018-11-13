from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Background import *
class Camera:

    def __init__(self, fov=60.0, asp=1.0, near=0.1, far=1000.0):
        self.fov = fov
        self.asp = asp
        self.near = near
        self.far = far
        self.eye = [10, 1, 1]
        self.target = [0, 0, 0]
        self.up = [0, 1, 0]



    def applyCamera(self, background):
        if background is not None :
            glDepthMask(GL_FALSE)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
        #    background.drawBackGround()

        glDepthMask(GL_TRUE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.asp, self.near, self.far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.eye[0],self.eye[1],self.eye[2], self.target[0], self.target[1], self.target[2], self.up[0], self.up[1], self.up[2])

    def setLens(self, fov, asp, near, far):
        self.fov = fov
        self.asp = asp
        self.near = near
        self.far = far

    def setPos(self, eye, target, up=[0,0, 1]) : 
        self.eye = eye
        self.target = target
        self.up = up

    def setAsp(self, w, h):
        self.asp = w/h
