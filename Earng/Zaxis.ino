#include <AccelStepper.h>
#include <Servo.h>
// Define a stepper and the pins it will use

#define Limit_sw 4
AccelStepper mystepper(1, 9, 11); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

unsigned long previousMillis = 0;        // will store last time LED was updated
char Trajectory_Flag = 0;
char direct;
float Tf;
char sign;

volatile unsigned char FreshBuffer = 0;
unsigned char Recieve[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};


// constants won't change:
const long interval = 2;           // interval at which to blink (milliseconds)
float zf, zi, a0, a1, a2, a3;

unsigned char Uart_buffer[9];

// ====================================== servo ========================================
Servo jaw;
Servo rotate;

void setupServo() {
  jaw.attach(5);
  rotate.attach(6);
}
void ServoTest() {

  rotate.write(0);
  jaw.write(0);
  delay(1000);
  rotate.write(180);
  jaw.write(180);
  delay(1000);
}

void GripperHold() {
  jaw.write(0);
}

void GripperRelease() {
  jaw.write(90);
}

void RotateGripper(char angle) {
  rotate.write(angle);

}
// ========================================== STEP =================================================
void setupStepper() {
  mystepper.setMaxSpeed(500000);
  mystepper.setAcceleration(500000);
  pinMode(Limit_sw, INPUT);    // sets the digital pin 13 as output
  // put your setup code here, to run once:
  pinMode(10, OUTPUT);    // sets the digital pin 13 as output
  pinMode(12, OUTPUT);    // sets the digital pin 13 as output
  digitalWrite(10, LOW);
  digitalWrite(12, LOW);
}
void pickup() {

  RotateGripper(180);
  GripperRelease();
  moveto(260.00);
  delay(5000);
  GripperHold();
  delay(5000);
  //  moveto(1.00, -1);
}
void sethome() {
  RotateGripper(0);
  GripperHold();
  mystepper.setSpeed(80000);
  mystepper.setAcceleration(80000);
  mystepper.moveTo(-400000);
  //  while (mystepper.currentPosition() != 5000) // Full speed up to 300
  while (digitalRead(Limit_sw) != 0) {
//    Serial.println(mystepper.currentPosition());
    mystepper.run();
    // Full speed up to 300
  }
  //   while (digitalRead(Limit_sw) != 0) // Full speed up to 300
  mystepper.stop(); // Stop as fast as possible: sets new target
  // Now stopped after quickstop
  mystepper.setCurrentPosition(0);

  delay(1000);

  //  moveto(3400.00, 1);
  //  mystepper.setCurrentPosition(0);
  Serial.print('F');
  Serial.println('0');
}

void moveto(float mm) {
  mystepper.setSpeed(80000);
  mystepper.setAcceleration(80000);
  int Step =  mm_to_step(mm);
  mystepper.moveTo(Step);
  //  mystepper.moveTo(2000);
  //  Serial.println(mystepper.currentPosition());
  mystepper.runToPosition();
  // Full speed up to 300
  //  mystepper.stop(); // Stop as fast as possible: sets new target
  // Now stopped after quickstop
  Serial.print('F');
  Serial.println('4');
}

// =============================== STEP2MM ===============================
float step_to_mm(long int stepp) {
  return (((float)stepp) * 40 / 1600);
}

long int mm_to_step(float mm) {
  return (long int)((mm ) * 1600 / 40);
}

// ============================== TRAJECTORY ===============================

void TryTrajectory(float Zf, unsigned char R) {
  Serial.println("Traj start");
  // trajectory
//  zf = mm_to_step(Zf);
  zf = Zf;
  zi = step_to_mm(mystepper.currentPosition());
  Serial.print("Position set mm: ");
  Serial.print(Zf);
  Serial.print("Position now: ");
  Serial.print(zi);
  Serial.print("Last Position: ");
  Serial.println(zf);
  //      if (zf>=0){
  //        direct = 1;
  //      }
  //      else{
  //        direct = -1;
  //      }
  RotateGripper(R);
  //      send_package(0x544A);       // send TJ
  Tf = 6.00;
  a2 = ((3) * abs(zf - zi)) / (Tf * Tf);
  a3 = ((-2) * abs(zf - zi)) / (Tf * Tf * Tf);
  Trajectory_Flag = 1;
  if ((zf - zi) < 0) {
    sign = -1;
  }
  else {
    sign = 1;
  }
//  Serial.println(zi);
}

