# PI-server-rack
A system that allows Monitoring of Raspberry PI('s) and it's running Minecraft Server(s) on PC and Mac as well as controlling their cooling

## Why?
Because I can. Overcomplicated stupid projects are a lot of fun.

## What it is about
The system contains of three parts. Those are the **PC Module**, **RPi Master Module** and **RPi Slave Module**

### To "briefly" explain the concenpt:
- The idea is to have a small server rack containing two Raspberry PI's (PI 4B & PI 1.2B+)
- We will call the PI 4B the *Master* and the PI 1.2B+ will now be the *Slave*
- The Master hosts all the information of its own system (such as CPU temps, frequency, etc.) and the ones from the Slave.
- The PC (or Mac) runs a program that, every cycle, requests all the data from the Master to essentially work as a Monitoring program for both PI's
- Let's introduce the fan control:
    - We have a large 80mm Fan that cools both PI's and a smaller 40mm fan that primarily cools the Master (it requires more cooling due to it being overclocked and its hosted Minecraft servers)
    - The small fan works as following:
        - The small fan is either on at 100% or off at 0%. 
        - As soon as the Master's CPU reaches `50°C` the small fan starts to spin
        - The fan requires a 5V. therefore the additional [fancontrol circuit](#fan-control-circuit):
            - As soon as the dedicated GPIO pin on the Master turns on, the transistor switches on and powers the fan with 5V from the 5V GPIO pin.
    - The large fan works as following:
        - The small fan is either at 25%, 50%, 75% or 100% power
        - As it cools both PI's, it needs to prioritize the cooling requirements of both PI's it always chooses the higher cooling requirment
- Now the Minecraft server(s):
    - The Master hosts two Minecraft servers and currently implemented is the support for a single Minecraft server.
    - The Master collects a variety of informations about the server of choice and throws it together with its other system information to form an array (or list in python) with all the information which then "travels" to the PC

### Required for this to work without any modifications are: 
- 1x PC or macboock
- 2x Raspberry PI's with GPIO Pins (Model A, A+, B or B+), any version works (I use a **Raspberry PI 4 B** and **Raspberry PI 1.2 B+**) and needed power, ethernet, etc. -connections
- 2x cooling fan (I used 1x 5V & 1x 12V fan), external 12V power source (or matching one for the large fan)
- 6x GPIO cables
- fan control pcb with control circuit (The needed circuit is described [here](#fan-control-circuit))

### PC Module
The PC module requests all kinds of system information from both Raspberry PI'S making use of FTP. The Raspberry PI hosts an FTP server from which the PC fetches the text file `output.txt` containing all infos.

### RPi Master Module
The Rpi Master Module (or Raspberry Pi Master module) gets all sorts of informations from its own system and Minecraft Servers and writes them to the `output.txt` file. It also gets fanspeed requirments from the **RPi Slave Module** making use of binary signal transmission over 2 GPIO pins. This module then controls the fan speeds.

### RPi Slave Module
The Rpio Slave Module transmits its fanspeed requirments over 2 GPIO pins to the **RPi Master Module**.

### Setup
## Raspberry PI basic setup
1. Install a UNIX operating of your choice onto both PI's
2. If both PI's are different, declare the more powerful one as the master and install an FTP server on it
3. Install pytho3 on both PI's
4. Go to the [releases page](https://github.com/J-onasJones/PI-MC-WATCHER/releases) and download the latest release.
5. Copy the single programs to their dedicated devices
6. Make the programs run automatically on launch (optional)
7. Edit **IP adresses**, **ports**, **usernames**, **passwords**, **configs**, etc... on all 3 programs
8. Connect 2 GPIO pins from the Slave on pins `GPIO_17` and `GPIO_18` to the Master pins `GPIO_17` and `GPIO_18` (17 to 17  and 18 to 18)
9. Connect the GPIO pins `GPIO_4` and `3.3V OUt` on both PI'S and pin `GPIO_24`, `GPIO_25` and `5V out` of the Master with the fan control circuit board. For pin mapping, view [here](#fan-control-circuit).
10. Connect the cooling fans like shown [here](#fan-control-circuit)

## Fan control circuit

This setup includes a custom designed and built circuit board that manages the cooling fans. The board has the following circuit:

![image](https://user-images.githubusercontent.com/91549607/154872478-d2807b99-3585-4100-b591-f2baa214ea48.png)

### Description
- **S1**: Status Pin for Master PI. Connected to `GPIO_4`
- **S2**: Status Pin for Slave PI. Connected to `GPIO_4`
- **P1**: Power Pin for Master PI. Connected to `3.3V Out`
- **P2**: Power Pin for Slave PI. Connected to `3.3V Out`
- **+ 1**: 12V external Power supply for large cooling fan
- **+ 2**: 5V Power supply for small coolimg fan. Connected to `5V Out` on Master PI
- **- 1**: Ground for 12V external power supply
- **- 2**: Ground for `5V Out` on Master PI
- **\~ 1**: Modulation Pin for large cooling fan. Connected to `GPIO_24` on Master PI
- **\~ 2**: Modulation Pin for small cooling fan. Connected to `GPIO_25` on Master PI
- **XOR 1**: XOR-Gate 1. Determines Master PI status
- **XOR 2**: XOR-Gate 2. Determines slave PI status
- **TR1**, **TR2**, **TR3**: NPN Transistors

# In-more-depth explanation

//TODO
