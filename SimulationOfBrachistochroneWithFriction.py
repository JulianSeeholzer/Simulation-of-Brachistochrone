import pygame
import pymunk
import os
import ctypes
import tkinter as tk
from tkinter import *
import numpy as np
from scipy.optimize import newton
import matplotlib
matplotlib.use("TkAgg")


'''initiating pygame'''
pyscreen_x = 915
pyscreen_y = 500
ctypes.windll.user32.SetProcessDPIAware()  # looks that python knows which resolution the CPU has
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pyscreen_x, pyscreen_y)  # setting the position of the pygame window to (pyscreen_x, pyscreen_y)
pygame.init()  # initiating pygame
pyscreen = pygame.display.set_mode((2000, 1200))  # create pygame window of size 2000pixels x 1200pixels
pygame.display.set_caption('Simulation')  # change title of pygame window
clock = pygame.time.Clock()  # create an in-game clock
pygame_icon = pygame.image.load('Mat_2021_Python_Image_8.png')  # define image for the icon of the pygame window
pygame.display.set_icon(pygame_icon)  # change icon of pygame window



'''Create a Space (Note: gravity is created in 
the main while-loop so it gets updated every time 
the tkinter scales and entries get changed)'''
space = pymunk.Space()  # create a pymunk space (area in which dynamical systems can be simulated)


'''create Array with all points that approximate the Brachistochrone Curve for a system with a friction like force 
(Note: The coordinates are scaled by a factor k_brach so they can be used directly as absolute values for the 
coordinates of the window.)'''
N = 200
omega_end = 3
omega = np.linspace(0, omega_end, N)
k_brach = 7
u_k = 30
u = k_brach * ((omega - np.sin(omega)) + u_k * (1 - np.cos(omega))) + 400
v = k_brach * ((1 - np.cos(omega)) + u_k * (omega + np.sin(omega))) + 350
u_end = k_brach * ((omega_end - np.sin(omega_end)) + u_k * (1 - np.cos(omega_end)))
v_end = k_brach * ((1 - np.cos(omega_end)) + u_k * (omega_end + np.sin(omega_end)))

s = []
for obj in range(len(u)):
    d = [u[obj], v[obj]]
    s.append(d)


'''Make an Array p with all the points that approximate 
the Cycloid (Note: In this case no scaling of the coordinates 
is needed because phi_end and R are determined in a way that they create 
coordinates which can directly be used as absolute values for the coordinates of the window)'''
def f(phi):
    return v_end / u_end - (1 - np.cos(phi)) / (phi - np.sin(phi))

phi_end = newton(f, np.pi / 2)
phi = np.linspace(0, phi_end, N)
R = v_end / (1 - np.cos(phi_end))
x = (R * (phi - np.sin(phi))) + 1200
y = ((R * (1 - np.cos(phi)))) + 350

p = []
for obj in range(len(x)):
    q = [x[obj], y[obj]]
    p.append(q)



'''Create all physcial objects via pymunk'''
r = 20

def static_Brachistochrone(space, i):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)  # create a static pymunk body
    shape = pymunk.Segment(body, (s[i][0], s[i][1]), (s[i + 1][0], s[i + 1][1]), 0)   # create a shape for body (draw line segments between the points that define the Brachistochrone)
    space.add(body, shape)  # add body and shape to pymunk space
    return shape

def static_Cycloid(space, i):  # define function for creating the Brachistochrone curve as a static pymunk body
    body = pymunk.Body(body_type=pymunk.Body.STATIC)  # create a static pymunk body
    shape = pymunk.Segment(body, (p[i][0], p[i][1]), (p[i + 1][0], p[i + 1][1]), 0)   # create a shape for body (draw line segments between the points that define the Brachistochrone)
    space.add(body, shape)  # add body and shape to pymunk space
    return shape

def dynamic_starting_ball_brach(space):  # define a function for a dynamical body sitting on the top of the inclined line
    body = pymunk.Body(1, 0.01, body_type=pymunk.Body.DYNAMIC)  # create dynamical pymunk body
    body.position = (s[0][0]+r, s[0][1]-r)  # define position of the body
    shape = pymunk.Circle(body, r)  # create shape for body with radius r
    space.add(body, shape)  # add body and shape to pymunk space
    return shape

