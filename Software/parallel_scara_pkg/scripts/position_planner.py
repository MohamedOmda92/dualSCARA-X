#!/usr/bin/env python3.8
import sys
print(sys.version)
from math import pi, sqrt, sin, cos, asin, acos, atan
from pandas import *
from typing import Sequence, Type
from pynput import keyboard
from parallel_scara_pkg.trajectory import Trajectory
import rospy
import sched
import os
import time
import json
import csv
import numpy as np
from std_msgs.msg import Float32MultiArray
from parallel_scara_pkg.srv import ptpNav, ptpNavResponse
from parallel_scara_pkg.srv import shapeNav, shapeNavResponse
from std_srvs.srv import Trigger, TriggerResponse


# Global CONSTANTS & Variables
RESOLUTION = 6400
SPEED = 4000
ACCELERATION = 4000
current_pose = [0.0985, 0.2039]


def inverseJacobin(th1: float, 
                   th4: float, 
                   Xd: float, 
                   Yd: float, 
                   X: float, 
                   Y: float) -> Sequence[float]:
    """
    Calculates required joints velocity based on desired cartesian velocity.

    Parameters
    ----------
    th1 : float
        Angle of the 1st joint (Left motor) {RAD}

    th2 : float
        Angle of the 2nd joint (Right motor) {RAD}

    Xd : float
        Velocity of cartesian X-axis element {METERS/SEC}

    Yd : float
        Velocity of cartesian Y-axis element {METERS/SEC}

    X : float
        X-axis coordinate of the target position {METERS}

    Y : float
        Y-axis coordinate of the target position {METERS}

    Returns
    -------
    tuple
        Joints velocity that will satisfy desired cartesian velocity
    """

    la = 0.1 # Short link
    lb = 0.2334 # Long link
    lc = 0.227 # Distance between motors
    
    X = X + 0.115 # Mapping desired pose to motor 1 (Left | q1) axis
    
    r1 = 0 # Offset from end-effector along the long link (Right lb)
    
    a1 = la
    a2 = lb
    a3 = lb
    a4 = la

    # Dependent joints
    th2 = asin((Y - (la*sin(th1))) / lb)
    th3 = acos((X-lc-(la*cos(th4))) / lc)

    # Jacobian matrix elements
    j11 = -a1*sin(th1) + a1*(sin(th2)*sin(th3-th1)*a3 + r1*sin(th3)*sin(th1-th2))/a3/sin(th3-th2)
    j12 = a4*(sin(th2)*sin(th4-th3)*a3 - r1*sin(th3)*sin(th4-th2))/a2/sin(th3-th2)
    j21 = a1*cos(th1) - a1*(cos(th2)*sin(th3-th1)*a3 + r1*cos(th3)*sin(th1-th2))/a3/sin(th3-th2)
    j22 = -a4*(cos(th2)*sin(th4-th3)*a3 - r1*cos(th3)*sin(th4-th2))/a3/sin(th3-th2)

    # <<< Note >>> Eliminated part as angular speed aroud Z-axis not needed
    #J31 = -a1*sin(q1-q2)/a3/sin(q3-q2)
    #J32 = a4*sin(q4-q2)/a3/sin(q3-q2)

    j = np.array([[j11, j12], 
                 [j21, j22]]) # Last row (J31 J32) in jacobian matrix not used 

    X_dot = np.array([[Xd],
                      [Yd]])
    
    j_inv = np.linalg.inv(j)
    Qd = np.matmul(j_inv, X_dot) # Actuated joints velocity matrix

    th_dot1 = Qd[0][0]
    th_dot4 = Qd[1][0]
    
    return th_dot1, th_dot4



