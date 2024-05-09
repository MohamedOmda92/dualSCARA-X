int pulse_per_rev = 6400;
float angle_per_pulse = 1.8 / 32;
float desired_angle;
float current_angle = 0;
float increment_angle;
int analog_val;
int analog_val2; 
double pulses;

void setup() {
  Serial.begin(250000);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
}

void loop() {
  analog_val = analogRead(A0);

  // Check for instability
  /*delay(100);
  analog_val2 = analogRead(A0);
  if (analog_val != analog_val2) {
    Serial.println(abs(analog_val - analog_val2));
  }*/
  
  if (analog_val <= 10) {
    analog_val = 10;
  }
  desired_angle = map(analog_val, 10, 1023, 0, 360);
  increment_angle = desired_angle - current_angle;
  if (increment_angle < 3 and increment_angle > 0) {
    increment_angle = 0;
  }
  // Calculate approx. no. of pulses
  pulses = 1.0 * increment_angle * pulse_per_rev / 360;
  Serial.print("\tPulses: ");
  Serial.println(pulses);
  // Detrmine direction
  if(increment_angle > 0) {
    digitalWrite(2, LOW);
  } else {
    digitalWrite(2, HIGH);
  }

  // Move to desired angle
  for(int i = 0; i < abs(pulses); i++) {
    digitalWrite(3, LOW);
    digitalWrite(3, HIGH);
    delayMicroseconds(60);
  }

  // Serial Printing
  Serial.print("Current: ");
  Serial.print(current_angle);
  Serial.print("\tDesired: ");
  Serial.print(desired_angle);
  Serial.print("\tIncrement: ");
  Serial.print(increment_angle);
  
  
  // Update actual angle
  current_angle += pulses * angle_per_pulse;

  // Reset increment
  increment_angle = 0;
}
