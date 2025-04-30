import turtle

# Set up the turtle
t = turtle.Turtle()
t.speed(3)  # Adjust speed (1-10)

# Function to draw a circle for eyes, nose, etc.
def draw_circle(x, y, radius, color="black"):
    t.penup()
    t.goto(x, y - radius)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

# Function to draw an ear
def draw_ear(x, y, direction):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor("brown")
    t.begin_fill()
    t.setheading(direction)  # Set angle for symmetry
    t.circle(25, 180)  # Make the ear rounder and symmetrical
    t.goto(x, y)
    t.end_fill()

# Draw the face
draw_circle(0, 0, 50, "brown")

# Draw the eyes
draw_circle(-20, 20, 7, "white")
draw_circle(20, 20, 7, "white")
draw_circle(-20, 20, 3, "black")
draw_circle(20, 20, 3, "black")

# Draw the nose
draw_circle(0, -10, 5, "black")

# Draw the ears (now properly aligned)
draw_ear(-50, 50, 120)  # Left ear
draw_ear(50, 50, 60)  # Right ear

# Draw the mouth
t.penup()
t.goto(-10, -25)
t.pendown()
t.setheading(-60)
t.circle(10, 120)

# Hide turtle and display window
t.hideturtle()
turtle.done()
