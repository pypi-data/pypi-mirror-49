"""
planefigures is a python package based on the turtle library.
It takes the pain out of drawing plain shapes.

Example

    import figures
    import turtle

    figures.color('red','yellow')

    figures.begin_fill()

    for n in range(8):
        figures.polygon(8, 80)
        turtle.right(360/8)

    figures.end_fill()

Functions

    polygon(sides:int, length:int) -- Draw a regular polygon of given sides with each side of given length.
    rectangle(length:int, breadth:int) -- Draw a rectangle of given length and breadth.
    circle(radius, extent=None, steps=None) -- Draw a circle of given radius. This function works exactly like turtle.circle().
    color(*args) -- Return or set pencolor and fillcolor. This function works exactly like turtle.color().
    begin_fill() -- To be called just before drawing a shape to be filled.
    end_fill() -- Fill the shape drawn after the last call to begin_fill().
"""

import turtle

def polygon(sides:int, length:int):
    """Draw a regular polygon of given sides with each side of given length.
    
    Arguments:
        sides {int} -- The number of sides of the polygon
        length {int} -- The length of each side of the polygon in pixels
    """
    # (sides - 2) * 180 -- defines sum of angles in any polygon
    angle = ((sides - 2) * 180) / sides

    for x in range(sides):
        turtle.forward(length)
        turtle.left(180 - angle)
        

def rectangle(length:int, breadth:int):
    """Draw a rectangle of given length and breadth.
    
    Arguments:
        length {int} -- The length of the quadrilateral in pixels
        breadth {int} -- The breadth of the quadrilateral in pixels
    """
    
    for x in range(2):
        turtle.forward(length)
        turtle.right(90)
        turtle.forward(breadth)
        turtle.right(90)


def parallelogram(length:int, breadth:int, angle:float):
    """Draw a parallelogram of given length and breadth and a given pair of opposite angle
    
    Arguments:
        length {int} -- The length of the parallelogram
        breadth {int} -- The breadth of the parallelogram
        angle {float} -- A pair of opposite angles
    """
    
    turtle.forward(length)
    turtle.left(angle)
    turtle.forward(breadth)
    turtle.left(180-angle)
    turtle.forward(length)
    turtle.left(angle)
    turtle.forward(breadth)
    turtle.left(180-angle)