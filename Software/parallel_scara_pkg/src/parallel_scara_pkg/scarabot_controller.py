#!/usr/bin/env python3.8

import rospy
import time
import sched
import numpy as np
from pynput import keyboard
from typing import Sequence, Type
from math import pi, sqrt, sin, cos, asin, acos, atan
from std_msgs.msg import Float32MultiArray
from parallel_scara_pkg.trajectory import Trajectory



# Global CONSTANTS & Variables
RESOLUTION = 6400
SPEED = 4000
ACCELERATION = 4000
HOME_POSE = [0.0985, 0.2039]



class scarabotController():

    def __init__(self) -> None:

        rospy.init_node('position_planner', anonymous=False)

        self.config_pub = rospy.Publisher('/cmd_config', Float32MultiArray, queue_size=10)

        self.home_pose = [0.0985, 0.2039]
        self.current_pose = [0.0985, 0.2039]



    def movewithKeys(self, direction: str, resolution: int) -> None:
        step = resolution*0.001

        if direction == "ul":
            x = self.current_pose[0] - step
            y = self.current_pose[1] + step
        elif direction == 'u':
            x = self.current_pose[0]
            y = self.current_pose[1] + step
        elif direction == 'ur':
            x = self.current_pose[0] + step
            y = self.current_pose[1] + step
        elif direction == 'l':
            x = self.current_pose[0] - step
            y = self.current_pose[1]
        elif direction == 'r':
            x = self.current_pose[0] + step
            y = self.current_pose[1]
        elif direction == 'dl':
            x = self.current_pose[0] - step
            y = self.current_pose[1] - step
        elif direction == 'd':
            x = self.current_pose[0]
            y = self.current_pose[1] - step
        elif direction == 'dr':
            x = self.current_pose[0] + step
            y = self.current_pose[1] - step

        try:
            theta1, theta2 = self._inverseKinematics(x, y)
            pul1 = 1.0 * RESOLUTION * theta1 / (2*pi)
            pul2 = 1.0 * RESOLUTION * theta2 / (2*pi)
            
            # >>> Update Current Pose
            self.current_pose[0] = x
            self.current_pose[1] = y

            # >>> Configure ROS message
            config = Float32MultiArray()
            config.data = [pul1, pul2, SPEED, SPEED, ACCELERATION, ACCELERATION]
            self.config_pub.publish(config)

            print("Moved to X: {:.3f}\tY: {:.3f}".format(x,y))
    
        except ValueError:
            print("Cannot reach provided target")



    def goHome(self) -> None:
        """
        Navigates to Home position
        """

        x = self.home_pose[0]
        y = self.home_pose[1]

        print(x)
        print(y)

        try:
            theta1, theta2 = self._inverseKinematics(x, y)
            pul1 = 1.0 * RESOLUTION * theta1 / (2*pi)
            pul2 = 1.0 * RESOLUTION * theta2 / (2*pi)
            
            # >>> Update Current Pose
            self.current_pose[0] = x
            self.current_pose[1] = y

            # >>> Configure ROS message
            config = Float32MultiArray()
            config.data = [pul1, pul2, SPEED, SPEED, ACCELERATION, ACCELERATION]
            self.config_pub.publish(config)

            print("Home reached successfully")
    
        except ValueError:
            print("Cannot reach provided target")
    

    
    def setHome(self, xy: Sequence[float]) -> None:
        """
        Sets new Home position
        """

        self.home_pose[0] = xy[0]
        self.home_pose[1] = xy[1]

        print("Successfully Set to X: {:.3f}\t Y: {:.3f}".format(xy[0],xy[1]))



    def resetHome(self) -> None:
        """
        Resets original Home position
        """
        self.home_pose = [0.0985, 0.2039]
        print("Successfuly Reseted")
        print(self.home_pose[0])
        print(self.home_pose[1])



    def goToPoint(self, xy: Sequence[float]) -> None:
        """ 
        Navigates to target position
        """

        x = xy[0]
        y = xy[1]

        try:
            theta1, theta2 = self._inverseKinematics(x, y)

            pos1 = 1.0 * RESOLUTION * theta1 / (2*pi)
            pos2 = 1.0 * RESOLUTION * theta2 / (2*pi)

            # >>> Update Current Pose
            self.current_pose[0] = x
            self.current_pose[1] = y

            # >>> Configure ROS message
            config = Float32MultiArray()
            config.data = [pos1, pos2, SPEED, SPEED, ACCELERATION, ACCELERATION]
            self.config_pub.publish(config)
            
            print("Reached to X: {:.3f} \tY: {:.3f}".format(x, y))
        
        except ValueError:
            rospy.logerr("Invalid target position [{:.3f},{:.3f}]".format(x, y))
        

    
    def followShape(self, shape: str, reqParams: str, optParams: str) -> None:

        shapes = ["Rectangle","Circle","Ellipse","Arc"]
        shapeObj = Trajectory(showFigure=False)

    
        # Shape selection 
        if shape == shapes[0]: # Rectangle
            
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
                
                print("Trajectory GENERATED")
            except ValueError as e:
                print(f"Invlaid inputs:\n {e}")
                return

        return shapeObj



    def start_point_nav(self, trajObj: Type[Trajectory]) -> None:
        
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

            theta1, theta2 = self._inverseKinematics(q1_initial, q2_initial)

            pos1 = 1.0 * RESOLUTION * theta1 / (2*pi)
            pos2 = 1.0 * RESOLUTION * theta2 / (2*pi)
            
        except ValueError:
            rospy.logerr("Invalid starting target position [{:.3f},{:.3f}]".format(q1_initial, q2_initial))
            return
        
        # >>> Update Current Pose
        self.current_pose[0] = q1_initial
        self.current_pose[1] = q2_initial

        # >>> Configure ROS message
        print("\nMoving to the start position ...")
        config = Float32MultiArray()
        config.data = [pos1, pos2, SPEED/2, SPEED/2, ACCELERATION, ACCELERATION]
        self.config_pub.publish(config)
        
        # NEEDS TO BE DETERMINED (SOFT CODED)
        for i in range(10):
            print(f"Start after: {10-i}")
            time.sleep(1)



    def track_trajectory(self, trajObj: Type[Trajectory]) -> None:
        """
        Executes "_follow_path()" repeatedly for trajectory tracking using event scheduler

        Parameters
        ----------
        trajObj : Type[Trajectory]
        """

        print("\nFollowing the trajectory ...")
        
        ts = trajObj.timeStep

        s = sched.scheduler()
        s.enter(ts, 1, self._follow_path, argument=(trajObj, s))
        s.run()



    def _inverseKinematics(self, X: float, 
                        Y: float) -> float:
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
        float
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
    


    def _inverseJacobin(self, th1: float, 
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



    def _follow_path(self, trajObj: Type[Trajectory], scheduler=None):
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
            theta1, theta2 = self._inverseKinematics(x_goal, y_goal)
            pos1 = 1.0 * RESOLUTION * theta1 / (2*pi)
            pos2 = 1.0 * RESOLUTION * theta2 / (2*pi)


            # >>> Setting up velocity
            th_dot1, th_dot2 = self._inverseJacobin(theta1, theta2, Xd, Yd, x_goal, y_goal)
            vel1 = 1.0 * RESOLUTION * th_dot1 / (2*pi)
            vel2 = 1.0 * RESOLUTION * th_dot2 / (2*pi)
            
            # >>> Update Current Pose
            self.current_pose[0] = x_goal
            self.current_pose[1] = y_goal

            # >>> Configure ROS message
            config = Float32MultiArray()
            config.data = [pos1, pos2, abs(vel1), abs(vel2), ACCELERATION, ACCELERATION]
            
            self.config_pub.publish(config)

            # Iterator Increment
            trajObj.currentSample += 1

            # Terminate Condition
            if sample_idx < samples-1:
                scheduler.enter(ts, 1, self._follow_path, argument=(trajObj, scheduler))

        except ValueError as e:
            rospy.logerr("Invalid target position [{:.3f},{:.3f}]".format(x_goal, y_goal))