void Time() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= 10) {
    previousMillis = currentMillis;

    Trajectory();
  }
}

float Trajectory() {
  static float t = 0;
  if (t >= 6.50) {
    Trajectory_Flag = 0;
    t = 0;
  }
  else {
    //    Serial.println(t);

    float zt = a2 * (t * t) + a3 * (t * t * t);
    zt = zi + zt * sign;
//    Serial.print(zt);
//    Serial.print(": ");
    double diff_zt = 2*a2*t*1000 + 3*a3*(t * t*1000*1000);
//    Serial.print(diff_zt);
//    Serial.print(": ");
    double diff_diff_zt = 2*a2 + 6*a3* t*1000;
//    Serial.println(diff_diff_zt);
    mystepper.moveTo(mm_to_step(zt));
    mystepper.setSpeed(mm_to_step(diff_zt));
//    mystepper.setSpeed((abs(zt - mystepper.currentPosition()) / 0.0015));
//    mystepper.setAcceleration(diff_diff_zt);
    mystepper.setAcceleration(mm_to_step(diff_diff_zt));
    mystepper.runToPosition();

    //    vt =  2*c2*t + 3*c3*t.^2;
    t += 0.01; // 10 ms
  }
}


// =============================== COMMAND ===============================
void CommandSet() {
  //      Serial.println('9');
  static unsigned char command = 9;
  // check if there is a new command
  if (FreshBuffer == 1) {
    Serial.write('i');
    command = Recieve[0];
    FreshBuffer = 0;
    //        printf("BUFFER: %x\n", buffer[0]);
  }
  if (command == 0) {
    Serial.write(0x01);
    sethome();
    Trajectory_Flag = 0;
    command = 9;
  }
  if (Trajectory_Flag == 0) { // cp way to act
    if (command == 1) {
      Serial.write('1');
      //      moveto(340.00, 1);
      //      RotateGripper(67);
      //      GripperHold();

      command = 9;
    }
    else if (command == 2) {
      unsigned int Zpos = ((Recieve[1] << 8) | Recieve[2]);
      unsigned char degree = Recieve[3];
      RotateGripper(degree);
      if (Recieve[4] > 0) {
        GripperRelease();
      }
      else {
        GripperHold();
      }
      moveto((float)Zpos / 100.00);
      Serial.write(0x02);
      command = 9;
    }
    else if (command == 3) {
      Serial.write('3');
      TryTrajectory((((Recieve[1] << 8) | Recieve[2] )/ 100.00), Recieve[3]);
      command = 9;
    }
    else {
      command = 9;
    }
  }
  else {
    command = 9;
  }
}

// =============================== UART ===============================
void VilgaxRead()
{
  static unsigned char Return[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  unsigned char data;
  static int datacount = 0;
  while (Serial.available() > 0) {
    data = Serial.read();
    if (datacount <= 1) {
      if (data == 0xFF) {
        datacount++;
      }
      else {
        datacount = 0;
      }
    }
    else if ((datacount > 1) && (datacount < 10)) {
      Return[datacount - 2] = data;
      datacount++;
    }
    else if (datacount == 10) {
      char j;
      unsigned char keep = 0;
      for (j = 0; j < 8; j++) {
        keep += Return[j];
      }
      //      printf("print data %x, keep %x\n", data, keep);
      if (data == (unsigned char)keep) {
        Serial.write('p');
        for (j = 0; j < 8; j++) {
          Recieve[j] = Return[j];
        }
        FreshBuffer = 1;
      }
      datacount = 0;
    }
    else {
      datacount = 0;
    }
  }
}

// =============================== MAIN CODE ===============================
void setup()
{
  Serial.begin(115200);
  setupStepper();
  setupServo();
//  sethome();
  
//  TryTrajectory(100, 10);
  //  mystepper.setCurrentPosition(0);
  //  moveto(370.00, 1);
  //  RotateGripper(67);
  //  GripperHold();
//      TryTrajectory();
  //    RotateGripper(65);
  //  GripperRelease();
  //    pickup();
  //        moveto(200.00, 1);

}

void loop()
{
  if (Trajectory_Flag) {
    Time();
  }
  //      ServoTest();
  //      Serial.println(mystepper.currentPosition());
  //      Serial.print(digitalRead(Limit_sw) );
  VilgaxRead();
  CommandSet();
}
