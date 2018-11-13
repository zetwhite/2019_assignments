import time
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Camera import *
from Lighting import *
from Timer import *
from Scene import *
from Background import *

class Graphics:
    def drawGrid(self, numberOfLines, angle=0, axis=[1,0,0]):
        glPushMatrix();
        glRotatef(angle, axis[0], axis[1], axis[2]);
        glDisable(GL_LIGHTING)
        glColor3f(0.5, 0.5, 0.5)
        for x in range(0, numberOfLines):
            glBegin(GL_LINES)
            glVertex3f(x-numberOfLines/2.0, 0, -numberOfLines/2.0)
            glVertex3f(x-numberOfLines/2.0, 0, numberOfLines/2.0)
            glEnd()

        for z in range(0, numberOfLines):
            glBegin(GL_LINES)
            glVertex3f(-numberOfLines/2.0, 0, z-numberOfLines/2.0)
            glVertex3f(numberOfLines/2.0, 0, z-numberOfLines/2.0)
            glEnd()
        glEnable(GL_LIGHTING)
        glPopMatrix();

    def drawBall(self, pos, radius=1.0):
        glPushMatrix()
        glColor(0.5, 0.0, 0.0, 1.0)
        glTranslatef(pos[0], pos[1], pos[2])
        glutSolidSphere(radius, 20, 20)
        glPopMatrix()


class Game(object):
    def __init__(self, w, h, title):
        self.cam = Camera(60., w/h, 0.1, 1000.0)
        self.cam.setPos([10,5,10], [0,0,0], [0, 1, 0])
        self.timer = Timer()
        self.gridMode = False
        self.gridAngle = 0
        self.gridAxis = [1,0,0]

        self.graphics = Graphics()
        #self.lighting = Lighting()
        self.scene = Scene()
        self.background = Background()

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(w, h)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(title)
        glClearColor(0.25, 0.25, 0.25, 1.0)
        glEnable(GL_DEPTH_TEST)
        #self.lighting.LightSet()


    def setBackground(self, filename1, filename2, filename3, filename4):
        self.background.initMy(filename1, filename2, filename3, filename4)

    #def setLightPosition(self, pos):
    #    self.lighting.SetLightPos(pos) 

    def reshape(self, w, h):
        self.cam.setAsp(w,h)
        glViewport(0,0, w,h)

    def grid(self, option):
        self.gridMode = option

    def rotateGrid(self, angle, axis):
        self.gridAngle = angle
        self.gridAxis = axis


    def timerStart(self):
        self.timer.start()

    def timerStop(self):
        self.timer.stop()

    def timerReset(self):
        self.timer.reset()


    def getDt(self):
        return self.timer.getDt()

    def getEt(self):
        return self.timer.getEt()

    def frame(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.cam.applyCamera(self.background)
        #self.lighting.LightPosition()
        if self.gridMode :
            self.graphics.drawGrid(100, self.gridAngle, self.gridAxis)

    def afterFrame(self):
        self.scene.draw()
        glFlush()

    def start(self, displayCallback, keyCallback):
        glutDisplayFunc(displayCallback)
        glutIdleFunc(displayCallback)
        glutKeyboardFunc(keyCallback)
        glutReshapeFunc(self.reshape)
        glutMainLoop()

    def drawBall(self, pos, radius=1.0):
        self.graphics.drawBall(pos, radius)

    def cameraAt(self, eye, target, up=[0,1,0]):
        self.cam.setPos(eye, target, up)

    def addObject(self, name, type):
        obj = VisualObj()
        obj.setNameAndType(name, type)
        self.scene.opaqueChildren.add(obj)
        return obj

    def addSphere(self, name):
        return self.addObject(name, 0)

    def addCube(self, name, scale, pos):
        return self.addObject(name, 1)

    def addTransparentObject(self, name, type):
        obj = VisualObj()
        obj.setNameAndType(name, type)
        self.scene.transChildren.add(obj)
        return obj

    def addTransparentSphere(self, name):
        return self.addTransparentObject(name, 0)


    def addTransparentCube(self, name):
        return self.addTransparentObject(name, 1)
    
