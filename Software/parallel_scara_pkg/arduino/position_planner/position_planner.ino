/*
 * To tune stepper motors, you basically need to make 2 steps:
 * 1. rostopic pub --once /cmd_angles "YOUR DESIRED ANGLES FOR EACH MOTOR"
 * 2. Re-upload this code to the arduino, so that the current steppersposition is the home
 */

#include "ros.h"
#include <std_msgs/Float32MultiArray.h>
#include <AccelStepper.h>


// Steppers Connections
int dir1 = 2; //left motor
int pul1 = 3; //left motor
int dir2 = 4; //right motor
int pul2 = 5; //right motor


// Stepper Definitions
AccelStepper stepper1(1, pul1, dir1);
AccelStepper stepper2(1, pul2, dir2);
int Resolution = 6400; //pulses per revolution
int Speed = 4000; //pulses per second (DEFAULT)
int Acc = 4000; //pulses per squared second (DEFAULT)
double pulses_1; //==================
double pulses_2; //==================
float pos1 = 0;
float pos2 = 0;
float vel1 = Speed;
float vel2 = Speed;
float acc1 = Acc;
float acc2 = Acc;


// ROS Definitions
ros::NodeHandle nh;



void config_Cb(const std_msgs::Float32MultiArray& msg){
  
  pos1 = msg.data[0];
  pos2 = msg.data[1];
  
  vel1 = msg.data[2];
  vel2 = msg.data[3];
}


ros::Subscriber <std_msgs::Float32MultiArray> config_sub("/cmd_config", &config_Cb);



void setup() { 
  // ROS Configuration
  nh.initNode();
  nh.subscribe(config_sub);


  // Steppers Configurations
  stepper1.setCurrentPosition(0);
  stepper2.setCurrentPosition(0);
  stepper1.setMaxSpeed(Speed);
  stepper1.setAcceleration(Acc);
  stepper2.setMaxSpeed(Speed);
  stepper2.setAcceleration(Acc);
}



void loop()
{
  // Move to destination
  stepper1.moveTo(pos1);
  stepper2.moveTo(pos2);

  //stepper1.setSpeed(vel1); //Commented in TASK SPACE
  //stepper2.setSpeed(vel2); //Commented in TASK SPACE
  
  //stepper1.runSpeedToPosition(); //Commented in TASK SPACE
  //stepper2.runSpeedToPosition(); //Commented in TASK SPACE

  stepper1.run(); //Commented in JOINT SPACE
  stepper2.run(); //Commented in JOINT SPACE
  
  nh.spinOnce();
  delayMicroseconds(100);
}





// ROS logging non-string values
/*char result[8];
    char log_msg[80];
    
    dtostrf(pulses_1, 6, 2, result);
    sprintf(log_msg, "Current pulses_1: ", result);
    nh.loginfo(log_msg);*/
