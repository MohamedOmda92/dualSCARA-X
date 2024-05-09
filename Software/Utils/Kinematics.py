from math import pi, sqrt, sin, cos, asin, acos, atan



def inverseKinematics(Xp, Yp):
    la = 0.1
    lb = 0.2334
    lc = 0.227

    Xp = Xp + 0.115

    c = sqrt((Xp**2) + (Yp**2))
    e = sqrt(((lc-Xp)**2) + (Yp**2))
    q1 = atan(Yp/Xp) + acos((-(lb**2)+(la**2)+(c**2)) / (2*la*c))
    q4 = 3.14 - atan((Yp)/(lc-Xp)) + acos((-(lb**2)+(la**2)+(e**2)) / (2*la*e))
    
    q1 = q1 * 180 / pi
    q4 = q4 * 180 / pi
    
    return q1, q4



def forwardKinematics(q1, q2):
    la = 0.1
    lb = 0.2334
    lc = 0.227
    
    e = 2*lb*(lc + (la*(cos(q2) - cos(q1))))
    f = (2*la*lb*sin(q2)) - (2*la*lb*sin(q1))
    g = (lc**2) + (2*(la**2)) + (2*lc*la*cos(q2)) - (2*lc*la*cos(q1)) - (2*(la**2)*cos(q2 - q1))

    theta2 = 2*atan((-f - sqrt( (e**2) + (f**2) - (g**2) )) / (g - e))

    x = lc + (la*cos(q2)) + (lb*cos(theta2))
    y = (la*sin(q2)) + (lb*sin(theta2))

    x = x - 0.115
    
    return x, y



if __name__ == "__main__":

    # q1, q4 = inverseKinematics(-0.02,0.1500441)
    # print(f"Angle 1: {q1}\tAngle 2: {q4}")
    
    x, y = forwardKinematics(2.9503295604638846, 3.9757998104225374)
    print(f"X: {x}\tY: {y}")
    print(f"Theta1: {2.9503295604638846 / pi * 180}")
    print(f"Theta2: {3.9757998104225374 / pi * 180}")