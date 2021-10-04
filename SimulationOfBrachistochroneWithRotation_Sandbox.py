import pygame
import pymunk
import pymunk.pygame_util
import os
import ctypes
import tkinter as tk
from tkinter import *
import numpy as np
from scipy.optimize import newton


'''initiating pygame'''
pyscreen_x = 1250
pyscreen_y = 500
ctypes.windll.user32.SetProcessDPIAware()  # looks that python knows which resolution the CPU has
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pyscreen_x, pyscreen_y)  # setting the position of the pygame window to (pyscreen_x, pyscreen_y)
pygame.init()  # initiating pygame
pyscreen = pygame.display.set_mode((2000, 1200))  # create pygame window
draw_options = pymunk.pygame_util.DrawOptions(pyscreen)
pygame.display.set_caption('Simulation')  # change title of pygame window
clock = pygame.time.Clock()  # create an in-game clock
pygame_icon = pygame.image.load('Mat_2021_Python_Image_8.png')
pygame.display.set_icon(pygame_icon)  # change icon of pygame window


'''embedding the pygame window in a tkinter window'''
ctypes.windll.user32.SetProcessDPIAware()  # check the resolution of the CPU
tkscreen = tk.Tk()  # create a tkinter window
tkscreen.title('Regulation of Parameters')  # change title of the tkinter window
tkscreen.geometry('600x1202+620+428')  # define size and position of the tkinter window
tkscreen.configure(bg='white')  # define background color of the tkinter window
os.environ['SDL_VIDEODRIVER'] = 'windib'  # get access of operating system parameters
tkinter_icon = PhotoImage(file = "Mat_2021_Python_Image_8.png")
tkscreen.iconphoto(False, tkinter_icon)  # change icon of tkinter window


'''Create a Space (Note: gravity is created in 
the main while loop so it gets updated every time 
the tkinter scales and entries are updated)'''
space = pymunk.Space()  # create a pymunk space (area in which physics will be active)



'''Make an Array p with all the points that approximate 
the Brachistochrone Curve. (Note: The coordinates are scaled by a 
factor k so they can be used directly as coordinates of the created window.)'''
a, b = 1, 0.65
N = 200
k = 700

def f(phi):
    return b / a - (1 - np.cos(phi)) / (phi - np.sin(phi))

phi_end = newton(f, np.pi / 2)
phi = np.linspace(0, phi_end, N)
R = b / (1 - np.cos(phi_end))
x = k * (R * (phi - np.sin(phi))) + 1000
y = k * ((R * (1 - np.cos(phi)))) + 400
u = k * (R * (phi - np.sin(phi)))
v = k * (R * (1 - np.cos(phi)))


p = []
for obj in range(len(x)):
    q = [x[obj], y[obj]]
    p.append(q)


'''Make an Array Q with all points that define the line'''
t = np.linspace(y[0], y[N-1], N)
x = ((u[N-1])/(v[N-1])) * t - 300
y = t


h = []
for point_l in range(len(x)):
    q = [x[point_l], y[point_l]]
    h.append(q)


'''create entry button for defining value of the ball radius'''
r0 = tk.StringVar()
r0.set('20')
entry_r = tk.Entry(tkscreen, bg='white', fg='black', textvariable=r0, bd=10)
entry_r.pack()
entry_r.place(x=140, y=750)


'''Create all physcial objects via pymunk'''
fk = 1

def dynamic_ball(space, pos):  # define function for creating a dynamical pymunk body
    r = float(entry_r.get())  # define variable for radius of the pymunk body
    body = pymunk.Body(1, 0.01, body_type=pymunk.Body.DYNAMIC)  # create a dynamic pymunk body
    body.position = pos  # define position of body
    shape = pymunk.Circle(body, r)  # create a shape for body with radius r
    shape.color = pygame.Color('red')
    shape.friction = fk  # add kinetic friction to the body to create a rotation
    space.add(body, shape)  # add body and shape to pymunk space
    return shape


