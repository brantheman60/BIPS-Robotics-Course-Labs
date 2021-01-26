import pygame as pg
import time
import math
import random

FOLLOW = False

def midpoint(p1, p2):
    return (int((p1[0]+p2[0])/2),
            int((p1[1]+p2[1])/2))

def draw_field():
    # White background and black path
    screen.fill((255, 255, 255))
    draw_path((0,0,0), path_corners, 30)

    # Flip the display
    pg.display.flip()

def draw_robot():
    # Square gray robot body w/ red streak and dot at front
    pg.draw.polygon(screen, (100, 100, 100), robot_corners)
    pg.draw.line(screen, (255,0,0), robot_corners[1], robot_corners[2], 5)
    pg.draw.circle(screen, (255,0,0),
        midpoint(robot_corners[1], robot_corners[2]), light_radius)

    # Flip the display
    pg.display.flip()

def draw_path(color, points, thickness):
    # Return if 0 points
    if(len(points) == 0): return

    # Put circles at the ends
    for pt in points:
        pg.draw.circle(screen, color, pt, int(thickness/2))

    # Return if 1 point
    if(len(points) == 1): return

    # Draw thick lines first
    pg.draw.lines(screen, color, False, points, thickness)

def rotate_robot(angle_deg):
    global robot_angle, robot_corners

    angle = math.radians(angle_deg)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    cx = robot_x
    cy = robot_y
    new_points = []
    for x_old, y_old in robot_corners:
        x_old -= cx
        y_old -= cy
        x_new = x_old * cos_val - y_old * sin_val
        y_new = x_old * sin_val + y_old * cos_val
        new_points.append([x_new + cx, y_new + cy])

    robot_angle = (robot_angle + angle_deg) % 360
    robot_corners = new_points

def forward_robot(distance):
    global robot_x, robot_y, robot_corners

    angle = math.radians(robot_angle)
    new_points = []
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    for x_old, y_old in robot_corners:
        x_new = x_old + (distance * cos_val)
        y_new = y_old + (distance * sin_val)
        new_points.append([x_new, y_new])

    robot_x += (distance * cos_val)
    robot_y += (distance * sin_val)
    robot_corners = new_points

def getSensorVal():
    (light_x, light_y) = midpoint(robot_corners[1], robot_corners[2])
    color_list = []
    for x in range(-light_radius, light_radius+1):
        for y in range(-light_radius, light_radius+1):

            if(x**2 + y**2 >= light_radius**2):
                if(light_x+x < 0 or light_x+x>=screen_width or
                   light_y+y < 0 or light_y+y>=screen_height):
                    color = (255,255,255)
                else:
                    color = tuple(screen.get_at((light_x+x, light_y+y)))
                color_list.extend([color[0], color[1], color[2]])

    return int(sum(color_list) / len(color_list))

screen_width  = 500
screen_height = 500
robot_x       = 200
robot_y       = 200
robot_width   = 50
robot_height  = 50
robot_angle   = 0
path_corners  = []
light_radius  = 10

# Set up the drawing window
pg.init()
screen = pg.display.set_mode([screen_width, screen_height])

# Gather the corners of the path
running = True
while running:
    # User input
    keys = pg.key.get_pressed()
    if keys[pg.K_RETURN] or keys[pg.K_SPACE]:
        running = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            path_corners.append(pg.mouse.get_pos())

    draw_field()
    time.sleep(0.01)

# Draw the first robot state
(robot_x, robot_y) = path_corners[0]
robot_corners = [(robot_x - robot_width/2, robot_y - robot_height/2),
                 (robot_x + robot_width/2, robot_y - robot_height/2),
                 (robot_x + robot_width/2, robot_y + robot_height/2),
                 (robot_x - robot_width/2, robot_y + robot_height/2)]
if(len(path_corners) > 1):
    cx = path_corners[1][0] - path_corners[0][0]
    cy = path_corners[1][1] - path_corners[0][1]
    angle = math.degrees(math.atan2(cy,cx))
    rotate_robot(angle)
draw_field()
draw_robot()

# Run until the user asks to quit
running = True
while running:
    # User input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    keys = pg.key.get_pressed()
    if(keys[pg.K_RETURN] or keys[pg.K_SPACE]):
        if(FOLLOW == False):
            FOLLOW = True
            time.sleep(0.1)
        else:
            running = False

    if(FOLLOW):
        draw_field()
        light = getSensorVal()
        print(light)

        if  (light < 110): rotate_robot(-2) #inside black, turn CCW
        elif(light > 150): rotate_robot(2)  #inside white, turn CW
        else: forward_robot(2)              #along white-black line
        draw_robot()
    else:
        pass

    time.sleep(0.01)

# Done! Time to quit.
pg.quit()
