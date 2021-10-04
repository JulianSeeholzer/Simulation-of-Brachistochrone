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
draw_options = pymunk.pygame_util.DrawOptions(pyscreen)   # define draw-function
pygame.display.set_caption('Simulation')  # change title of pygame window
clock = pygame.time.Clock()  # create an in-game clock
pygame_icon = pygame.image.load('Mat_2021_Python_Image_8.png')
pygame.display.set_icon(pygame_icon)  # change icon of pygame window



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


'''Create all physcial objects via pymunk'''
fk = 1

def dynamic_ball(space, pos):  # define function for creating a dynamical pymunk body
    r = 20  # define variable for radius of the pymunk body
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
    r = 20  # define variable for radius of the pymunk body
    body = pymunk.Body(1, 0.01, body_type=pymunk.Body.DYNAMIC)  # create dynamic pymunk body
    body.position = (h[0][0]+r, h[0][1]-r)  # define position of the body
    shape = pymunk.Circle(body, r)  # create shape for body with radius r
    shape.friction = fk  # add kinetic friction to the body to create a rotation
    shape.color = pygame.Color('red')
    space.add(body, shape)  # add body and shape to pymunk space
    return shape


def dynamic_starting_ball2(space):  # define a function for a dynamical body sitting on the top of the Brachistochrone curve
    r = 20 # define variable for radius of the pymunk body
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
        r = 20
        pos_x = int(ball.body.position.x)  # x-position of the pymunk body
        pos_y = int(ball.body.position.y)  # y-position of the pymunk body
        pygame.draw.circle(pyscreen, (255, 0, 0), (pos_x, pos_y), r)  # draw every ball in balls


# create function to draw the startingballs
def visualize_dynamic_startingballs(startingballs):
    for startingball in startingballs:
        r = 20
        pos_x = int(startingball.body.position.x)  # x-position of the pymunk body
        pos_y = int(startingball.body.position.y)  # y-position of the pymunk body
        pygame.draw.circle(pyscreen, (255, 0, 0), (pos_x, pos_y), r)  # draw every startingball in startingballs


'''define functions for the buttons'''
def dynamic_starting_balls():  # define a function that calls the functions which create the balls sitting on top the two cruves
    visualize_dynamic_startingballs(startingballs)
    dynamic_starting_ball1(space)
    dynamic_starting_ball2(space)



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
            balls.append(dynamic_starting_balls())  # append dynamic_ball to balls = []

    '''additions to pygame window'''
    pyscreen.fill((255, 255, 255))  # set background color of the pygame window

    '''call functions needed to '''
    pygame.draw.aalines(pyscreen, (0, 0, 255), False, p, 1)  # draw Brachistochrone (aalines is used to draw an antialiasing line)
    pygame.draw.aalines(pyscreen, (0, 0, 255), False, h, 1)  # draw line
    space.debug_draw(draw_options)  # draw all dynamical objects

    '''create gravity for pymunk space'''
    g = 20 # define a variable g as the current value of the scale button
    space.gravity = (0, g)  # add gravity to pymunk space


    '''updating functions'''
    space.step(1 / 50)  # define rate of updating the state of pymunk space
    pygame.display.update()  # update pygame window
    clock.tick(150)  # set a limit to fps