def inverseKinematics(X: float, 
                      Y: float) -> Sequence[float]:
    """
    Calculates required joints angle based on target cartesian coordinates

    Parameters
    ----------
    X : float
        X-axis coordinate of the target position {METERS}

    Y : float
        Y-axis coordinate of the target position {METERS}

    Returns
    -------
    Sequence[float]
        Joints angle that will satisfy desired cartesian coordinate
    """

    la = 0.1 # Short link
    lb = 0.2334 # Long link
    lc = 0.227 # Distance between motors

    X = X + 0.115
    
    c = sqrt((X**2) + (Y**2))
    e = sqrt(((lc-X)**2) + (Y**2))
    th1 = atan(Y/X) + acos((-(lb**2)+(la**2)+(c**2)) / (2*la*c))
    th4 = 3.14 - atan((Y)/(lc-X)) + acos((-(lb**2)+(la**2)+(e**2)) / (2*la*e))

    return th1, th4



def forwardKinematics(q1: float, 
                      q2: float) -> Sequence[float]:
    """
    Calculates cartesian coordinates from joints angle 

    Parameters
    ----------
    q1 : float
        Angle of joint 1 (Left Motor) {RAD}

    q2 : float
        Angle of joint 2 (Right Motor) {RAD}

    Returns
    -------
    Sequence[float]
        Cartesian coordinates at these angles {METERS}
    """

    la = 0.1 # Short link
    lb = 0.2334 # Long link
    lc = 0.227 # Distance between motors
    
    e = 2*lb*(lc + (la*(cos(q2) - cos(q1))))
    f = (2*la*lb*sin(q2)) - (2*la*lb*sin(q1))
    g = (lc**2) + (2*(la**2)) + (2*lc*la*cos(q2)) - (2*lc*la*cos(q1)) - (2*(la**2)*cos(q2 - q1))

    theta2 = 2*atan((-f - sqrt( (e**2) + (f**2) - (g**2) )) / (g - e))

    x = lc + (la*cos(q2)) + (lb*cos(theta2))
    y = (la*sin(q2)) + (lb*sin(theta2))

    x = x - 0.115
    
    return x, y



def start_point_nav(trajObj: Type[Trajectory]) -> None:
    """
    Navigate to the 1st point of the trajectory

    Parameters
    ----------
    traj : <class 'Trajectory'>
    """

    traj = trajObj.trajectory
    q1_initial = traj[1][0]
    q2_initial = traj[2][0]

    try:

        theta1, theta2 = inverseKinematics(q1_initial, q2_initial)

        pos1 = 1.0 * RESOLUTION * theta1 / (2*pi)
        pos2 = 1.0 * RESOLUTION * theta2 / (2*pi)
        
    except ValueError:
        rospy.logerr("Invalid starting target position [{:.3f},{:.3f}]".format(q1_initial, q2_initial))
        return
    
    # >>> Update Current Pose
    current_pose[0] = q1_initial
    current_pose[1] = q2_initial

    # >>> Configure ROS message
    print("\nMoving to the start position ...")
    config = Float32MultiArray()
    config.data = [pos1, pos2, SPEED/2, SPEED/2, ACCELERATION, ACCELERATION]
    config_pub.publish(config)
    
    # NEEDS TO BE DETERMINED (SOFT CODED)
    for i in range(10):
        print(f"Start after: {10-i}")
        time.sleep(1)



