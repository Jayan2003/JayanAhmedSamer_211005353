from OpenGL.GL import *
from OpenGL.GLU import *


def draw_basket(x_pos):
    glPushMatrix()
    glTranslatef(x_pos, -3.5, -3)

    chest_width = 2.0
    chest_height = 1.0
    chest_depth = 1.2
    lid_height = 0.4 

    dark_blue = (0.0, 0.0, 0.3)  # Very dark blue
    border_color = (1.0, 1.0, 1.0)  # White border 

    # the chest base (solid)
    glColor3f(*dark_blue)
    glBegin(GL_QUADS)
    
    # Front face
    glVertex3f(-chest_width/2, -chest_height/2, chest_depth/2)
    glVertex3f(chest_width/2, -chest_height/2, chest_depth/2)
    glVertex3f(chest_width/2, chest_height/2, chest_depth/2)
    glVertex3f(-chest_width/2, chest_height/2, chest_depth/2)

    # Back face
    glVertex3f(-chest_width/2, -chest_height/2, -chest_depth/2)
    glVertex3f(chest_width/2, -chest_height/2, -chest_depth/2)
    glVertex3f(chest_width/2, chest_height/2, -chest_depth/2)
    glVertex3f(-chest_width/2, chest_height/2, -chest_depth/2)

    # Left face
    glVertex3f(-chest_width/2, -chest_height/2, -chest_depth/2)
    glVertex3f(-chest_width/2, -chest_height/2, chest_depth/2)
    glVertex3f(-chest_width/2, chest_height/2, chest_depth/2)
    glVertex3f(-chest_width/2, chest_height/2, -chest_depth/2)

    # Right face
    glVertex3f(chest_width/2, -chest_height/2, -chest_depth/2)
    glVertex3f(chest_width/2, -chest_height/2, chest_depth/2)
    glVertex3f(chest_width/2, chest_height/2, chest_depth/2)
    glVertex3f(chest_width/2, chest_height/2, -chest_depth/2)

    # Bottom face
    glVertex3f(-chest_width/2, -chest_height/2, -chest_depth/2)
    glVertex3f(chest_width/2, -chest_height/2, -chest_depth/2)
    glVertex3f(chest_width/2, -chest_height/2, chest_depth/2)
    glVertex3f(-chest_width/2, -chest_height/2, chest_depth/2)
    glEnd()

    # the open lid (solid)
    glPushMatrix()
    glTranslatef(0, chest_height/2, 0)
    glRotatef(-30, 1, 0, 0)  # Tilt backward
    glColor3f(*dark_blue)
    glBegin(GL_QUADS)
    # Top face (lid)
    glVertex3f(-chest_width/2, 0, -chest_depth/2)
    glVertex3f(chest_width/2, 0, -chest_depth/2)
    glVertex3f(chest_width/2, lid_height, chest_depth/2)
    glVertex3f(-chest_width/2, lid_height, chest_depth/2)
    glEnd()

    #lid border (wireframe)
    glColor3f(*border_color)
    glBegin(GL_LINE_LOOP)
    glVertex3f(-chest_width/2, 0, -chest_depth/2)
    glVertex3f(chest_width/2, 0, -chest_depth/2)
    glVertex3f(chest_width/2, lid_height, chest_depth/2)
    glVertex3f(-chest_width/2, lid_height, chest_depth/2)
    glEnd()

    glPopMatrix()  # End lid matrix

    # chest base border 
    glColor3f(*border_color)
    glBegin(GL_LINES)
    # Front
    glVertex3f(-chest_width/2, -chest_height/2, chest_depth/2)
    glVertex3f(chest_width/2, -chest_height/2, chest_depth/2)

    glVertex3f(chest_width/2, -chest_height/2, chest_depth/2)
    glVertex3f(chest_width/2, chest_height/2, chest_depth/2)

    glVertex3f(chest_width/2, chest_height/2, chest_depth/2)
    glVertex3f(-chest_width/2, chest_height/2, chest_depth/2)

    glVertex3f(-chest_width/2, chest_height/2, chest_depth/2)
    glVertex3f(-chest_width/2, -chest_height/2, chest_depth/2)

    # Back
    glVertex3f(-chest_width/2, -chest_height/2, -chest_depth/2)
    glVertex3f(chest_width/2, -chest_height/2, -chest_depth/2)

    glVertex3f(chest_width/2, -chest_height/2, -chest_depth/2)
    glVertex3f(chest_width/2, chest_height/2, -chest_depth/2)

    glVertex3f(chest_width/2, chest_height/2, -chest_depth/2)
    glVertex3f(-chest_width/2, chest_height/2, -chest_depth/2)

    glVertex3f(-chest_width/2, chest_height/2, -chest_depth/2)
    glVertex3f(-chest_width/2, -chest_height/2, -chest_depth/2)

    # Connect front and back
    glVertex3f(-chest_width/2, -chest_height/2, chest_depth/2)
    glVertex3f(-chest_width/2, -chest_height/2, -chest_depth/2)

    glVertex3f(chest_width/2, -chest_height/2, chest_depth/2)
    glVertex3f(chest_width/2, -chest_height/2, -chest_depth/2)

    glVertex3f(chest_width/2, chest_height/2, chest_depth/2)
    glVertex3f(chest_width/2, chest_height/2, -chest_depth/2)

    glVertex3f(-chest_width/2, chest_height/2, chest_depth/2)
    glVertex3f(-chest_width/2, chest_height/2, -chest_depth/2)

    glEnd()

    glPopMatrix()