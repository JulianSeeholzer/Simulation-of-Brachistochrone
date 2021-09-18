import pygame
import pymunk
import os
import ctypes
import tkinter as tk
from tkinter import *
import numpy as np
from scipy.optimize import newton

#Programming the Physics:
'''initiating pygame'''
pyscreen_x = 1250
pyscreen_y = 500
ctypes.windll.user32.SetProcessDPIAware()  # looks that python knows which resolution the CPU has
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pyscreen_x,pyscreen_y)
pygame.init()  # initiating pygame
pyscreen = pygame.display.set_mode((2000, 1200))  # create Window
pygame.display.set_caption('Simulation')
clock = pygame.time.Clock()  # create a in-game clock
pygame_icon = pygame.image.load('Mat_2021_Python_Image_8.png')
pygame.display.set_icon(pygame_icon)

'''embedding the pygame window in a tkinter window'''
ctypes.windll.user32.SetProcessDPIAware()  # looks that python knows which resolution the CPU has
tkscreen = tk.Tk()
tkscreen.title('Regulation of Parameters')
tkscreen.geometry('600x1202+620+428')
tkscreen.configure(bg='black')
os.environ['SDL_VIDEODRIVER'] = 'windib'
tkinter_icon = PhotoImage(file = "Mat_2021_Python_Image_8.png")
tkscreen.iconphoto(False, tkinter_icon)


'''Create a Space (Note: gravity is created in 
the main while loop so it gets updated every time 
the tkinter scales and entries are updated)'''
space = pymunk.Space()  # creat a space in which events can occur



'''Make an Array p with all the points that approximate 
the Brachistochrone Curve. (Note: The coordinates are scaled by a 
factor k so they can be used directly as coordinates of the created window.)'''
# (unscaled) coordinates of the endpoint of the Brachistochrone
a, b = 1, 0.65

# number of steps for Theta
N = 200

# function for calculating theta2
def f(theta):
    return b / a - (1 - np.cos(theta)) / (theta - np.sin(theta))


# calculated theta2 via newton-raphson-method
theta2 = newton(f, np.pi / 2)

# calculate the radius of the circle generation the Brachistochrone
R = b / (1 - np.cos(theta2))

# scale-factor for Brachistochrone coordinates
k = 700

# parametric equation for the Brachistochrone (with additonal Terms for moving the startpoint)
theta = np.linspace(0, theta2, N)
x = k * (R * (theta - np.sin(theta))) + 1000
y = k * ((R * (1 - np.cos(theta)))) + 400

# unscaled parametric equation for the Brachistochrone
u = k * (R * (theta - np.sin(theta)))
v = k * (R * (1 - np.cos(theta)))

print(theta2)

# create the Array with the x and y coordinates of the points, which approximate the Brachistochrone
p = []

# append the coordinates to the Array
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

r0 = tk.StringVar()
r0.set('20')
entry_r = tk.Entry(tkscreen, bg='black', fg='white', textvariable=r0, bd=10)
entry_r.pack()
entry_r.place(x=140, y=750)

'''Create all physcial objects via pymunk'''
#creat dynamic balls (objects that can change position in pygame space)
def dynamic_ball(space, pos):
    r = float(entry_r.get())
    body = pymunk.Body(1, 0.01, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, r)
    shape.friction = 0.0
    space.add(body, shape)
    return shape

#create a linear Brachistochrone
def static_Brachistochrone(space, i):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (p[i][0], p[i][1]), (p[i + 1][0], p[i + 1][1]), 0)
    shape.friction = 0.0
    space.add(body, shape)
    return shape

#create a linear line
def static_line(space, i):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (h[i][0], h[i][1]), (h[i + 1][0], h[i + 1][1]), 0)
    shape.friction = 0.0
    space.add(body, shape)
    return shape


#create a ball which is at the top position of the linear line when the programm is started
def dynamic_starting_ball1(space):
    r = float(entry_r.get())
    body = pymunk.Body(1, 0.01, body_type=pymunk.Body.DYNAMIC)
    body.position = (h[0][0]+r/2, h[0][1]-r)
    shape = pymunk.Circle(body, r)
    shape.friction = 0.0
    space.add(body, shape)
    return shape

#create a ball which is at the top position of the Brachistochrone when the programm is started
def dynamic_starting_ball2(space):
    r = float(entry_r.get())
    body = pymunk.Body(1, 0.01, body_type=pymunk.Body.DYNAMIC)
    body.position = (p[0][0]+r/2, p[0][1]-r)
    shape = pymunk.Circle(body, r)
    shape.friction = 0.0
    space.add(body, shape)
    return shape


'''function for visualizing the Ball with pygame'''
# create the function to draw the dynamicballs
def visualize_dynamic_ball(balls):
    for ball in balls:
        r = float(entry_r.get())  # set the radius of the ball to the value in the entry
        pos_x = int(ball.body.position.x)  # x-position of the pymunk body
        pos_y = int(ball.body.position.y)  # y-position of the pymunk body
        pygame.draw.circle(pyscreen, (255, 147, 51), (pos_x, pos_y), r)  # draw every ball in balls