def _follow_path(trajObj: Type[Trajectory], scheduler=None):
    """
    Follow trajectory through scheduled event with specific time intervarls (50ms)

    Parameters
    ----------
    trajObj : <class 'Trajectory'>
    
    scheduler : _type_, optional
        Event scheduler from <class 'sched'>, by default None
    """

    sample_idx = trajObj.currentSample # Iterator
    samples = trajObj.samples # used in loop termination 
    ts = trajObj.timeStep # scheduler event time intervals
    traj = trajObj.trajectory

    # Publishing config data (TASK SPACE)
    x_goal = traj[1][sample_idx]
    y_goal = traj[2][sample_idx]
    Xd = traj[3][sample_idx]
    Yd = traj[4][sample_idx]

    try:
        # >>> Setting up position
        theta1, theta2 = inverseKinematics(x_goal, y_goal)
        pos1 = 1.0 * RESOLUTION * theta1 / (2*pi)
        pos2 = 1.0 * RESOLUTION * theta2 / (2*pi)


        # >>> Setting up velocity
        th_dot1, th_dot2 = inverseJacobin(theta1, theta2, Xd, Yd, x_goal, y_goal)
        vel1 = 1.0 * RESOLUTION * th_dot1 / (2*pi)
        vel2 = 1.0 * RESOLUTION * th_dot2 / (2*pi)
        
        # >>> Update Current Pose
        current_pose[0] = x_goal
        current_pose[1] = y_goal

        # >>> Configure ROS message
        config = Float32MultiArray()
        config.data = [pos1, pos2, abs(vel1), abs(vel2), ACCELERATION, ACCELERATION]
        
        config_pub.publish(config)

        # Iterator Increment
        trajObj.currentSample += 1

        # Terminate Condition
        if sample_idx < samples-1:
            scheduler.enter(ts, 1, _follow_path, argument=(trajObj, scheduler))

    except ValueError as e:
        rospy.logerr("Invalid target position [{:.3f},{:.3f}]".format(x_goal, y_goal))



def track_trajectory(trajObj: Type[Trajectory]) -> None:
    """
    Executes "_follow_path()" repeatedly for trajectory tracking using event scheduler

    Parameters
    ----------
    trajObj : Type[Trajectory]
    """

    print("\nFollowing the trajectory ...")
    
    ts = trajObj.timeStep

    s = sched.scheduler()
    s.enter(ts, 1, _follow_path, argument=(trajObj, s))
    s.run()



def _get_shape_params(required, options, types, choices):
    
    col1 = required + options
    col2 = types
    col3 = choices

    pad1 = max(map(len, col1))
    pad2 = max(map(len, col2))
    pad3 = max(map(len, col3))

    # Shape Properties Table
    print("")
    for name, value, choice in zip(col1, col2, col3):
        print(f'   {col1.index(name)+1}. {name:<{pad1}} | {value:<{pad2}} | {choice:<{pad3}}') 
    print("\n**NOTE: All user inputs should be in \"space-separated\" form")
    
    # Required Properties Entry
    print("\n<<< Required properties >>>")
    reqParam = []
    for prop in required:
        reqParam.append(input(f"{prop}: "))

    # Optional Properties Entry
    if len(options) == 0: # If there is not optional properties
        optParam = None
    
    else: 
        select = ''
        while select.lower() != 'y' and select.lower() != 'n':
            select = str(input("\nDo you want to add optional properties? [Y/n]: "))

        optParam = []
        if select.lower() == 'y':
            print("**NOTE: Leave undesired options empty")
            print("\n<<< Optional properties >>>")
            
            for prop in options:
                s = input(f"{prop}: ")
                if s == "":
                    optParam.append(None)
                else:
                    optParam.append(s)
        
        else:
            
            optParam = [None for i in range(len(options))]


    return reqParam, optParam



