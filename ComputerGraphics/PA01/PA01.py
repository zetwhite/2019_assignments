# -*- coding: cp949 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

pi = 3.141592
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
POSITION_X = 0
POSITION_Y = 0 
angle = 180
LongDistance = 20
ShortDistance = 15
#For earth 
angle_earth = 0.0
distance_earth = 10
#For pluto 
angle_pluto = 0.0
x_pluto = 0
y_pluto = 0 
r = 10
#For satelite 
slope_satelite = 0
x_satelite = 0
y_satelite = 0
z_satelite = 0
#for Zoom in/out
viewDistance = [40, 40, 40]
#set ViewSatelite
viewSatelite = True
halt = True 



eightTop = [0, 0, 1]
eightBottom = [0, 0, -1]
eightCo1 = [1, 0, 0]
eightCo2 = [0, 1, 0]
eightCo3 = [-1, 0, 0]
eightCo4 = [0, -1, 0] 

tetraCo1 = [0, 0, 0]
tetraCo2 = [-math.sqrt(3)/2, float(1)/2, 0]
tetraCo3 = [0, 1, 0]
tetraCo4 = [-math.sqrt(3)/6, float(1)/2, math.sqrt(6)/3]

CubeCo1 = [0, 0, 0]
CubeCo2 = [0, 1, 0]
CubeCo3 = [0, 1, 1]
CubeCo4 = [0, 0, 1]
CubeCo5 = [-1, 0, 0]
CubeCo6 = [-1, 1, 0]
CubeCo7 = [-1, 1, 1]
CubeCo8 = [-1, 0, 1] 

def drawTriangle(color,point1, point2, point3):
    glBegin(GL_TRIANGLES)
    glColor(color[0], color[1], color[2])
    glVertex3fv(point1)
    glVertex3fv(point2)
    glVertex3fv(point3)
    glEnd()

def drawSquare(color, point1, point2, point3, point4):
    glBegin(GL_QUADS)
    glColor(color[0], color[1], color[2])
    glVertex3fv(point1)
    glVertex3fv(point2)
    glVertex3fv(point3)
    glVertex3fv(point4)
    glEnd() 

def drawEight(size, spin):
    glPushMatrix()
    glRotatef(spin, 0, 0, 1)
    glScalef(size, size, size) 
    color = [1, 1, 0]
    drawTriangle(color, eightTop, eightCo1, eightCo2)
    drawTriangle(color, eightTop, eightCo2, eightCo3)
    drawTriangle(color, eightTop, eightCo3, eightCo4)
    drawTriangle(color, eightTop, eightCo4, eightCo1)
    drawTriangle(color, eightBottom, eightCo2, eightCo1)
    drawTriangle(color, eightBottom, eightCo3, eightCo2)
    drawTriangle(color, eightBottom, eightCo4, eightCo3)
    drawTriangle(color, eightBottom, eightCo1, eightCo4)
    glPopMatrix()

def drawTetrahedron(spin, size) :
    glPushMatrix()
    glRotatef(spin, 0, 0, 1)
    glScalef(size, size, size) 
    glTranslatef(math.sqrt(3)/6, float(1)/2 * (-1), math.sqrt(6)/12*(-1)) 
    color = [1, 1, 1]
    drawTriangle(color, tetraCo1, tetraCo2, tetraCo3)
    drawTriangle(color, tetraCo1, tetraCo4, tetraCo2)
    drawTriangle(color, tetraCo4, tetraCo3, tetraCo2)
    drawTriangle(color, tetraCo1, tetraCo3, tetraCo4)
    glPopMatrix()

def drawCube(selfR, spin, size) :
    glPushMatrix()
    glRotatef(selfR, 1, 0, 0)
    glRotatef(spin, 0, 0, 1)
    glScalef(size, size, size) 
    glTranslatef(0.5, -0.5, -0.5) 
    color = [0, 0.5, 1.0]
    drawSquare(color, CubeCo1, CubeCo2, CubeCo3, CubeCo4)
    drawSquare(color, CubeCo1, CubeCo5, CubeCo6, CubeCo2)
    drawSquare(color, CubeCo2, CubeCo6, CubeCo7, CubeCo3) 
    drawSquare(color, CubeCo4, CubeCo3, CubeCo7, CubeCo8) 
    drawSquare(color, CubeCo4, CubeCo8, CubeCo5, CubeCo1) 
    drawSquare(color, CubeCo8, CubeCo7, CubeCo6, CubeCo5)
    glPopMatrix()

def drawPluto(LongDistance, ShortDistance, angle, size, spin= 0.0):
    global x_pluto, y_pluto, pi
    glColor(1, 1, 0)
    glBegin(GL_LINE_STRIP)
    for i in range(0, 361):
        theta = 2.0*pi*i/360
        x = LongDistance * math.cos(theta)
        y = ShortDistance * math.sin(theta)
        glVertex3f(x, y, 0)
    glEnd()
    aR = pi*angle/180
    x_pluto = LongDistance*math.cos(aR)
    y_pluto = ShortDistance*math.sin(aR)
    glTranslatef(x_pluto, y_pluto, 0)
    RealAngle = math.acos(x_pluto/math.sqrt(x_pluto**2 + y_pluto**2))
    RealAngle = RealAngle*180.0/pi
    if aR > pi and aR < pi*2 :
        RealAngle = 360.0 - RealAngle 
    drawEight(size, RealAngle)

