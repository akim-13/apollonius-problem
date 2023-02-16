import logging
import math
from logging import debug as D
import pretty_errors
import turtle

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle():
    def __init__(self, centre, r, turtle):
        self.centre = centre
        self.x = centre.x
        self.y = centre.y
        self.r = r
        self.turtle = turtle

    def draw(self):
        t = self.turtle
        t.penup() 
        t.setheading(0)
        t.setpos(self.x, self.y - self.r)
        t.pendown()
        t.circle(self.r)
        t.penup()
        t.setpos(self.x, self.y)
        t.pendown()


def main():
    t = create_n_turtles(3)

    circles = initialize_circles(t)

    for circle in circles:
        circle.draw()

    delta_r = find_radius_for_inflation(circles)

    circles_to_be_inflated = [ infl_tang_c1, infl_tang_c2, infl_c3 ] = match_tangent_circles(circles, delta_r)

    inflate_and_draw_circles(circles_to_be_inflated, delta_r)

    # D(f"\nd_r = {d_r}\nr1 = {infl_c1.r}, ({infl_c1.x}, {infl_c1.y})\nr2 = {infl_c2.r}, ({infl_c2.x}, {infl_c2.y})")
    #
    # # Find the centre of the circle of inversion
    # k = infl_c1.r/(infl_c1.r + infl_c2.r)
    # x_inv = infl_c1.x + k*(infl_c2.x - infl_c1.x)
    # y_inv = infl_c1.y + k*(infl_c2.y - infl_c1.y)
    #
    # D(f"\nx_i = {x_inv}\ny_i = {y_inv}\nr = 300")
    #
    # c_inv = Circle(x_inv, y_inv, 300)
    # t[3].pencolor("red")
    # c_inv.draw(t[3])
    #
    # infl_c1_inv_x, infl_c1_inv_y = find_inverse_point_x_y_of_tangent_circles(infl_c1, c_inv)
    # print("First line")
    # print(infl_c1_inv_x, infl_c1_inv_y)
    # infl_c2_inv_x, infl_c2_inv_y = find_inverse_point_x_y_of_tangent_circles(infl_c2, c_inv)
    #
    # setpos_turtle_wo_drawing(t[0], x_inv, y_inv)
    # t[0].clear()
    # draw_inverted_circle_line(infl_c1_inv_x, infl_c1_inv_y, c_inv.r*2, t[0])
    #
    # setpos_turtle_wo_drawing(t[1], x_inv, y_inv)
    # t[1].clear()
    # draw_inverted_circle_line(infl_c2_inv_x, infl_c2_inv_y, c_inv.r*2, t[1])
    #
    # infl_c3_inv_x, infl_c3_inv_y = find_inverse_point_x_y(infl_c3, c_inv)
    # infl_c3_inv_r = find_radius_of_inverted_circle(infl_c3, c_inv)
    # c3_inv = Circle(infl_c3_inv_x, infl_c3_inv_y, infl_c3_inv_r)
    # t[2].clear()
    # c3_inv.draw(t[2])

    turtle.done()


def initialize_circles(turtles):
    t = turtles
    t[0].color("red")
    c1 = Circle(Point(0, 0), 100, t[0])

    t[1].color("green")
    c2 = Circle(Point(200, 200), 50, t[1])

    t[2].color("blue")
    c3 = Circle(Point(425, -100), 75, t[2])

    return [ c1, c2, c3 ]

def create_n_turtles(num_of_turtles):
    turtles = []
    for n in range(num_of_turtles):
        turtles.append(turtle.Turtle())
        turtles[n].pensize(3)
        turtles[n].speed(10)

    return turtles

def find_radius_for_inflation(circles):
    delta_r_0_1 = find_delta_r_between_two_circles(circles[0], circles[1])
    delta_r_0_2 = find_delta_r_between_two_circles(circles[0], circles[2])
    delta_r_1_2 = find_delta_r_between_two_circles(circles[1], circles[2])

    min_delta_r = min(delta_r_0_1, delta_r_0_2, delta_r_1_2)
    return min_delta_r

def find_delta_r_between_two_circles(c1, c2):
    distance_between_centres = find_distance_between_two_points(c1.centre, c2.centre)

    delta_r = (distance_between_centres - c1.r - c2.r) / 2
    return delta_r

def find_distance_between_two_points(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def match_tangent_circles(circles, delta_r):
    c1 = circles[0]
    c2 = circles[1]
    c3 = circles[2]
    distance_c1_c2 = find_distance_between_two_points(c1.centre, c2.centre)
    distance_c1_c3 = find_distance_between_two_points(c1.centre, c3.centre)

    if c1.r + c2.r + delta_r*2 == distance_c1_c2:
        tang_c1 = c1
        tang_c2 = c2
        c3 = c3
    elif c1.r + c3.r + delta_r*2 == distance_c1_c3:
        tang_c1 = c1
        tang_c2 = c3
        c3 = c2
    else:
        tang_c1 = c2
        tang_c2 = c3
        c3 = c1

    return tang_c1, tang_c2, c3

def inflate_and_draw_circles(circles, delta_r):
    for circle in circles:
        circle.r += delta_r
        circle.turtle.clear()
        circle.draw()
    return


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
