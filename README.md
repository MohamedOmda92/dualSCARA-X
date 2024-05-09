<h1 align="center">
  <br>
	<img width="30%" src="https://www.freelogoservices.com/api/main/images/1j+ojFVDOMkX9Wytexe43D6kh...GFqxNHmRnJwXs1M3EMoAJtlyEoh...Vq9PU...">
  <br>
  SPENSER-pid-control
  <br>
</h1>

<h4 align="center">MATLAB & Simulink repository showcasing forward and inverse kinematics, CAD modeling, and PID control for a serial manipulator.</h4>

<div align="center">
   	<img src="https://img.shields.io/badge/MATLAB-R2023a-orange">
   	<img src="https://img.shields.io/badge/Build-unkown-brightgray?color=a6a6a5">
    	<img src="https://img.shields.io/github/last-commit/MohamedOmda92/SPENSER-PID-Control">
 	<img src="https://img.shields.io/badge/Contributions-Welcome-blue">	
</div>
<div align="center">
	<br>
   	<a target="_blank" href="https://www.linkedin.com/in/mohamed71163"><img height="25" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
	<a target="_blank" href="https://grabcad.com/mohamed.emad-58"><img src="https://github.com/MohamedOmda92/ReadMe-Tester/assets/126765124/faba7fd8-fa48-48f9-a843-4df74d6a19ed"></a>
	<a target="_blank" href="https://www.upwork.com/freelancers/~01f184498499d943ed?viewMode=1"><img height="25" src="https://img.shields.io/badge/UpWork-6FDA44?style=for-the-badge&logo=Upwork&logoColor=white" /></a>	
</div>

<p align="center">
	<br>
	<a href="#basic-overview">Basic Overview</a> •
	<a href="#getting-started">Getting Started</a> •
	<a href="#key-features">Key Features</a> •
	<a href="#future-work">Future Work</a> •	
	<a href="#resources">Resources</a>
</p>


## Basic Overview

"SPENSER" is a project focused on the design and simulation of a serial Cartesian manipulator using SOLIDWORKS, Simscape Multibody, and MATLAB Simulink. It involves CAD modeling, derivation of forward and inverse kinematics, and the implementation of a PID controller for precise control of the manipulator, causing a settling time of approximately 200ms, and zero steady-state error with no overshoot.

<div align="center">
	<img width=22%" src="https://github.com/MohamedOmda92/SPENSER-PID-Control/assets/126765124/b2195b60-5bbc-4781-8f94-96007a29c139">
</div>


## Getting Started

### Prerequisites

1. MATLAB & Some Add-ons
   
   + What MATLAB version to use?
     - MATLAB version <strong>R2023a</strong> is highly recommended. 
   + How to install MATLAB?
     - The most common installation options for MATLAB are presented on [MathWorks Docs](https://www.mathworks.com/help/releases/R2023a/install/install-products.html).
   + What are required Add-ons?
     - Simulink       
     - Simscape Multibody <code style="color:gray"><i>(License Needed)</i></code>
     - Fuzzy Logic Toolbox <code style="color:gray"><i>(License Needed)</i></code>


### Usage
To clone and run this application, you'll need [Git](https://git-scm.com/) and [Node.js](https://nodejs.org/en/download/) 
installed on your computer. Then, from your command line:

```console
# Clone this repository
$ git clone https://github.com/MohamedOmda92/SPENSER-PID-Control
```

Now run `Software\MATLAB\Spenser_Control_System.slx` file, enter the desired XYZ coordinates location (in mm) in the "Constant" Blocks, and
run the simulation.

> You can tune PID controller parameters (gains) by modifying variables saved in Model Workspace. For further details, refer to [Simulink Docs](https://www.mathworks.com/help/simulink/ug/change-model-workspace-data.html)


## Key Features

+ Exceptional Performance:
  - Achieved exceptional performance with a fine-tuned PID controller, showcasing a settling time of approximately 200ms, zero steady-state error, and zero percent overshoot.
+ CAD Modeling:
  - Utilized SOLIDWORKS to design a detailed CAD model of the serial Cartesian manipulator, enabling accurate representation of the mechanical structure including harmonic gears.
+ Kinematics Analysis:
  - Derived and implemented forward and inverse kinematics equations to accurately control the manipulator's movement based on desired XYZ coordinates.
+ PID Control:
  - Integrated and fine-tunned a PID controller into the MATLAB Simulink environment to enhance the manipulator.
+ Simulation Capabilities:
  -  Leveraged MATLAB Simulink to simulate the movement of the manipulator, providing a realistic virtual environment for testing and validation.
  > Note:
  > Refer to <a href="#resources">Resources</a> section for animation videos.
  

## Future work
### 1. Trajectory Planning: 
Implement advanced trajectory planning algorithms to generate smooth and optimized motion paths for the manipulator, considering factors such as acceleration, jerk, and dynamic constraints.

### 2. Dynamic Modeling and Control: 
Enhance the simulation by incorporating dynamic modeling techniques to accurately represent the manipulator's dynamics and explore advanced control strategies like model predictive control (MPC) or adaptive control algorithms.

### 3. Sensor Integration: 
Integrate sensors, such as encoders or vision systems, to provide real-time feedback and enable closed-loop control, enhancing the manipulator's interaction capabilities and robustness in handling uncertainties.


## Resources

+ [Harmonic Gearbox Catalog - Harmonic Drive.pdf](https://github.com/MohamedOmda92/SPENSER-PID-Control/files/15250756/Harmonic.Gearbox.Catalog.-.Harmonic.Drive.pdf)
+ Final Calculation for SPENSER kinematics could be found [here](https://github.com/MohamedOmda92/SPENSER-PID-Control/files/15250760/Spencer.DH.Parameters.pdf)
+ Animation video for custom motion study in SOLDIWORKS could be found <a href="Results/Animations/Conceptual Design V1.mp4">here</a>
+ Animation video for Simscape Multibody simulation could be found <a href="Results/Simulation-Outputs/SPENCER Animation.avi">here</a>