def drawEarth(distance, angle, size, spin = 0.0, slope = 0.0, selfR= 0.0) :
    global angle_earth 
    glColor3f(0, 0.5, 1.0)
    glRotatef(slope, 1, 0, 0) 
    glBegin(GL_LINE_STRIP)
    for i in range (0, 361):
        theta = 2.0* 3.141592* i /360
        x = distance * math.cos(theta)
        y = distance * math.sin(theta)
        glVertex3f(x, y, 0)
    glEnd()
    glRotatef(angle, 0, 0, 1)
    glTranslatef(distance, 0, 0) 
    drawCube(selfR, spin, size)


def drawSatelite(distance, angle, size, spin= 0.0, slope = 0.0) :
    global pi, x_satelite, y_satelite, z_satelite, angle_earth, distance_earth 

    glColor(1, 1, 1)
    glRotatef(slope, 1, 0, 0)
    glBegin(GL_LINE_STRIP)
    for i in range(0, 361) :
        theta = 2.0*pi*i/360
        x = distance * math.cos(theta) 
        y = distance * math.sin(theta) 
        glVertex3f(x, y, 0)
    glEnd()
    glRotatef(angle, 0, 0, 1)
    glTranslatef(distance, 0, 0)
    angle_r = angle*pi/180.0
    angle_e_r = angle_earth*pi/180.0 
    slope_r = slope*pi/180.0
    cos = math.cos(angle_r)
    sin = math.sin(angle_r)
    cosA = math.cos(slope_r)
    sinA = math.sin(slope_r)
    x_satelite0 = distance*cosA + distance_earth 
    y_satelite0 = cos*sinA*distance
    z_satelite = sin*sinA*distance
    x_satelite = x_satelite0*math.cos(angle_earth_r) - y_satelite0*math.sin(angle_earth_r)
    y_satelite = x_satelite0*math.sin(angle_earth_r) + y_satelite0*math.cos(angle_earth_r)
    
    drawTetrahedron(spin, size)


def drawScene() :
    global angle, angle_earth, angle_pluto, slope_satelite, r, pi, halt
     
    #sun
    glColor3f(1, 0, 0)
    glutSolidSphere(1.0, 20, 20)

    if(not halt) : 
        angle += 1
        angle %=361*16

    #명왕성
    glPushMatrix()
    angle_pluto = 1/4.0*angle + 40
    drawPluto(20, 15, angle_pluto, 1, angle_pluto*8)
    glPopMatrix()
    
    #earth
    glPushMatrix()
    glColor3f(0, 0.5, 1.0)
    angle_earth = angle
    drawEarth(distance_earth, angle_earth, 1, angle_earth*4, 0, 15)

    #인공위성
    drawSatelite(r/3, angle_earth, 1, 0, angle_earth/12) 
    glPopMatrix()

def MyKeyBoard(key,x,y):
    global viewDistance, viewSatelite, halt
    if key == '+': # Zoom IN
        if viewDistance[0] > 5:
            viewDistance[0] -= 5
            viewDistance[1] -= 5
            viewDistance[2] -= 5
    elif key == '-': # Zoom OUT
        if viewDistance[0] < 70:
            viewDistance[0] += 5
            viewDistance[1] += 5
            viewDistance[2] += 5
    elif key == 't':
        if viewSatelite == True:
            viewSatelite = False
        else:
            viewSatelite = True
    elif key == 'q':
        exit(0)
    elif key == 'h':
        if halt == True:
            halt = False
        else :
            halt = True 
    glutPostRedisplay()
    return 0

def disp() :
    global r, angle_earth_r, angle_earth, x_pluto, y_pluto, distance_earth
    global x_satelite, y_satelite, z_satelite, viewDistance, viewSatelite 

    glClear(GL_COLOR_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, 1.0, 2, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #3/4분면 화면 - 명왕성에서 바라보는 장면
    glViewport(POSITION_X, POSITION_Y, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    glPushMatrix()
    angle_earth_r = angle_earth/180.0*pi
    gluLookAt(x_pluto, y_pluto, 0, distance_earth*math.cos(angle_earth_r), distance_earth*math.sin(angle_earth_r), 0, 0, 0, 1)
    drawScene()
    glPopMatrix()

    #4/4분할 화면 - 지구에서 바라보는 장면 
    glViewport(POSITION_X+WINDOW_WIDTH/2, POSITION_Y, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    glPushMatrix()
    angle_earth_r = angle_earth/180.0*pi
    if(viewSatelite) : 
        gluLookAt(distance_earth*math.cos(angle_earth_r), distance_earth*math.sin(angle_earth_r), 0, 0, 0, 0, 0, 0, 1)
    else : 
        gluLookAt(x_satelite, y_satelite, z_satelite, distance_earth*math.cos(angle_earth_r), distance_earth*math.sin(angle_earth_r), 0, 0, 0, 1)
    drawScene()
    glPopMatrix()

    #2/4분할 화면 - 전체 조명
    glViewport(POSITION_X, POSITION_Y + WINDOW_HEIGHT/2, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    glPushMatrix()
    gluLookAt(viewDistance[0], viewDistance[1], viewDistance[2], 0, 0, 0, 0, 0, 1)
    drawScene()
    glPopMatrix()

    #1/4분할 화면 - 태양이 12시 방향으로 바라봄 
    glViewport(POSITION_X+WINDOW_WIDTH/2, POSITION_Y + WINDOW_HEIGHT/2, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    glPushMatrix()
    gluLookAt(0, 0, 0, 1, 0, 0, 0, 0, 1)
    drawScene()
    glPopMatrix()

    glFlush()


def main():
    #windowing
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(POSITION_X, POSITION_Y)
    glutCreateWindow("201724515 윤승희 programming Assignmnet01")

    glClearColor(0, 0.0, 0.0, 0)

    #register call backs
    glutDisplayFunc(disp)
    glutKeyboardFunc(MyKeyBoard)
    glutIdleFunc(disp)

    glutMainLoop()

if __name__ == "__main__":
    main() 