def on_press(key):

    if key == keyboard.Key.up:
        x = current_pose[0]
        y = current_pose[1] + 0.001

        try:
            theta1, theta2 = inverseKinematics(x, y)
            pul1 = 1.0 * RESOLUTION * theta1 / (2*pi)
            pul2 = 1.0 * RESOLUTION * theta2 / (2*pi)
            
            # >>> Update Current Pose
            current_pose[0] = x
            current_pose[1] = y

            # >>> Configure ROS message
            print("\nMoving to X: {:.3f} \tY: {:.3f}".format(x, y))
            config = Float32MultiArray()
            config.data = [pul1, pul2, SPEED, SPEED, ACCELERATION, ACCELERATION]
            config_pub.publish(config)
    
        except ValueError:
            print("Cannot reach provided target")


    elif key == keyboard.Key.down:
        x = current_pose[0]
        y = current_pose[1] - 0.001

        try:
            theta1, theta2 = inverseKinematics(x, y)
            pul1 = 1.0 * RESOLUTION * theta1 / (2*pi)
            pul2 = 1.0 * RESOLUTION * theta2 / (2*pi)
            
            # >>> Update Current Pose
            current_pose[0] = x
            current_pose[1] = y

            # >>> Configure ROS message
            print("\nMoving to X: {:.3f} \tY: {:.3f}".format(x, y))
            config = Float32MultiArray()
            config.data = [pul1, pul2, SPEED, SPEED, ACCELERATION, ACCELERATION]
            config_pub.publish(config) 
        
        except ValueError:
            print("Cannot reach provided target")


    elif key == keyboard.Key.left:
        x = current_pose[0] - 0.001
        y = current_pose[1]

        try:
            theta1, theta2 = inverseKinematics(x, y)
            pul1 = 1.0 * RESOLUTION * theta1 / (2*pi)
            pul2 = 1.0 * RESOLUTION * theta2 / (2*pi)

            # >>> Update Current Pose
            current_pose[0] = x
            current_pose[1] = y

            # >>> Configure ROS message
            print("\nMoving to X: {:.3f} \tY: {:.3f}".format(x, y))
            config = Float32MultiArray()
            config.data = [pul1, pul2, SPEED, SPEED, ACCELERATION, ACCELERATION]
            config_pub.publish(config)

        except ValueError:
            print("Cannot reach provided target")


    elif key == keyboard.Key.right:
        x = current_pose[0] + 0.001
        y = current_pose[1]

        try:
            theta1, theta2 = inverseKinematics(x, y)
            pul1 = 1.0 * RESOLUTION * theta1 / (2*pi)
            pul2 = 1.0 * RESOLUTION * theta2 / (2*pi)
            
            # >>> Update Current Pose
            current_pose[0] = x
            current_pose[1] = y

            # >>> Configure ROS message
            print("\nMoving to X: {:.3f} \tY: {:.3f}".format(x, y))
            config = Float32MultiArray()
            config.data = [pul1, pul2, SPEED, SPEED, ACCELERATION, ACCELERATION]
            config_pub.publish(config)
        
        except ValueError:
            print("Cannot reach provided target")


    if key == keyboard.Key.esc:
        listener.stop()



def goHome_response(request):
    # >>> Update Current Pose
    current_pose[0] = 0
    current_pose[1] = 0

    # >>> Configure ROS message
    config = Float32MultiArray()
    config.data = [0, 0, SPEED, SPEED, ACCELERATION, ACCELERATION]
    
    print("Going HOME position ...")
    config_pub.publish(config)

    return TriggerResponse()



def goToPoint_response(request):

    # Service title
    title = "P\noint to Point Navigation"
    print('=' * len(title))
    print(title)
    print('=' * len(title))

    x = request.x / 100 # Unit conversion (cm > m)
    y = request.y / 100 # Unit conversion (cm > m)
    try:
        theta1, theta2 = inverseKinematics(x, y)

        pos1 = 1.0 * RESOLUTION * theta1 / (2*pi)
        pos2 = 1.0 * RESOLUTION * theta2 / (2*pi)

        # >>> Update Current Pose
        current_pose[0] = x
        current_pose[1] = y

        # >>> Configure ROS message
        print("Navigating to X: {:.3f} \tY: {:.3f}".format(x, y))
        config = Float32MultiArray()
        config.data = [pos1, pos2, SPEED, SPEED, ACCELERATION, ACCELERATION]
        config_pub.publish(config)

        return ptpNavResponse()
    
    except ValueError:
        rospy.logerr("Invalid target position [{:.3f},{:.3f}]".format(x, y))
        return ptpNavResponse()



