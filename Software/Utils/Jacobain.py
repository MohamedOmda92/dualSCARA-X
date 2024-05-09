from math import pi, sin, cos, asin, acos, atan
import numpy as np



def forwardJacobian(q1, q4, Qd, Xp, Yp):
    
    la = 0.100 # Sort link
    lb = 0.220 # Long link
    lc = 0.230 # Distance between motors
    
    Xp = Xp + 0.115 # Mapping desired pose to motor 1 (Left | q1) axis
    
    r1 = 0 # Offset from end-effector along the long link (Right lb)
    
    a1 = la
    a2 = lb
    a3 = lb
    a4 = la
    
    # Dependent joints
    q2 = asin((Yp - (la*sin(q1))) / lb)
    q3 = acos((Xp-lc-(la*cos(q4))) / lc)

    # Jacobian matrix elements
    j11 = -a1*sin(q1) + a1*(sin(q2)*sin(q3-q1)*a3 + r1*sin(q3)*sin(q1-q2))/a3/sin(q3-q2)
    j12 = a4*(sin(q2)*sin(q4-q3)*a3 - r1*sin(q3)*sin(q4-q2))/a2/sin(q3-q2)
    j21 = a1*cos(q1) - a1*(cos(q2)*sin(q3-q1)*a3 + r1*cos(q3)*sin(q1-q2))/a3/sin(q3-q2)
    j22 = -a4*(cos(q2)*sin(q4-q3)*a3 - r1*cos(q3)*sin(q4-q2))/a3/sin(q3-q2)

    # <<< Note >>> Eliminated part as angular speed aroud Z-axis not needed
    #J31 = -a1*sin(q1-q2)/a3/sin(q3-q2)
    #J32 = a4*sin(q4-q2)/a3/sin(q3-q2)

    j = np.array([[j11, j12], 
                 [j21, j22]]) # Last row (J31 J32) in jacobian matrix not used 

    Q_dot = np.array([[Qd[0]],
                      [Qd[3]]])
    
    V = np.matmul(j, Q_dot) # End-effecor velocity matrix

    Xd = V[0]
    Yd = V[1]
    
    return Xd, Yd



def inverseJacobin(q1, q4, Xd, Xp, Yp):
    
    la = 0.100 # Sort link
    lb = 0.220 # Long link
    lc = 0.230 # Distance between motors
    
    Xp = Xp + 0.115 # Mapping desired pose to motor 1 (Left | q1) axis
    
    r1 = 0 # Offset from end-effector along the long link (Right lb)
    
    a1 = la
    a2 = lb
    a3 = lb
    a4 = la
    
    # Dependent joints
    q2 = asin((Yp - (la*sin(q1))) / lb)
    q3 = acos((Xp-lc-(la*cos(q4))) / lc)

    # Jacobian matrix elements
    j11 = -a1*sin(q1) + a1*(sin(q2)*sin(q3-q1)*a3 + r1*sin(q3)*sin(q1-q2))/a3/sin(q3-q2)
    j12 = a4*(sin(q2)*sin(q4-q3)*a3 - r1*sin(q3)*sin(q4-q2))/a2/sin(q3-q2)
    j21 = a1*cos(q1) - a1*(cos(q2)*sin(q3-q1)*a3 + r1*cos(q3)*sin(q1-q2))/a3/sin(q3-q2)
    j22 = -a4*(cos(q2)*sin(q4-q3)*a3 - r1*cos(q3)*sin(q4-q2))/a3/sin(q3-q2)

    # <<< Note >>> Eliminated part as angular speed aroud Z-axis not needed
    #J31 = -a1*sin(q1-q2)/a3/sin(q3-q2)
    #J32 = a4*sin(q4-q2)/a3/sin(q3-q2)

    j = np.array([[j11, j12], 
                 [j21, j22]]) # Last row (J31 J32) in jacobian matrix not used 

    X_dot = np.array([[Xd[0]],
                      [Xd[1]]])
    
    j_inv = np.linalg.inv(j)
    Qd = np.matmul(j_inv, X_dot) # End-effecor velocity matrix

    qd1 = Qd[0]
    qd4 = Qd[1]
    
    return qd1, qd4


if __name__ == "__main__":
    
    #Xd, Yd = forwardJacobian(2.778405, 3.825739, [-0.00009215938,0.00002889549,-0.000044185,-0.00014858], -0.02, 0.149)
    qd1, qd4 = inverseJacobin(2.051969, 3.2066084, [0,0.075], 0.02, 0.213442)
    print(qd1)
    print(qd4)


