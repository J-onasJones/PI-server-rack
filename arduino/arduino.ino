// options for both vs code and arduino IDE
//include arduino installed libs
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>
#include <Thread.h>
#include <ThreadController.h>
// include local libs
#include "libs/SoftwareSerial/SoftwareSerial.h"
#include "libs/LiquidCrystal/LiquidCrystal.h"
#include "libs/ArduinoThread/Thread.h"
#include "libs/ArduinoThread/ThreadController.h"
//#include "src/LcdControl.h"

/*
Pinmap:
  - 1 LCD                                        1x 6 pins
  - 2 software serial ports (one for each pi)    2x 2 pins
  - 2 analog shunt voltage measurement pins      2x 1 pins
  - 6 buttons for manual display and fan control 6x 1 pins

Notepad:

  - serial message distributor:
    - check recipiant of serial message and forward it to said device
  
  - collect data of package loss, respond times, etc...
  - drive display (show stats such as cpu temps, cpu usage, system load, uptime, server status, power usage, etc.)
  - accept button input from button panel

*/

SoftwareSerial pi4(6, 7); // Softwareserial connection for Raspery Pi 4
SoftwareSerial pi1(8, 9); // SoftwareSerial connection for Raspery Pi 1.2B+

LiquidCrystal lcd(12, 11, 5, 4, 3, 2); // Initialize the LCD displays

ThreadController master = ThreadController(); // initialize ThreadController

Thread serialhandler = Thread(); // initialize Thread for serial handler
Thread lcdcontrol = Thread(); // initialize Thread for lcd control
Thread telemetryhandler = Thread(); // initialize Thread for telemetry handler

void setup() {

  lcd.begin(16, 2); // Set the LCD size to 16x2

  Serial.begin(9600);       // Serial connection for desktop
  pi4.begin(9600);          // SoftwareSerial connection for Raspery Pi 4
  pi1.begin(9600);          // SoftwareSerial connection for Raspery Pi 1.2B+

  serialhandler.setInterval(0);
  serialhandler.onRun(serialDeliverThreadHandler);

  lcdcontrol.setInterval(100);
  lcdcontrol.onRun(lcdControlThreadHandler);

  telemetryhandler.setInterval(1000);
  telemetryhandler.onRun(telemetryThreadHandler);

  master.add(&serialhandler); // add serial handler to ThreadController
  master.add(&lcdcontrol); // add lcd control to ThreadController
  master.add(&telemetryhandler); // add telemetry handler to ThreadController


  while (!Serial || !pi4 || !pi1) {
    ; // wait for serial port to connect
  }

}

void loop() {
  master.run(); // run ThreadController

}


void serialDeliverThreadHandler()  {
  Serial.println("serialDeliverThreadHandler");
}

void lcdControlThreadHandler() {
  Serial.println("lcdControlThreadHandler");
}
void telemetryThreadHandler() {
  Serial.println("telemetryThreadHandler");
}