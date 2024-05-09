#!/usr/bin/env python3.8
from typing import Sequence
import matplotlib.pyplot as plt
import matplotlib.patches
import numpy as np
import matlab.engine
import math  
import rospy


class Trajectory:

    def __init__(self, showFigure=True) -> None:
        self.timeStep = 0.05
        self.samples = 0
        self.currentSample = 0
        self.trajectory = None
        self.showFigure = showFigure

        # Start Matlab Engine
        print("\nPreparing trajectory generator ...")
        self.eng = matlab.engine.start_matlab()
        self.eng.cd(r'~/catkin_ws/src/parallel_scara_pkg/scripts/Matlab')


    
    def rectangle_traj(
            self, height: float, width: float, pinPoint: Sequence[float], 
            time: float, anchor: str = 'sw', direction : str = 'ccw') -> matlab.double:
        """
        Generates MATLAB trapeziodal velocity profile trajectory for rectangle shape

        Parameters
        ----------
        height : float
            Rectangle height (vertical side) {METERS}.

        width : float
            Rectangle width (horizontal side) {METERS}.

        pinPoint : Sequence[float]
            XY coordinates of a point at which the rectangle will be pinned {METERS}.

        time : float
            Time taken to complete whole rectangle {SECONDS}.
        
        anchor : {'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'}, optional
            Location of anchor that will be aligned with `pinPoint`, by default 'sw'.

        direction : {'cw', 'ccw'}, optional
            Direction of path following from `pinPoint`, by default 'ccw'.

        Returns
        -------
        matlab.double
            Array of combined time, dist, vel, acc. {METERS}
        """
        
        # Data Validation
        anchor = 'sw' if anchor is None else anchor
        direction = 'ccw' if direction is None else direction 

        # Generate rectangle shape waypoints
        h = matlab.double([height])
        w = matlab.double([width])
        pin = matlab.double([pinPoint])

        waypoints = self.eng.generate_rectangle(h, w, pin, "Anchor", anchor, "Direction", direction)

        # Generate rectangle trajectory profile 
        print("\nGenerating trajectory ...")
        traj = self.eng.generate_trajectory(waypoints, time, self.timeStep)
        
        # Update instance attributes
        self.samples = traj.size[1]
        self.trajectory = traj

        if self.showFigure:
            self._plot_trajectory()

        return traj



    def circle_traj(
            self, radius: float, center: Sequence[float], 
            time: float, startAngle: float = 0, direction : str = 'ccw') -> matlab.double:
        """
        Generates MATLAB trapeziodal velocity profile trajectory for circle shape

        Parameters
        ----------
        radius : float
            Circle radius {METERS}.

        center : Sequence[float]
            Circle center XY coordinates {METERS}.

        time : float
            Time taken to complete whole circle {SECONDS}.
        
        startAngle : float, optional
            Start angle of path following, by default = 0.

        direction : {'cw', 'ccw'}, optional
            Direction of path following from `Start`, by default 'ccw'.

        Returns
        -------
        matlab.double
            Array of combined time, dist, vel, acc. {METERS}
        """
        
        # Data Validation
        startAngle = 0 if startAngle is None else startAngle
        direction = 'ccw' if direction is None else direction 

        # Generate circle shape waypoints
        r = matlab.double([radius])
        c = matlab.double([center])
        start = matlab.double([startAngle])

        waypoints = self.eng.generate_circle(r, c, "Start", start, "Direction", direction)

        # Generate circle trajectory profile 
        print("\nGenerating trajectory ...")
        traj = self.eng.generate_trajectory(waypoints, time, self.timeStep)
        
        # Update instance attributes
        self.samples = traj.size[1]
        self.trajectory = traj

        if self.showFigure:
            self._plot_trajectory()

        return traj



    def ellipse_traj(
            self, center: Sequence[float], xAmp: float, yAmp: float, time: float, 
            startAngle: float = 0, rotationAngle: float = 0, direction : str = 'ccw') -> matlab.double:
        """
        Generates MATLAB trapeziodal velocity profile trajectory for ellipse shape

        Parameters
        ----------
        center : Sequence[float]
            Circle center XY coordinates {METERS}.

        xAmp : float
            X axes length of non-rotated ellipse {METERS}.

        yAmp : float
            Y axes length of non-rotated ellipse {METERS}.

        time : float
            Time taken to complete whole circle {SECONDS}.
        
        startAngle : float, optional
            Start angle of path following, by default = 0.

        rotationAngle : float, optional
            Angle of rotation of the ellipse ccw from +ve x-axis.

        direction : {'cw', 'ccw'}, optional
            Direction of path following from `Start`, by default 'ccw'.

        Returns
        -------
        matlab.double
            Array of combined time, dist, vel, acc. {METERS}
        """
        
        # Data Validation
        startAngle = 0 if startAngle is None else startAngle
        rotationAngle = 0 if rotationAngle is None else rotationAngle
        direction = 'ccw' if direction is None else direction 

        # Generate circle shape waypoints
        c = matlab.double([center])
        xAmplitude = matlab.double([xAmp])
        yAmplitude = matlab.double([yAmp])
        start = matlab.double([startAngle])
        angle = matlab.double([rotationAngle])

        waypoints = self.eng.generate_ellipse(c, xAmplitude, yAmplitude, 
                                             "Start", start, 
                                             "Angle", angle,
                                             "Direction", direction)

        # Generate circle trajectory profile 
        print("\nGenerating trajectory ...")
        traj = self.eng.generate_trajectory(waypoints, time, self.timeStep)
        
        # Update instance attributes
        self.samples = traj.size[1]
        self.trajectory = traj

        if self.showFigure:
            self._plot_trajectory()

        return traj



    def arc_traj(
            self, radius: float, center: Sequence[float], 
            startAngle: float, endAngle:float, time: float) -> matlab.double:
        """
        Generates MATLAB trapeziodal velocity profile trajectory for arc shape

        Parameters
        ----------
        radius : float
            Circle radius {METERS}.

        center : Sequence[float]
            Circle center XY coordinates {METERS}.

        startAngle : float
            Start angle of path following. {METERS}.

        endAngle : float
            End angle of path following. {METERS}.

        time : float
            Time taken to complete whole circle {SECONDS}.


        Returns
        -------
        matlab.double
            Array of combined time, dist, vel, acc. {METERS}
        """

        # Generate circle shape waypoints
        r = matlab.double([radius])
        c = matlab.double([center])
        start = matlab.double([startAngle])
        end = matlab.double([endAngle])

        waypoints = self.eng.generate_arc(r, c, start, end)

        # Generate circle trajectory profile 
        print("\nGenerating trajectory ...")
        traj = self.eng.generate_trajectory(waypoints, time, self.timeStep)
        
        # Update instance attributes
        self.samples = traj.size[1]
        self.trajectory = traj

        if self.showFigure:
            ax = self._plot_trajectory(instantShow=False)
            
            startLineX = np.multiply(np.array([center[0], waypoints[0][0]]),100)
            startLineY = np.multiply(np.array([center[1], waypoints[1][0]]), 100)
            endLineX = np.multiply(np.array([center[0], waypoints[0][-1]]), 100)
            endLineY = np.multiply(np.array([center[1], waypoints[1][-1]]), 100)

            ax.plot(startLineX, startLineY, linestyle='dashed', c = 'red')
            ax.plot(endLineX, endLineY, linestyle='dashed', c = 'green')

            plt.show()

        return traj



    def custom_traj(self, csvData: list, timeMode: str, totalTime: float):
        
        print("\nGenerating trajectory ...")
        
        # Reshape waypoints data
        xVal = []
        yVal = []
        time = []
        for i in range(len(csvData)):
            xVal.append(float(csvData[i][0])/100)
            yVal.append(float(csvData[i][1])/100)
            time.append(float(csvData[i][2]))
        
        waypoints = matlab.double([[xVal], [yVal]])
        time[0] = 0
        time = matlab.double(time)

        if int(timeMode) == 1: # At "Total Time" mode

            traj = self.eng.generate_trajectory(waypoints, totalTime, self.timeStep, "timeMode","dist")

        elif int(timeMode) == 2: # At "Absolue Time" mode
            pass
            traj = self.eng.generate_trajectory(waypoints, time, self.timeStep, "timeMode","abs")

        elif int(timeMode) == 3: # At "Increment Time" mode
        
            traj = self.eng.generate_trajectory(waypoints, time, self.timeStep, "timeMode","inc")


        # Update instance attributes
        self.samples = traj.size[1]
        self.trajectory = traj

        if self.showFigure:
            self._plot_trajectory(customEnds=True)


    
    def grid_trajectory(self, start, goal, time, diagonal = False):

        # Properites Handling
        diagonal = "on" if diagonal == False else "off"

        # Generate occupancy grid waypoints
        occArray = [
            [0, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 1, 0],
            [0, 0, 1, 0, 0, 1, 1, 1, 1],
            [0, 0, 1, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 0, 1],
            [0, 0, 1, 0, 1, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 0, 1, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 1, 1],
            [0, 0, 0, 1, 1, 1, 0, 0, 0]
        ]
        map = matlab.double([occArray])
        startPose = matlab.double([start])
        endPose = matlab.double([goal])

        waypoints = self.eng.solve_occupancyGrid(map, startPose, endPose, "Diagonal", diagonal)

        # Grid Waypoints Conditioning
        # X_grid - 9.5 = cm
        x_grid = waypoints[0]
        x_grid -= 9.5

        # Y_grid + 11.5 = cm
        y_grid = waypoints[1]
        y_grid += 11.5

        print(f"X grid {x_grid}")
        print(f"\n\nY grid {y_grid}")
        # # Generate planner trajectory  
        # print("\nGenerating trajectory ...")
        # traj = self.eng.generate_trajectory(waypoints, time, self.timeStep)
        
        # # Update instance attributes
        # self.samples = traj.size[1]
        # self.trajectory = traj

        # self._plot_trajectory(instant=False)



    def _plot_trajectory(self, instantShow: bool = True, customEnds: bool = False):
        x = np.asarray(self.trajectory[1])*100
        y = np.asarray(self.trajectory[2])*100
        
        plt.rcParams["figure.figsize"] = [7, 3.50]
        plt.rcParams["figure.autolayout"] = True

        fig = plt.figure()
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()

        major_ticksX = np.arange(-20, 20, 5)
        minor_ticksX = np.arange(-20, 20, 1)
        major_ticksY = np.arange(-5, 40, 5)
        minor_ticksY = np.arange(-5, 40, 1)

        ax = fig.add_subplot(1, 1, 1)
        ax.set_xticks(major_ticksX)
        ax.set_xticks(minor_ticksX, minor=True)
        ax.set_yticks(major_ticksY)
        ax.set_yticks(minor_ticksY, minor=True)
        ax.set_aspect('equal')
        ax.autoscale(False, axis='both')
        
        ax.grid(which='both')
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)
        
        stepper1 = plt.Rectangle((-15,-3), 6, 6, fc='black',ec="grey")
        stepper2 = plt.Rectangle((8,-3), 6, 6, fc='black',ec="grey")
        plt.gca().add_patch(stepper1)
        plt.gca().add_patch(stepper2)
        
        # Plot trajectory
        ax.plot(x, y)
        
        # Plot trajectory START point indicator
        ax.plot(x[0], y[0], 'or')

        # Plot trajectory END point indicator
        if customEnds == False:
            idx = math.floor(len(x)*0.99 - 1) # point before END by 0.1%
        else:
            idx = -1

        ax.plot(x[idx], y[idx], 'og')
        
        if instantShow == True:
            plt.show()

        return ax



if __name__ == "__main__":
    rec = Trajectory()
    trajectory = rec.grid_trajectory([3, 9], [15, 9], 8)

