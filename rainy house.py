from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 650, 650

rain_speed = 10
num_raindrops = 50
raindrops = []

# Generate random raindrops
for i in range(num_raindrops):
    x = random.randint(-W_Width // 2, W_Width // 2)
    y = random.randint(50, W_Height // 2)
    size = random.randint(9, 15)
    raindrops.append((x, y, size))

bend = 0
r, g, b, s = 0.0, 0.0, 0.0, 0.0
background_colors = [r, g, b, s]
current_color_index = 0

def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def drawShapes():
    scale = 0.8
    # Roof (red triangle)
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Red color
    glVertex2f(5 * scale, 200 * scale)
    glVertex2f(-250 * scale, 5 * scale)
    glVertex2f(250 * scale, 5 * scale)
    glEnd()

    # House body (yellow rectangle)
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    glVertex2f(-250 * scale, 5 * scale)
    glVertex2f(250 * scale, 5 * scale)
    glVertex2f(250 * scale, -250 * scale)
    glVertex2f(-250 * scale, -250 * scale)
    glEnd()

    # Door

    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # White door
    glVertex2f(-80 * scale, -250 * scale)
    glVertex2f(-80 * scale, -100 * scale)
    glVertex2f(10 * scale, -100 * scale)
    glVertex2f(10 * scale, -250 * scale)
    glEnd()

    # Door knob
    glColor3f(0.0, 0.0, 0.0)  # Black color
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(-20 * scale, -175 * scale)
    glEnd()

    # Window (grid window)
    glColor3f(0.0, 0.0, 0.0)  # Black border
    glBegin(GL_LINE_LOOP)
    glVertex2f(100 * scale, -185 * scale)
    glVertex2f(100 * scale, -80 * scale)
    glVertex2f(220 * scale, -80 * scale)
    glVertex2f(220 * scale, -185 * scale)
    glEnd()

    # Grid lines
    glBegin(GL_LINES)
    glVertex2f(160 * scale, -185 * scale)  # Vertical grid line
    glVertex2f(160 * scale, -80 * scale)
    glVertex2f(100 * scale, -132.5 * scale)  # Horizontal grid line
    glVertex2f(220 * scale, -132.5 * scale)
    glEnd()

def draw_rain():
    glColor3f(0.0, 0.0, 1.0) #BLUE RAIN DROPS
    glLineWidth(2)
    glBegin(GL_LINES)
    for x, y, size in raindrops:
        glVertex2f(x, y)
        glVertex2f(x + bend, y - size)
    glEnd()

def keyboardListener(key, x, y):
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global rain_speed, bend

    if key == GLUT_KEY_RIGHT:
        bend += 1
    elif key == GLUT_KEY_LEFT:
        bend -= 1
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global background_colors
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        background_colors[0] += 0.1 #R
        background_colors[1] += 0.1 #G
        background_colors[2] += 0.1 #B
        if 0 <= background_colors[0] <= 1:
            glClearColor(*tuple(background_colors))
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        background_colors[0] -= 0.1
        background_colors[1] -= 0.1
        background_colors[2] -= 0.1
        if 0 <= background_colors[0] < 1:
            glClearColor(*tuple(background_colors))
        glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    draw_rain()
    drawShapes()
    glutSwapBuffers()

def animate():
    glutPostRedisplay()
    global raindrops
    for i in range(len(raindrops)):
        x, y, size = raindrops[i]
        x += bend
        y -= rain_speed
        if y < 50:
            y = W_Height // 2
            x = random.randint(-W_Width // 2, W_Width // 2)
        if y < -W_Height // 2:
            y = W_Height // 2
            x = random.randint(-W_Width // 2, W_Width // 2)
        if x > W_Width // 2:
            x = -W_Width // 2
        elif x < -W_Width // 2:
            x = W_Width // 2
        raindrops[i] = (x, y, size)

def init():
    global wind
    glutInit()
    glutInitWindowSize(500,500)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    wind = glutCreateWindow(b"Rain House")
    glClearColor(*tuple(background_colors))
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

init()
glutMainLoop()




