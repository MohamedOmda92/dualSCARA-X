int pulse_per_rev = 6400;
int desired_angle = 360 * 5;

bool Run;
double pulses;

void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, INPUT);
  digitalWrite(3, LOW);
  
  // Set direction
  if (desired_angle < 0) {
    digitalWrite(2, HIGH);
  }
  else {
    digitalWrite(2, LOW);
  }
  
  pulses = 1.0 * desired_angle * pulse_per_rev / 360;
  Serial.begin(9600); 
}

void loop() {
  Run = digitalRead(4);
  if(Run == 1) {
    for(int i = 0; i < abs(int(pulses)); i++) {
      digitalWrite(3, LOW);
      digitalWrite(3, HIGH);
      delayMicroseconds(12);
    }
  }
}