def static_Brachistochrone(space, i):  # define function for creating the Brachistochrone curve as a static pymunk body
    body = pymunk.Body(body_type=pymunk.Body.STATIC)  # create a static pymunk body
    shape = pymunk.Segment(body, (p[i][0], p[i][1]), (p[i + 1][0], p[i + 1][1]), 0)   # create a shape for body (draw line segments between the points that define the Brachistochrone)
    shape.friction = fk  # add kinetic friction to the body to create a rotation
    space.add(body, shape)  # add body and shape to pymunk space
    return shape


def static_line(space, i):  # define function for creating a inclined line as a static pymunk body
    body = pymunk.Body(body_type=pymunk.Body.STATIC)  # create static pymunk body
    shape = pymunk.Segment(body, (h[i][0], h[i][1]), (h[i + 1][0], h[i + 1][1]), 0)  # create a shape for body
    shape.friction = fk  # add kinetic friction to the body to create a rotation
    space.add(body, shape)  # add body and shape to pymunk space
    return shape


def dynamic_starting_ball1(space):  # define a function for a dynamical body sitting on the top of the inclined line
    r = float(entry_r.get())  # define variable for radius of the pymunk body
    body = pymunk.Body(1, 0.01, body_type=pymunk.Body.DYNAMIC)  # create dynamic pymunk body
    body.position = (h[0][0]+r, h[0][1]-r)  # define position of the body
    shape = pymunk.Circle(body, r)  # create shape for body with radius r
    shape.friction = fk  # add kinetic friction to the body to create a rotation
    shape.color = pygame.Color('red')
    space.add(body, shape)  # add body and shape to pymunk space
    return shape


def dynamic_starting_ball2(space):  # define a function for a dynamical body sitting on the top of the Brachistochrone curve
    r = float(entry_r.get())  # define variable for radius of the pymunk body
    body = pymunk.Body(1, 0.01, body_type=pymunk.Body.DYNAMIC)  # create dynamic pymunk body
    body.position = (p[0][0]+r, p[0][1]-r)  # define position of the body
    shape = pymunk.Circle(body, r)  # create shape for body with radius r
    shape.friction = fk  # add kinetic friction to the body to create a rotation
    shape.color = pygame.Color('red')
    space.add(body, shape)  # add body and shape to pymunk space
    return shape


'''function for visualizing the Ball with pygame'''
# create needed arrays
balls = []
startingballs = []
startingballs.append(dynamic_starting_ball1(space))
startingballs.append(dynamic_starting_ball2(space))


# create the function to draw the dynamicballs
def visualize_dynamic_ball(balls):
    for ball in balls:
        r = float(entry_r.get())  # set the radius of the ball to the value in the entry
        pos_x = int(ball.body.position.x)  # x-position of the pymunk body
        pos_y = int(ball.body.position.y)  # y-position of the pymunk body
        pygame.draw.circle(pyscreen, (255, 0, 0), (pos_x, pos_y), r)  # draw every ball in balls


# create function to draw the startingballs
def visualize_dynamic_startingballs(startingballs):
    for startingball in startingballs:
        r = float(entry_r.get())  # set the radius of the ball to the value in the entry
        pos_x = int(startingball.body.position.x)  # x-position of the pymunk body
        pos_y = int(startingball.body.position.y)  # y-position of the pymunk body
        pygame.draw.circle(pyscreen, (255, 0, 0), (pos_x, pos_y), r)  # draw every startingball in startingballs


'''define functions for the buttons'''
def dynamic_starting_balls():  # define a function that calls the functions which create the balls sitting on top the two cruves
    visualize_dynamic_startingballs(startingballs)
    dynamic_starting_ball1(space)
    dynamic_starting_ball2(space)

def gravity_off():  # define a function to turn gravity off
    scale_g.set(0)  # set the value of scale_g to 0

def gravity_on():  # define a function to turn gravity on
    scale_g.set(20)  # set the value of scale_g to 20


'''create buttons and sliders'''
scale_g = tk.Scale(tkscreen, bg='white', fg='black', from_=0, to=100, orient=tk.HORIZONTAL, length=200, bd=10)  # create a tkinter scale
scale_g.config(highlightbackground='white')  # define border color
scale_g.pack()  # add the scale to the tkinter window
scale_g.place(x=107, y=387)  # define absolute position of the scale

