#!/usr/bin/env python

from math import pi, sqrt, sin, cos, asin, acos, atan
import numpy as np
import matplotlib.pyplot as plt



def inverseKinematics(Xp, Yp):
    la = 0.100
    lb = 0.230
    lc = 0.230

    Xp = Xp + 0.115

    c = sqrt((Xp**2) + (Yp**2))
    e = sqrt(((lc-Xp)**2) + (Yp**2))
    q1 = atan(Yp/Xp) + acos((-(lb**2)+(la**2)+(c**2)) / (2*la*c))
    q4 = 3.14 - atan((Yp)/(lc-Xp)) + acos((-(lb**2)+(la**2)+(e**2)) / (2*la*e))
    
    q1 = q1 * 180 / pi
    q4 = q4 * 180 / pi
    
    return q1, q4





def draw_circle(Xc, Yc, r):
    th = np.arange(0, 2*pi, pi/50)
    xunit = r * cos(th) + Xc
    yunit = r * sin(th) + Yc
    h = plt.plot(xunit, yunit)
    print(type(xunit))
    # X = xunit'
    # Y = yunit'
    # M = [X, Y]
    # writematrix(M, "circle.csv")
   



def main():

    x = 0
    y = 0.17
    r = 0.04

    draw_circle(x, y, r)

if __name__ == "__main__":
    try:
        main()
    except:
        pass


