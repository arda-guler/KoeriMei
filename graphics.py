import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

from ui import *
from math_utils import *

def drawOrigin():
    glBegin(GL_LINES)
    glColor(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(1000,0,0)
    glColor(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,1000,0)
    glColor(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1000)
    glEnd()

def drawPoints(points):

    for p in points:
        glColor(p.color[0], p.color[1], p.color[2])
        
        glPushMatrix()
        glTranslatef(p.pos.x, p.pos.y, p.pos.z)

        glBegin(GL_POINTS)
        glVertex3f(0, 0, 0)
        glEnd()

        glPopMatrix()

def drawPoint2D(x, y, color, camera):
    glPushMatrix()

    glTranslate(-camera.pos.x,
                -camera.pos.y,
                -camera.pos.z)
    
    glColor(color[0], color[1], color[2])

    glBegin(GL_POINTS)

    x1 = x * 100
    y1 = y * 100

    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])

    glEnd()
    
    glPopMatrix()

def drawLine2D(x1, y1, x2, y2, color, camera):
    glPushMatrix()
    glTranslate(-camera.pos.x,
                -camera.pos.y,
                -camera.pos.z)
    
    glColor(color[0], color[1], color[2])
    
    glBegin(GL_LINES)

    x1 = x1 * 100
    y1 = y1 * 100
    x2 = x2 * 100
    y2 = y2 * 100
    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])
    
    glVertex3f((x2) * camera.get_orient()[0][0] + (y2) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x2) * camera.get_orient()[0][1] + (y2) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x2) * camera.get_orient()[0][2] + (y2) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])
    glEnd()
    glPopMatrix()

def drawRectangle2D(x1, y1, x2, y2, color, camera):
    drawLine2D(x1, y1, x2, y1, color, camera)
    drawLine2D(x1, y1, x1, y2, color, camera)
    drawLine2D(x2, y1, x2, y2, color, camera)
    drawLine2D(x1, y2, x2, y2, color, camera)

def drawEarthGlobe(globe, pos, rot, scale, color):
    
    glPushMatrix()
    
    glTranslatef(pos[0], pos[1], pos[2])

    if rot:
        glRotatef(rot[0], rot[1], rot[2], rot[3])

    if scale:
        glScalef(scale[0], scale[1], scale[2])
        
    glColor(color[0], color[1], color[2])

    glPolygonMode(GL_FRONT, GL_LINE)
    glBegin(GL_LINE_STRIP)
    for vertex_i in globe.model:
        glVertex3f(vertex_i.x, vertex_i.y, vertex_i.z)
    glEnd()

    for i_phi in range(36):
        glBegin(GL_LINE_STRIP)
        for i_theta in range(36):
            vertex = globe.model[i_theta * 36 + i_phi]
            glVertex3f(vertex.x, vertex.y, vertex.z)
        glEnd()

    glPopMatrix()

def drawSettlements(settlements, cam, label=True, label_offset=0.2):
    glPushMatrix()
    
    for stmnt in settlements:

        glColor(0,1,1)
        if stmnt.pop > 10E6:
            glPointSize(20)
        elif stmnt.pop > 3E6:
            glPointSize(10)
        elif stmnt.pop > 0.5E6:
            glPointSize(5)
        else:
            glPointSize(3)

        glBegin(GL_POINTS)
        glVertex3f(stmnt.cartesian.x, stmnt.cartesian.y, stmnt.cartesian.z)
        glEnd()

    glPopMatrix()

    if label:
        for stmnt in settlements:
            if world2cam([stmnt.cartesian.x, stmnt.cartesian.y, stmnt.cartesian.z], cam):
                label_render_start = world2cam([stmnt.cartesian.x, stmnt.cartesian.y, stmnt.cartesian.z], cam)
                label_render_start[0] += label_offset
                label_render_start[1] += label_offset * 3
                render_AN(stmnt.name, (0,1,1), label_render_start, cam)

                label_render_start[1] -= label_offset * 3.5
                render_AN(stmnt.get_pop_str(), (0,1,1), label_render_start, cam, 0.06)

def drawQuakes(EQlist):
    glPushMatrix()
    
    for EQ in EQlist:

        if EQ.mag > 6:
            glColor(1,0,1)
            glPointSize(7)
        elif EQ.mag > 4:
            glColor(1,0,0)
            glPointSize(5)
        elif EQ.mag > 2:
            glColor(1,0.65,0)
            glPointSize(2)
        else:
            glColor(0.65, 1, 0)

        glBegin(GL_POINTS)
        glVertex3f(EQ.cartesian.x, EQ.cartesian.y, EQ.cartesian.z)
        glEnd()

    glPopMatrix()

