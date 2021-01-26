import pygame as pg
import math

def val2pixel(value):
    # Let 1 unit = 2 pixels
    return 2*value + screen_width/2

def pixel2val(pixel):
    # Let 1 pixel = 1/2 unit
    return (int) ((pixel - screen_width/2)/2)

def draw_field():
    # White background and black ground
    screen.fill((255, 255, 255))
    pg.draw.rect(screen, (0, 0, 0),
            (0, ground_height, screen_width, screen_height))

    # Mark the ground w/ values
    marks = [-200, -150, -100, -50, 0, 50, 100, 150, 200]
    for val in marks:
        pg.draw.line(screen, (255, 255, 255),
                (val2pixel(val), ground_height),
                (val2pixel(val), ground_height + 10))
        label = font2.render(str(val), True, BLUE)
        screen.blit(label, (val2pixel(val) - 10,
                 ground_height + 20))

    # Flip the display
    pg.display.flip()

def draw_robot():
    # Rectangular robot body
    pg.draw.rect(screen, (100, 100, 100),
        (robot_x - robot_width/2, robot_y - robot_height/2,
        robot_width, robot_height))

    # Circular robot wheels
    wheel1_x = int(robot_x - robot_width/2 + wheel_radius)
    wheel2_x = int(robot_x + robot_width/2 - wheel_radius)
    wheel_y  = int(robot_y + robot_height/2)

    pg.draw.circle(screen, (255, 255, 255),
        (wheel1_x, wheel_y), wheel_radius, 0)
    pg.draw.circle(screen, (0, 0, 0),
        (wheel1_x, wheel_y), wheel_radius, 2)

    pg.draw.circle(screen, (255, 255, 255),
        (wheel2_x, wheel_y), wheel_radius, 0)
    pg.draw.circle(screen, (0, 0, 0),
        (wheel2_x, wheel_y), wheel_radius, 2)

    # Dots on robot wheels
    dot_offsetx = dot_dist * math.cos(math.radians(wheel_angle))
    dot_offsety = dot_dist * math.sin(math.radians(wheel_angle))
    dot1_x = int(wheel1_x + dot_offsetx)
    dot1_y = int(wheel_y  + dot_offsety)
    dot2_x = int(wheel2_x + dot_offsetx)
    dot2_y = int(wheel_y  + dot_offsety)

    pg.draw.circle(screen, (255, 0, 0),
        (dot1_x, dot1_y), dot_radius, 0)

    pg.draw.circle(screen, (255, 0, 0),
        (dot2_x, dot2_y), dot_radius, 0)

    # Flip the display
    pg.display.flip()


# Size constants
screen_width  = 1000
screen_height = 400
ground_height = 150
robot_x       = screen_width/2
robot_y       = 100
robot_width   = 120
robot_height  = 60
wheel_radius  = 23
dot_dist      = 15
dot_radius    = 5
wheel_angle   = 90  #degrees
destination   = robot_x
arm_angle     = 0


# Textbox constants
box_width      = 100
input_box      = pg.Rect((screen_width - box_width)/2,
                          screen_height - 100,
                          box_width,
                          50)
color_inactive = (50, 50, 50)
color_active   = (255, 255, 255)
color          = color_inactive
text           = ""
active         = False

# Set up the drawing window
pg.init()
screen = pg.display.set_mode([screen_width, screen_height])
clock = pg.time.Clock()

# Prepare the labels
font1 = pg.font.SysFont("Arial", 70)
font2 = pg.font.SysFont("Arial", 30)
BLUE = (0, 255, 0)

# Run until the user asks to quit
running = True
while running:
    # User input and textbox
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if active:
                if event.key == pg.K_RETURN:
                    # Check if text is valid
                    try:
                        tmp = val2pixel(int(text))
                        if(tmp<0 or tmp>screen_width):
                            raise ValueError("")
                        destination = tmp
                        active = False
                    except ValueError:
                        pass
                    text = ""
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    # Draw the field
    draw_field()

    # Draw the textbox
    txt_surface = font1.render(text, True, color)
    color = color_active if active else color_inactive
    input_box.w = max(box_width, txt_surface.get_width()+10)
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pg.draw.rect(screen, color, input_box, 2)
    pg.display.flip()

    # Draw the robot
    draw_robot()

    # Determine how robot wheels and robot body should move
    if  (robot_x > destination + 4): # must move left
        wheel_angle -= 3
        robot_x -= wheel_radius * math.radians(3)
        active = False
        text = ""
    elif(robot_x < destination - 4): # must move right
        wheel_angle += 3
        robot_x += wheel_radius * math.radians(3)
        active = False
        text = ""
    else:
        active = True

    clock.tick(100)

# Done! Time to quit.
pg.quit()
