import logging
import math
from logging import debug as D
import pretty_errors
import turtle

def main():
    t = []
    for i in range (5):
        t.append(turtle.Turtle())
        t[i].pensize(3)
        t[i].speed(0)

    c1 = Circle(0, 0, 100)
    c2 = Circle(200, 200, 50)
    c3 = Circle(400, -100, 75)
    circles = [c1, c2, c3]

    draw_circles(circles, t)

    d_r_12 = find_d_r(c1, c2)
    d_r_13 = find_d_r(c1, c3)
    d_r_23 = find_d_r(c2, c3)
    d_r = min(d_r_12, d_r_13, d_r_23)
    infl_c1 = c1
    infl_c2 = c2
    if d_r == d_r_13:
        infl_c2 = c3
    elif d_r == d_r_23:
        infl_c1 = c3

    # Inflate all three circles by delta r
    for i, circle in enumerate(circles):
        circle.r += d_r
        t[i].clear()
    draw_circles(circles, t)
    D(f"\nd_r = {d_r}\nr1 = {infl_c1.r}, (0, 0)\nr2 = {infl_c2.r}, (200, 200)")

    angle_infl_c1_c2 = math.atan((infl_c1.y - infl_c2.y)/(infl_c1.x - infl_c2.x))
    dist_x_inv = (infl_c1.r + d_r)*math.cos(angle_infl_c1_c2)
    dist_y_inv = (infl_c1.r + d_r)*math.sin(angle_infl_c1_c2)

    if infl_c1.x < infl_c2.x:
        x_inv = infl_c1.x + dist_x_inv
    else:
        x_inv = infl_c1.x - dist_x_inv

    if infl_c1.y < infl_c2.y:
        y_inv = infl_c1.y + dist_y_inv
    else:
        y_inv = infl_c1.y - dist_y_inv

    D(f"\nx_i = {x_inv}\ny_i = {y_inv}")
    c_inv = Circle(x_inv, y_inv, 800)
    c_inv.draw(t[3])

    turtle.done()

def draw_circles(circles, turtles):
    for i, circle in enumerate(circles): 
        circle.draw(turtles[i])

def find_d_r(c1, c2):
    x1 = c1.x
    x2 = c2.x
    y1 = c1.y
    y2 = c2.y
    distance_between_centres = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    delta_r = (distance_between_centres - c1.r - c2.r) / 2
    return delta_r

class Circle():
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self, turtle):
        t = turtle
        t.penup() 
        t.setheading(0)
        t.setpos(self.x, self.y - self.r)
        t.pendown()
        t.circle(self.r)
        t.penup()
        t.setpos(self.x, self.y)

if __name__ == '__main__':
    pretty_errors.configure(
        lines_before         = 10,
        separator_character  = '',
        line_number_first    = True,
        display_locals       = True,
        display_trace_locals = True,
        local_name_color     = pretty_errors.BLUE,
        filename_color       = pretty_errors.CYAN,
        code_color           = pretty_errors.WHITE,
        exception_arg_color  = pretty_errors.YELLOW,
        function_color       = pretty_errors.BRIGHT_GREEN,
        line_number_color    = pretty_errors.BRIGHT_YELLOW,
        line_color           = pretty_errors.RED + '> ' + pretty_errors.default_config.local_value_color,
        infix = '────────────────────────────────────────────────────────────────────────────────'
    )

    logging.basicConfig(level = logging.DEBUG, format = '[%(levelname)s] -----> [%(lineno)s]: %(msg)s')

    main()