def followShape_response(request):

    # Service title
    title = "Defined Shape Path Tracking"
    print('=' * len(title))
    print(title)
    print('=' * len(title))

    shapes = ["rectangle","circle","ellipse","arc"]
    
    shape: str = request.shape
    
    # Check for valid requested shape
    if shape not in shapes:
        print(f"No defined shape with this name: {shape}")
        return shapeNavResponse()
    
    # Load shapes properties fromm json file
    folderDir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folderDir,'shapesProperties.json'), "r") as read_file:
            data = json.load(read_file)

    shapeObj = Trajectory(showFigure=False)

    # Shape Properties Statement
    print(f"\nRequested \"{shape.capitalize()}\" shape requires the following properties:")

    # Shape selection 
    if shape == shapes[0]: # Rectangle
        reqProp = data[shapes[0]]["required"]
        optProp = data[shapes[0]]["optional"]
        types = data[shapes[0]]["types"]
        choices = data[shapes[0]]["choices"]
        
        reqParams, optParams = _get_shape_params(reqProp, optProp, types, choices)
        
        # Properties Manipulation
        try:
            reqParams = [float(x) for x in reqParams] # Type conversion (str > float)
            reqParams[:4] = [x/100 for x in reqParams[:4]] # Unit conversion (cm > m)
                        
            shapeObj.rectangle_traj(
                height=reqParams[0],
                width=reqParams[1],
                pinPoint=reqParams[2:4], 
                time=reqParams[4],
                anchor=optParams[0],
                direction=optParams[1])
            
        except ValueError as e:
            print(f"Invlaid inputs:\n {e}")
            return
    

    elif shape == shapes[1]: # Circle
        reqProp = data[shapes[1]]["required"]
        optProp = data[shapes[1]]["optional"]
        types = data[shapes[1]]["types"]
        choices = data[shapes[1]]["choices"]

        reqParams, optParams = _get_shape_params(reqProp, optProp, types, choices)
    
        # Properties Manipulation
        try:
            reqParams = [float(x) for x in reqParams] # Type conversion (str > float)
            reqParams[:3] = [x/100 for x in reqParams[:3]] # Unit conversion (cm > m)

            if optParams[0] != None:
                optParams[0] = float(optParams[0])/180*pi # Type + Unit conversion (str/deg > float/rad)

            shapeObj.circle_traj(
                radius=reqParams[0],        
                center=reqParams[1:3], 
                time=reqParams[3],
                startAngle=optParams[0],
                direction=optParams[1])
            
        except ValueError as e:
            print(f"Invlaid inputs:\n {e}")
            return
    

    elif shape == shapes[2]: # Ellipse
        reqProp = data[shapes[2]]["required"]
        optProp = data[shapes[2]]["optional"]
        types = data[shapes[2]]["types"]
        choices = data[shapes[2]]["choices"]

        reqParams, optParams = _get_shape_params(reqProp, optProp, types, choices)

        # Properties Manipulation
        try:
            reqParams = [float(x) for x in reqParams] # Type conversion (str > float)
            reqParams[:4] = [x/100 for x in reqParams[:4]] # Unit conversion (cm > m)

            for i in range(2):
                if optParams[i] != None:
                    optParams[i] = float(optParams[i])/180*pi # Type + Unit conversion (str/deg > float/rad)

            shapeObj.ellipse_traj(            
                center=reqParams[:2],
                xAmp=reqParams[2],
                yAmp=reqParams[3], 
                time=reqParams[4],
                startAngle=optParams[0],
                rotationAngle=optParams[1],
                direction=optParams[2])
            
        except ValueError as e:
            print(f"Invlaid inputs:\n {e}")
            return
    

    elif shape == shapes[3]: # Arc
        reqProp = data[shapes[3]]["required"]
        optProp = data[shapes[3]]["optional"]
        types = data[shapes[3]]["types"]
        choices = data[shapes[3]]["choices"]

        reqParams, optParams = _get_shape_params(reqProp, optProp, types, choices)
    
        # Properties Manipulation
        try:
            reqParams = [float(x) for x in reqParams] # Type conversion (str > float)
            reqParams[:3] = [x/100 for x in reqParams[:3]] # Unit conversion (cm > m)
            reqParams[3] = reqParams[3]/180*pi # Unit conversion (deg > rad)
            reqParams[4] = reqParams[4]/180*pi # Unit conversion (deg > rad)

            shapeObj.arc_traj(
                radius=reqParams[0],        
                center=reqParams[1:3],
                startAngle=reqParams[3],
                endAngle=reqParams[4],
                time=reqParams[5])
            
        except ValueError as e:
            print(f"Invlaid inputs:\n {e}")
            return
    
    
    start_point_nav(shapeObj)
    
    track_trajectory(shapeObj)

    print("COMPLETED!!")

    return shapeNavResponse()
    


