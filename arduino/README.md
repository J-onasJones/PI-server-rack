# Arduino module

## task
The Arduino module manages the overall assets of the server rack. Those are the LCD display, the button panel and the internal and external serial communication between the computer, Raspberry PI4,  Raspberry PI1.2 and itself. It also collects data about the system such as package loss, etc...

## Build from source
1. The following packages/programs need to be installed and setup:

    - arduino-cli with the following libraries installed (or use libs provided in `libs/`):
        - SoftwareSerial
        - LiquidCristal
    - git (or clone repository manually) 

2. open a terminal and run the following commands:

```
git clone https://github.com/J-onasJones/PI-server-rack.git
cd PI-server-rack
arduino-cli --fqbn [arduino board of your choice] arduino
```
3. to upload the sketch to an arduino run the following command:
```
arduino-cli upload --fqbn [arduino board of your choice] -p [arduino port name] arduino
```
As an example on Linux for the `Arduino Nano` the following:
```
arduino-cli upload --fqbn arduino:avr:nano -p /dev/ttyUSB0 arduino
```



## Credits and Licensing

This project is licensed under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

### Libraries
All provided license files for the arduino libraries at `/arduino/libs` of this repository have been added to the top of the header file of each library (the files ending in `.h`) if provided or required.