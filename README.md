# Braccio_Plus_Robot_Arm_Controller
The robot arms are widely used in the Industry 4.0 scenario such as create smart factories with the interconnection of systems that can exchange data, integrate the entire production chain and make decentralized decisions. We want to create a robot arm control software (UI) which help user to remote control the [Braccio++ Robot Arm](https://store.arduino.cc/products/braccioplusplus) via serial port, UDP or TCP and let the robot do some complex actions sequence (such as grab a box and transfer the boxes on to canvas conveyer). The program is design for below purpose: 

- **Testing** : For user who want to try, learn and test their Braccio robot arm. 
- **Education** : User for hands one usage cases or class demo for robot ICS / IOT course . 
- **Development/Demo** : For people who want to build a smart factories model for demo and research. 

[TOC]



------

### Introduction

**Background Introduction** 

The Industry 4.0, or the 4th Industrial Revolution, was made possible by developing new technologies such as cyber-physical systems, the Internet of Things, cloud computing, cognitive computing, and Artificial Intelligence. 

Arduino Braccio ++ offers a multitude of expansive possibilities from the very outset, including a new Braccio Carrier with LCD screen, new RS485 servo motors, and a totally enhanced experience. Detailed introduction please refer to the Braccio official website: https://store.arduino.cc/products/braccioplusplus

The Braccio_Plus_Robot_Arm_Controller provide the Arduino firmware and UI based controller program for user to remote  control the Braccio ++ via serial port, UDP or TCP and let the robot do some complex actions. This is a example to let the robot arm to execute a box transfer playbook:

 ![](doc/img/grabbox.gif)

Our program contents 2 parts: 

**Braccio ++ Arduino firmware** :  The firmware program running on the Braccio's [Arduino Nano RP2040 Connect](https://docs.arduino.cc/hardware/nano-rp2040-connect) to accept the control request from the controller then drive the motors to make the robot arm to finish the action.

**Braccio ++ Controller UI** : The controller with a GUI for user to remote control the robot arm through wire connection (serial comm) or wireless connection (Wifi TCP/UDP comm). It will provide the function to user to :

1. Display the real time potentiometer position / state for the robot arm's six parts (`gripper`, `wristRoll`, `wristPitch`, `elbow`, `shoulder`, `base`) . 
2. Control the 6 Servo motor (M1 ~ M6) to move the arm. 
3. Allow user to reset the robot arm position, and load the arm action "playbook" to make the arm to finish the complex action. 

Controller UI screen shot: 

![](doc/img/controller_ui_mid.png)





------

### Program Design

This session will introduce the detail design Braccio ++ Arduino firmware and Braccio ++ Controller UI. The program workflow diagram is shown below:

 ![](doc/img/workflow.png)

**Braccio ++ Arduino firmware** 

The Braccio ++ Arduino firmware will be load in to the Arduino Nano RP2040 board, it contents 2 main parts: 

- Communication handling : for different firmware (`Braccio_serial_comm.ino`, `Braccio_tcp_comm.ino`, `Braccio_udp_comm.ino`), they will provide different communication protocol handler to receive the control request from controller and feed back the action execution result / state . 
- Request handling : based on the request, call different API to control the robot arm and the components on the Arduino carrier board. 

**Braccio ++ Controller UI** 

The Braccio ++ Controller UI will run on user's computer with 2 thread; 

- GUI thread : The user interface to handle user's control action. 
- Request & responds manager thread : convert user's action to robot arm control request, send the request to the  Braccio ++ Arduino firmware and feed back the data / action execution result to UI. 

The user interface design is shown below: 

![](doc/img/ui_design.png)

The user's control requests will be put in controller's tasks manager queue and send to the Braccio ++ in sequence, so the user can change the motor angle when the arm is moving, the arm finished one action, it will send back the action finished response, then the controller will dequeue the new task and send to the Braccio ++ arm. If the user press the reset button, the tasks queue will be clear and the program will send the reset command to the Braccio ++.  Each arm parts angle , potentiometer reading will be displayed on the related arm part's control panel.

 