startingballs = []
startingballs.append(dynamic_starting_ball1(space))
startingballs.append(dynamic_starting_ball2(space))

# create function to draw the startingballs
def visualize_dynamic_startingballs(startingballs):
    for startingball in startingballs:
        r = float(entry_r.get())  # set the radius of the ball to the value in the entry
        pos_x = int(startingball.body.position.x)  # x-position of the pymunk body
        pos_y = int(startingball.body.position.y)  # y-position of the pymunk body
        pygame.draw.circle(pyscreen, (255, 147, 51), (pos_x, pos_y), r)  # draw every startingball in startingballs


'''function for button'''
def dynamic_starting_balls():
    startingballs.append(dynamic_starting_ball2(space))
    startingballs.append(dynamic_starting_ball1(space))
    visualize_dynamic_startingballs(startingballs)
    dynamic_starting_ball1(space)
    dynamic_starting_ball2(space)



'''Create buttons and sliders to regulate some constants of the simulation '''
#defining the functions which are called when the associated button is clicked
def gravity_off():
    scale_g.set(0)

def gravity_on():
    scale_g.set(20)

#creat all buttons needed in the Tkinter window
scale_g = tk.Scale(tkscreen, bg='black', fg='white', from_=0, to=100, orient=tk.HORIZONTAL, length=200, bd=10)
scale_g.config(highlightbackground='black')
scale_g.pack()
scale_g.place(x=107, y=387)

label_g_off_image = PhotoImage(file='Mat_2021_Python_Image_5.png')
label_g_off = Button(tkscreen, bg='black', image=label_g_off_image, bd=0, command=gravity_off)
label_g_off.pack()
label_g_off.place(x=380, y=320)

label_g_on_image = PhotoImage(file='Mat_2021_Python_Image_4.png')
label_g_on = Button(tkscreen, bg='black', image=label_g_on_image, bd=0, command=gravity_on)
label_g_on.pack()
label_g_on.place(x=380, y=410)

label_startingballs_image = PhotoImage(file='Mat_2021_Python_Image_6.png')
label_startingballs = Button(tkscreen, bg='black', image=label_startingballs_image, bd=0, command=dynamic_starting_balls)
label_startingballs.pack()
label_startingballs.place(x=70, y=980)

#create all labels needed for description in the Tkinter window
label_g_strength_image = PhotoImage(file='Mat_2021_Python_Image_3.png')
label_g_strength = tk.Label(tkscreen, bg='black', image=label_g_strength_image)
label_g_strength.pack()
label_g_strength.place(x=70, y=320)

label_g_image = PhotoImage(file='Mat_2021_Python_Image_1.png')
label_g = tk.Label(tkscreen, bg='black', image=label_g_image)
label_g.pack()
label_g.place(x=70, y=230)

label_r_image = PhotoImage(file='Mat_2021_Python_Image_2.png')
label_r = tk.Label(tkscreen, bg='black', image=label_r_image)
label_r.pack()
label_r.place(x=70, y=660)

label_title_image = PhotoImage(file='Mat_2021_Python_Image_7.png')
label_title = tk.Label(tkscreen, bg='black', image=label_title_image)
label_title.pack()
label_title.place(x=70, y=30)





'''create needed lists'''

# create the list with all points that approximate the Brachistochrone for pygame
Brachistochrone = []
for i in range(len(p)):
    try:
        Brachistochrone.append(static_Brachistochrone(space, i))
    except:
        print('Last point of Brachistochrone reached')

# create the list for all ball objects
balls = []


# create the list for all point that define the linear line for pygame
line = []
for i in range(len(h)):
    try:
        line.append(static_line(space, i))
    except:
        print('Last point of line reached')



'''Control that game runs and visualize all objects with pygame'''
while True:  # game loop
    for event in pygame.event.get():  # checking for user input
        if event.type == pygame.QUIT:  # input to close the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(dynamic_ball(space, event.pos))

    '''color pygame window'''
    pyscreen.fill((255, 255, 255))  # coloring window the pygame window


    '''draw objects'''
    visualize_dynamic_ball(balls)  # drawing the balls
    visualize_dynamic_startingballs(startingballs)  # drawing the startingballs
    pygame.draw.aalines(pyscreen, (0, 0, 0), False, p, 1)  # draw Brachistochrone (aalines is used to draw an antialiasing line)
    pygame.draw.aalines(pyscreen, (0, 0, 0), False, h, 1)  # draw line


    '''create gravity'''
    g = Scale.get(scale_g)  # set g to the current value of the scale button
    # print(g)
    space.gravity = (0, g)  # define the gravity in pymunk space


    '''define updating properties'''
    space.step(1 / 50)  # define rate of updating the the positions of the objects in pymunk
    pygame.display.update()  # update pygame window
    tkscreen.update()  # update tkinter window
    clock.tick(150)  # set a limit to fps
