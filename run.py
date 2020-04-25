from euler import Euler
from math import pi

if __name__ == "__main__":
    equation = input("enter first order differential equation: ")
    curve = input("curve: ")
    x0 = float(input("x0: "))
    y0 = float(input("y0: "))
    if curve == "":
        e = Euler(equation, x0, y0)
    else:
        e = Euler(equation, x0, y0, curve)

    while True:
        x_final = eval(input("find value at: "))
        step_size = float(input("step_size: "))
        e.compare_errors(x_final, step_size)