def followCustomPath_response(request):
    print(current_pose)

    # Service Title
    title = "Custom Path Tracking"
    print('=' * len(title))
    print(title)
    print('=' * len(title))

    # Instantiate trajectory Object
    customObj = Trajectory()

    # CSV File Description
    print("\n**NOTE:\tFill the \"custom_trajectory.csv\" file with the desired targets")
    print("\n**NOTE:\t1st Column > X coordinates\n\t2nd Column > Y coordinates\n\t3rd Column > Time (Optional)")
    
    # Time Mode Statement
    title = f"Trajectory generation requires one of the following time modes:"
    print("\n", '-' * len(title))
    print(title)
    print("  1. Total Time -> Specify total time for whole trajectory (3RD COLUMN IGNORED)")
    print("  2. Absolute Time -> Specify time for each target at which robot reach")
    print("  3. Increment Time -> Specify duration taken by the robot to reach each waypoint\n")
    

    # Select Time Mode
    print("\n<<< Time Calculation Mode >>>")
    timeMode = None
    totalTime = None

    while timeMode not in ['1','2','3']:
        timeMode = input("Selected mode: ")

        if timeMode == '1':
            totalTime = float(input("Total Time: "))


    # Load CSV file
    folderDir = os.path.dirname(os.path.abspath(__file__))
    rows = []

    with open(os.path.join(folderDir,'custom_trajectory.csv'), 'r') as file:
        csvReader = csv.reader(file)
        
        for row in csvReader:
            rows.append(row)

    
    # Generate trajectory
    customObj.custom_traj(rows, timeMode, totalTime)

    start_point_nav(customObj)
    
    track_trajectory(customObj)

    print("COMPLETED!!")

    return TriggerResponse(message="Ok!")
        


def moveWithKeyboard_response(request):
    global listener

    print("Use keyboard arrows for control")
    print("\n**NOTE: You can cancel usign ESC not Ctrl+C")

    with keyboard.Listener(on_press=on_press) as listener:            
            listener.join()

    return TriggerResponse() 



def goToGoal_response(request):
    # Service title
    title = "\nObstacle-free Goal Navigation"
    print('=' * len(title))
    print(title)
    print('=' * len(title))

    print("*NOTE: You need to specif start and end cell values {Intergers Only} ")
    
    startX = int(input("Start Grid X: "))
    startY = int(input("Start Grid Y: "))
    goalX = int(input("Goal Grid X: "))
    goalY = int(input("Goal Grid Y: "))
    totalTime = float(input("Total Time: "))


    startCell = [startY, startX]
    goalCell = [goalY, goalX]

    gridObj = Trajectory()
    gridObj.grid_trajectory(startCell, goalCell, totalTime)

    # start_point_nav(gridObj)

    # track_trajectory(gridObj)

    print("COMPLETED!!")

    return TriggerResponse()




def main():
    global config_pub

    rospy.init_node('position_planner', anonymous=False)

    config_pub = rospy.Publisher('/cmd_config', Float32MultiArray, queue_size=10)
    rospy.Service('go_home', Trigger, goHome_response)
    rospy.Service('go_to_point', ptpNav, goToPoint_response)
    rospy.Service('follow_shape', shapeNav, followShape_response)
    rospy.Service('follow_custom_path', Trigger, followCustomPath_response)
    rospy.Service('move_with_keyboard', Trigger, moveWithKeyboard_response)
    rospy.Service('go_to_goal', Trigger, goToGoal_response)

    print("\nReady For Commands\n")

    # FOR TEST ONLY

    rospy.spin()



if __name__ == "__main__":
    try:
        main()
        

    except rospy.ROSInterruptException:
        pass