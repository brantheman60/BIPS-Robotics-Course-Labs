import pygame as pg
import time
import math
import random
import matplotlib.path as mpltPath

MANUAL   = True
BLOCKED  = True
HIDDEN   = False
LIGHT    = True

def midpoint(p1, p2): # Always an integer
    return (int((p1[0]+p2[0])/2),
            int((p1[1]+p2[1])/2))

def distance(p1, p2): # Always an integer
    return int(math.sqrt((p2[0] - p1[0])**2
                       + (p2[1] - p1[1])**2))

def draw_field():
    # White background and black walls
    screen.fill((255, 255, 255))
    pg.draw.polygon(screen, (0, 0, 0), wall_corners)

    # Flip the display
    pg.display.flip()

def draw_robot():
    # Square gray robot body w/ red streak at front
    pg.draw.polygon(screen, (100, 100, 100), robot_corners)
    pg.draw.line(screen, (255,0,0), robot_corners[1], robot_corners[2], 5)

    # Hide the workspace
    if(HIDDEN):
        pg.draw.polygon(screen, (0, 0, 0),
                    [(100,100), (100,400), (400,400), (400, 100)])

    # Flip the display
    pg.display.flip()

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

    # Check if intersects the wall
    if(BLOCKED):
        wall_path = mpltPath.Path(wall_corners)
        robot_path = mpltPath.Path(new_points)
        for point in new_points:
            if(wall_path.contains_point(point)): return
        if(robot_path.intersects_path(wall_path)): return

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

    # Check if intersects the wall
    if(BLOCKED):
        wall_path = mpltPath.Path(wall_corners)
        robot_path = mpltPath.Path(new_points)
        for point in new_points:
            if(wall_path.contains_point(point)): return
        if(robot_path.intersects_path(wall_path)): return

    robot_x += (distance * cos_val)
    robot_y += (distance * sin_val)
    robot_corners = new_points

def getSensorVal():
    (light_x, light_y) = midpoint(robot_corners[1], robot_corners[2])
    angle = math.radians(robot_angle)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    sensor_points = []

    # Variables to store most recent point values
    x_exact = float(light_x)
    y_exact = float(light_y)
    (x_old, y_old) = (-1, -1)
    reading = -1

    # Check every pixel in the path of the light
    while True:
        # Get new (x,y)
        (x, y) = (int(x_exact), int(y_exact))

        # Prepare next pixel check
        x_exact += cos_val
        y_exact += sin_val

        # Compare current and old pixel
        if (x == x_old and y == y_old):
            continue
        else:
            (x_old, y_old) = (x, y)

        # See if (x,y) is out of bounds
        if (x<0 or x>=screen_width or y<0 or y>=screen_height):
            reading = sensor_max
            break

        # See if (x,y) is black
        if (tuple(screen.get_at((x,y))) == (0,0,0,255)):
            reading = distance((x,y), (light_x,light_y))
            break

    # Draw line and print reading
    if LIGHT:
        pg.draw.line(screen, (255,255,0), (x,y), (light_x, light_y), 2)
        pg.display.flip()
    return min(reading, sensor_max)



screen_width  = 500
screen_height = 500
robot_x       = 200
robot_y       = 200
robot_width   = 50
robot_height  = 50
robot_angle   = 0
door_size     = 70 # change this b/w 50 and 300
door_wall     = int( ((400 - 100) - door_size)/2 )
wall_corners  = [(100,100), (100+door_wall,100), # topleft
                 (100+door_wall,80), (80,80),    # topleft
                 (80,420), (420,420),            # bottom
                 (420,80), (400-door_wall, 80),  # topright
                 (400-door_wall,100), (400,100), # topright
                 (400,400), (100,400)]           #inner
sensor_max    = 200

# Set up the drawing window
pg.init()
screen = pg.display.set_mode([screen_width, screen_height])

# Draw the first state
robot_x = random.randint(150,350)
robot_y = random.randint(150,350)
robot_corners = [(robot_x - robot_width/2, robot_y - robot_height/2),
                 (robot_x + robot_width/2, robot_y - robot_height/2),
                 (robot_x + robot_width/2, robot_y + robot_height/2),
                 (robot_x - robot_width/2, robot_y + robot_height/2)]
rotate_robot(random.randint(0,360))
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
    # switch manual mode and light mode
    if(keys[pg.K_m] or keys[pg.K_RETURN] or keys[pg.K_SPACE]):
        MANUAL = not MANUAL
        time.sleep(0.1)
    elif keys[pg.K_l]:
        LIGHT  = not LIGHT
        time.sleep(0.1)

    # Draw the field
    draw_field()

    # Let user control robot w/ keyboard
    if(MANUAL):
        if keys[pg.K_LEFT]:
            rotate_robot(-2)
        elif keys[pg.K_RIGHT]:
            rotate_robot(2)
        if keys[pg.K_UP]:
            forward_robot(2)
        elif keys[pg.K_DOWN]:
            forward_robot(-2)
        if keys[pg.K_h]:
            HIDDEN = not HIDDEN
            time.sleep(0.1)

        print(getSensorVal())
        draw_robot()
    # Have the robot autonomously find the exit
    else:
        print("Hi")
        print(getSensorVal())
        draw_robot()

    time.sleep(0.01)

# Done! Time to quit.
pg.quit()
