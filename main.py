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
        t[i].speed(10)

    c1 = Circle(0, 0, 100)
    c2 = Circle(200, 200, 50)
    c3 = Circle(425, -100, 75)
    circles = [c1, c2, c3]

    draw_circles(circles, t)

    d_r_12 = find_d_r(c1, c2)
    d_r_13 = find_d_r(c1, c3)
    d_r_23 = find_d_r(c2, c3)
    d_r = min(d_r_12, d_r_13, d_r_23)

    # infl_c1 and infl_c2 are the ones that are expanded until tangency.
    infl_c1 = c1
    infl_c2 = c2
    infl_c3 = c3
    if d_r == d_r_13:
        infl_c2 = c3
        infl_c3 = c2
    elif d_r == d_r_23:
        infl_c1 = c3
        infl_c3 = c1

    # Inflate all three circles by delta r
    for i, circle in enumerate(circles):
        circle.r += d_r
        t[i].clear()
    draw_circles(circles, t)
    D(f"\nd_r = {d_r}\nr1 = {infl_c1.r}, ({infl_c1.x}, {infl_c1.y})\nr2 = {infl_c2.r}, ({infl_c2.x}, {infl_c2.y})")

    # Find the centre of the circle of inversion
    k = infl_c1.r/(infl_c1.r + infl_c2.r)
    x_inv = infl_c1.x + k*(infl_c2.x - infl_c1.x)
    y_inv = infl_c1.y + k*(infl_c2.y - infl_c1.y)

    D(f"\nx_i = {x_inv}\ny_i = {y_inv}\nr = 300")

    c_inv = Circle(x_inv, y_inv, 300)
    t[3].pencolor("red")
    c_inv.draw(t[3])

    infl_c1_inv_x, infl_c1_inv_y = find_inverse_point_x_y_of_tangent_circles(infl_c1, c_inv)
    print("First line")
    print(infl_c1_inv_x, infl_c1_inv_y)
    infl_c2_inv_x, infl_c2_inv_y = find_inverse_point_x_y_of_tangent_circles(infl_c2, c_inv)

    setpos_turtle_wo_drawing(t[0], x_inv, y_inv)
    t[0].clear()
    draw_inverted_circle_line(infl_c1_inv_x, infl_c1_inv_y, c_inv.r*2, t[0])

    setpos_turtle_wo_drawing(t[1], x_inv, y_inv)
    t[1].clear()
    draw_inverted_circle_line(infl_c2_inv_x, infl_c2_inv_y, c_inv.r*2, t[1])

    infl_c3_inv_x, infl_c3_inv_y = find_inverse_point_x_y(infl_c3, c_inv)
    infl_c3_inv_r = find_radius_of_inverted_circle(infl_c3, c_inv)
    c3_inv = Circle(infl_c3_inv_x, infl_c3_inv_y, infl_c3_inv_r)
    t[2].clear()
    c3_inv.draw(t[2])

    turtle.done()

def find_radius_of_inverted_circle(c1, c_inv):
    k = abs((c_inv.r**2) / ((c1.x - c_inv.x)**2 + (c1.y - c_inv.y)**2 - c1.r**2))
    inv_r = k * c1.r 
    return inv_r

def setpos_turtle_wo_drawing(t, x, y):
    t.penup()
    t.setpos(x, y)
    t.pendown()

def draw_inverted_circle_line(x, y, length, turtle):
    t = turtle
    t.setheading(t.towards(x, y))
    setpos_turtle_wo_drawing(t, x, y)
    t.left(90)
    t.forward(length)
    t.setpos(x, y)
    t.back(length)

# Same as `find_inverse_point_x_y()` but w/o `- c1.r**2` because then
# it goes off to infinity for reasons I haven't figured out yet.
def find_inverse_point_x_y_of_tangent_circles(c1, c_inv):
    k = abs((c_inv.r**2) / ((c1.x - c_inv.x)**2 + (c1.y - c_inv.y)**2))
    c1_inv_x = c_inv.x + k*(c1.x - c_inv.x)
    c1_inv_y = c_inv.y + k*(c1.y - c_inv.y)

    return c1_inv_x, c1_inv_y

def find_inverse_point_x_y(c1, c_inv):
    k = abs((c_inv.r**2) / ((c1.x - c_inv.x)**2 + (c1.y - c_inv.y)**2 - c1.r**2))
    c1_inv_x = c_inv.x + k*(c1.x - c_inv.x)
    c1_inv_y = c_inv.y + k*(c1.y - c_inv.y)

    return c1_inv_x, c1_inv_y

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
        t.pendown()

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
