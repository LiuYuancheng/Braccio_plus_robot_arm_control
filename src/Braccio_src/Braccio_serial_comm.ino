/**************************************************************************************
 * INCLUDE
 **************************************************************************************/

#include <Braccio++.h>

/**************************************************************************************
 * DEFINES
 **************************************************************************************/

#define TIME_DELAY     2000

/**************************************************************************************
 * CONSTANTS
 **************************************************************************************/

static float const HOME_POS[6] = {157.5, 157.5, 157.5, 157.5, 157.5, 90.0};

/**************************************************************************************
 * GLOBAL VARIABLES
 **************************************************************************************/

static auto gripper    = Braccio.get(1);
static auto wristRoll  = Braccio.get(2);
static auto wristPitch = Braccio.get(3);
static auto elbow      = Braccio.get(4);
static auto shoulder   = Braccio.get(5);
static auto base       = Braccio.get(6);

float angles[6];

void setup() {
  if (Braccio.begin())
  {
    /* Warning:
       Keep a safe distance from the robot until you make sure the code is properly
       working. Be mindful of the robot’s movement prior to that, as it could be
       speedy and accidentally hit someone.
    */

    /* Move to home position. */
    Braccio.moveTo(HOME_POS[0], HOME_POS[1], HOME_POS[2], HOME_POS[3], HOME_POS[4], HOME_POS[5]);
    delay(TIME_DELAY);
    Serial.begin(9600);
    delay(500);
    Serial.println("Braccio robot arm ready!");
  }
}

void loop() {
    String cmd;
    if(Serial.available()){
        cmd = Serial.readStringUntil('\n');
        cmd.trim();
        if(cmd.substring(0,3) == "RST")
        {
            Braccio.moveTo(HOME_POS[0], HOME_POS[1], HOME_POS[2], HOME_POS[3], HOME_POS[4], HOME_POS[5]);
            delay(TIME_DELAY*2);
            Serial.println("RST:Done");
        }else if(cmd.substring(0,3) == "POS"){
          Braccio.positions(angles);
          String posStr = "POS:"+String(angles[0]) +";"+ String(angles[1]) +";"+String(angles[2]) +";"
                    +String(angles[3]) +";"+String(angles[4]) +";"+String(angles[5]) +";"+String(angles[6]);
          Serial.println(posStr);
        } else if (cmd.substring(0,3) == "MOV"){
          String part = cmd.substring(3,7);
          float angle = cmd.substring(7).toFloat();
          if(part == "grip"){
            gripper.move().to(angle); delay(TIME_DELAY);
          } else if (part == "wrtR"){
            wristRoll.move().to(angle); delay(TIME_DELAY);
          } else if (part == "wrtP"){
            wristPitch.move().to(angle); delay(TIME_DELAY);
          } else if (part == "elbw"){
            elbow.move().to(angle); delay(TIME_DELAY);
          } else if (part == "shld"){
            shoulder.move().to(angle); delay(TIME_DELAY);
          } else if (part =="base") {
            base.move().to(angle); delay(TIME_DELAY);
          } else{
            Serial.println("notSupportAct.");
          }
        }
    }
}
