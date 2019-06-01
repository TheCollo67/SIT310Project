#define USE_USBCON
#include <Wire.h>
#include <Zumo32U4.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int8.h>

ros::NodeHandle nh;

Zumo32U4LineSensors lineSensors;


bool  lineLeftActive;
bool  lineFrontActive;
bool  lineRightActive;

unsigned int lineSensorValues[3];   //init three

std_msgs::Int8 line_msg;

ros::Publisher pub_line_left("/zumo/line_left", &line_msg);
ros::Publisher pub_line_frontleft("/zumo/line_frontleft", &line_msg);
ros::Publisher pub_line_frontright("/zumo/line_frontright", &line_msg);
ros::Publisher pub_line_right("/zumo/line_right", &line_msg);

void ros_handler( const geometry_msgs::Twist& cmd_msg) {
  float x = cmd_msg.linear.x;
  float y = cmd_msg.linear.y;
  int speed = 100;

  if(x == 1.0) forward(speed);
  if(x == -1.0) backward(speed);
  if(y == 1.0) left(speed);
  if(y == -1.0) right(speed);
  stop();
}

ros::Subscriber<geometry_msgs::Twist> sub("/zumo/cmd_vel", ros_handler);

Zumo32U4Motors motors;

void setup()
{
  nh.initNode();
  nh.subscribe(sub);

  nh.advertise(pub_line_left);
  nh.advertise(pub_line_right);

  lineSensors.initThreeSensors();

  uint16_t defaultBrightnessLevels[] = {1,2,3,4,5,6,7,8,9,10};
}

void publishSensorData()
{
  line_msg.data = lineSensorValues[0]; //left
  pub_line_left.publish( &line_msg);
  pub_line_frontleft.publish( &line_msg);
  line_msg.data = lineSensorValues[2]; //right
  pub_line_right.publish( &line_msg);
  pub_line_frontright.publish( &line_msg);

}

void forward(int time)
{
  motors.setLeftSpeed(100);
  motors.setRightSpeed(100);
  delay(time);
}

void backward(int time)
{
  motors.setLeftSpeed(-100);
  motors.setRightSpeed(-100);
  delay(time);
}

void left(int time)
{
  motors.setLeftSpeed(-100);
  motors.setRightSpeed(100);
  delay(time);
}

void right(int time)
{
  motors.setLeftSpeed(100);
  motors.setRightSpeed(-100);
  delay(time);
}

void stop()
{
  motors.setLeftSpeed(0);
  motors.setRightSpeed(0);
}

void loop()
{
  static uint16_t lastSampleTime = 0;
  if ((uint16_t)(millis() - lastSampleTime) >= 100)
  {
    lastSampleTime = millis();
    lineSensors.read(lineSensorValues,QTR_EMITTERS_ON);
    publishSensorData();
  }
  nh.spinOnce();
  delay(1);
}