def dynamic_starting_ball_cycl(space):  # define a function for a dynamical body sitting on the top of the Brachistochrone curve
    body = pymunk.Body(1, 0.01, body_type=pymunk.Body.DYNAMIC)  # create dynamical pymunk body
    body.position = (p[0][0]+r, p[0][1]-r)  # define position of the body
    shape = pymunk.Circle(body, r)  # create shape for body with radius r
    space.add(body, shape)  # add body and shape to pymunk space
    return shape


'''function for visualizing the Ball with pygame'''
# create needed arrays:
startingballs_brach = []
startingballs_brach.append(dynamic_starting_ball_brach(space))
startingballs_cycl = []
startingballs_cycl.append(dynamic_starting_ball_cycl(space))
startingballs = []
startingballs.append(startingballs_brach[0])
startingballs.append(startingballs_cycl[0])


# create function to draw the startingballs:
def visualize_dynamic_startingballs(startingballs):
    for startingball in startingballs:
        pos_x = int(startingball.body.position.x)  # define x-position as x-position of the pymunk body
        pos_y = int(startingball.body.position.y)  # define y-position as y-position of the pymunk body
        pygame.draw.circle(pyscreen, (255, 0, 0), (pos_x, pos_y), r)  # draw every startingball


'''define functions for the buttons'''
def dynamic_starting_balls():  # define a function that calls the functions which create the balls sitting on top the two cruves
    startingballs.append(startingballs_brach[0])  # add the pymunk body to startingballs
    startingballs.append(startingballs_cycl[0])  # add the pymunk body to startingballs
    visualize_dynamic_startingballs(startingballs)
    dynamic_starting_ball_cycl(space)
    dynamic_starting_ball_brach(space)


'''create arrays needed to draw the curves'''
Brachistochrone = []  # define array for Brachistochrone curve
for i in range(len(s)):
    try:
        Brachistochrone.append(static_Brachistochrone(space, i))
    except:
        print('Last point of Brachistochrone reached')


Cycloid = []  # define array for Cycloid curve
for i in range(len(p)):
    try:
        Cycloid.append(static_Cycloid(space, i))
    except:
        print('Last point of Cycloid reached')


'''Control that game runs and visualize all objects with pygame'''
while True:  # game loop
    for event in pygame.event.get():  # checking for user input
        if event.type == pygame.QUIT:  # check for input to close the game
            pygame.quit()  # quit game
            sys.exit()  # close window


    '''additions to pygame window'''
    pyscreen.fill((255, 255, 255))  # set background color of the pygame window


    '''call functions needed to '''
    visualize_dynamic_startingballs(startingballs)  # call function to draw the dynamic bodies at the top of the curves
    pygame.draw.aalines(pyscreen, (0, 0, 255), False, p, 1)  # draw Cycloid (aalines is used to draw an antialiasing line)
    pygame.draw.aalines(pyscreen, (0, 0, 255), False, s, 1)  # draw Brachistochrone


    "add frictional force to the bodies"
    for startingball in startingballs:
        startingball_velocity = startingball.body._get_velocity()  # get current velocity of the startingball
        if (abs(startingball_velocity)) != 0:
            ô = (startingball_velocity)/(abs(startingball_velocity))  # define direction of motion via normalization of the velocity vector
            startingball.body.apply_force_at_local_point(- (u_k/2) * ô, [0, 0])  # add a force to the startingball at its local coordinate [0,0]


    '''create gravity for pymunk space'''
    g = 20
    space.gravity = (0, g)  # add gravity to pymunk space


    '''check which startingball reached the end of the curve first'''
    k = 0.5
    if (v_end+350-r+k >= startingballs_brach[0].body.position.y) and (startingballs_brach[0].body.position.y >= v_end+350-r):  # check if the y-position of the startingball1 ist bigger than the y-position of the last point of the curve
        print('Brachistochrone')

    if (v_end+350-r+k >= startingballs_cycl[0].body.position.y) and (startingballs_cycl[0].body.position.y >= v_end+350-r):  # check if the y-position of the startingball2 ist bigger than the y-position of the last point of the curve
        print('Cycloid')


    '''updating functions'''
    space.step(1 / 50)  # define rate of updating the state of pymunk space
    pygame.display.update()  # update pygame window
    clock.tick(150)  # set a limit to fps