label_g_off_image = PhotoImage(file='Mat_2021_Python_Image_5.1.png')  # define an image for button
label_g_off = Button(tkscreen, bg='white', image=label_g_off_image, bd=0, command=gravity_off)  # create a tkinter button
label_g_off.pack()  # add the button to the tkinter window
label_g_off.place(x=380, y=320)  # define absolute position of the button

label_g_on_image = PhotoImage(file='Mat_2021_Python_Image_4.1.png')  # define an image for button
label_g_on = Button(tkscreen, bg='white', image=label_g_on_image, bd=0, command=gravity_on)  # create a tkinter button
label_g_on.pack()  # add the button to the tkinter window
label_g_on.place(x=380, y=410)  # define absolute position of the button

label_startingballs_image = PhotoImage(file='Mat_2021_Python_Image_6.1.png')  # define an image for button
label_startingballs = Button(tkscreen, bg='white', image=label_startingballs_image, bd=0, command=dynamic_starting_balls)  # create a tkinter button
label_startingballs.pack()  # add the button to the tkinter window
label_startingballs.place(x=70, y=980)  # define absolute position of the button

'''create labels for optimizing the GUI'''
label_g_strength_image = PhotoImage(file='Mat_2021_Python_Image_3.1.png')  # define an image for label
label_g_strength = tk.Label(tkscreen, bg='white', image=label_g_strength_image)  # create a tkinter label
label_g_strength.pack()  # add label to the tkinter window
label_g_strength.place(x=70, y=320)  # define absolute position of the label

label_g_image = PhotoImage(file='Mat_2021_Python_Image_1.1.png')  # define an image for label
label_g = tk.Label(tkscreen, bg='white', image=label_g_image)  # create a tkinter label
label_g.pack()   # add label to the tkinter window
label_g.place(x=70, y=230)  # define absolute position of the label

label_r_image = PhotoImage(file='Mat_2021_Python_Image_2.1.png')  # define an image for label
label_r = tk.Label(tkscreen, bg='white', image=label_r_image)  # create a tkinter label
label_r.pack()   # add label to the tkinter window
label_r.place(x=70, y=660)  # define absolute position of the label

label_title_image = PhotoImage(file='Mat_2021_Python_Image_7.1.png')  # define an image for label
label_title = tk.Label(tkscreen, bg='white', image=label_title_image)  # create a tkinter label
label_title.pack()   # add label to the tkinter window
label_title.place(x=70, y=30)  # define absolute position of the label


'''create arrays needed to draw the curves'''
Brachistochrone = []  # define array for Brachistochrone curve
for i in range(len(p)):
    try:
        Brachistochrone.append(static_Brachistochrone(space, i))
    except:
        print('Last point of Brachistochrone reached')


line = []  # define array for inclined line
for i in range(len(h)):
    try:
        line.append(static_line(space, i))
    except:
        print('Last point of line reached')



'''Control that game runs and visualize all objects with pygame'''
while True:  # game loop
    for event in pygame.event.get():  # checking for user input
        if event.type == pygame.QUIT:  # check for input to close the game
            pygame.quit()  # quit game
            sys.exit()  # close window
        if event.type == pygame.MOUSEBUTTONDOWN:  # check if mouse is clicked
            balls.append(dynamic_ball(space, event.pos))  # append dynamic_ball to balls = []

    '''additions to pygame window'''
    pyscreen.fill((255, 255, 255))  # set background color of the pygame window

    '''call functions needed to '''
    pygame.draw.aalines(pyscreen, (0, 0, 255), False, p, 1)  # draw Brachistochrone (aalines is used to draw an antialiasing line)
    pygame.draw.aalines(pyscreen, (0, 0, 255), False, h, 1)  # draw line
    space.debug_draw(draw_options)

    '''create gravity for pymunk space'''
    g = Scale.get(scale_g)  # define a variable g as the current value of the scale button
    space.gravity = (0, g)  # add gravity to pymunk space


    '''updating functions'''
    space.step(1 / 50)  # define rate of updating the state of pymunk space
    pygame.display.update()  # update pygame window
    tkscreen.update()  # update tkinter window
    clock.tick(150)  # set a limit to fps