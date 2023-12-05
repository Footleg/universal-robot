#!/usr/bin/env python3
""" Example of a robot using tank steering with two motors for left and right tracks.
    This robot uses the hardware abstraction robot interface to work with a variety of
    hardware. The speed and steering are controlled from the left and right sticks on a
    game controller respectively. Using two sticks, the change handler functions store
    the stick postions in global variables and these are used to update the motor powers
    in the main program loop. Stick mixing is done using an trig based algorithm designed
    by Footleg. The hardware interface is used to import a Robot class for the hardware of
    your actual robot. This is assumed to have a pair of motors, and a set of RGB LEDs.
"""
import pygame #random
import math
from time import sleep
from os import system
from pygamecontroller import RobotController
#from RobotHardware_Virtual import Robot
from RobotHardware_InventorHATmini import Robot

#Initialise global variables
maxMChangeRate = 20.0

power = 0
turn = 0
minMovingSpeed = 10 #Set to the lowest percentage of motor power needed to turn the motors
message = ""
battPowerColour = (0,255,255) # This will get updated to colour indicating battery level
ledPos = 0 #Position of LED scanning cursor used for animation
ledDir = 1 #Direction LED scanning cursor is moving
shutdownFlag1 = False
shutdownFlag2 = False
shutdownFlag3 = False

# Globals used to track the actual applied motor speeds, so changes can be dampened to protect them
realLM = 0.0
realRM = 0.0

# Sets amount speed is divided by to make turns less twitchy
defaultSpeedDampening = 1.3 #1=full batt. voltage, 2=half max speed
slowModeSpeedDampening = 3 #2=half speed, 3=third max speed
speedDampening = defaultSpeedDampening

# Create robot hardware instance
robot = Robot()

def showBatteryStatus(v=0):
    global battPowerColour

    #Show battery level when using default speed
    # Display charge level
    BATT_MIN = 6.5
    BATT_MAX = 8.0
    battery_voltage = v
    r = 120
    g = 60
    if v == 0 :
        battery_voltage = robot.getBatteryVoltage()
        
    if battery_voltage > 0:
        batt_percent = 100 * (battery_voltage - BATT_MIN) / (BATT_MAX - BATT_MIN)
        if batt_percent > 100:
            batt_percent = 100
        elif batt_percent < 0:
            batt_percent = 0
        r = int(120 - 1.2 * batt_percent)
        g = int(batt_percent)
    battPowerColour = (r, g, 0)
    print(f"Motor supply voltage: {battery_voltage:.2f} Colour: {battPowerColour}")

def motorSpeed():
    global power, turn, realLM, realRM, message

    # To reduce stress on the motors we take the power and turn inputs from the driver
    ### New trig based motor power mixing ###
    
    # Power and Steer values create vector. Calculate angle of the vector
    vAngle = math.atan2(turn,power)
    
    # Calculate scale factor to keep vector within bounds of circle
    if abs(power) > abs(turn):
        scaleFactor = math.cos(vAngle)
    else:
        scaleFactor = math.sin(vAngle)
        
    scaleFactor = scaleFactor * scaleFactor * 100
    
    adjPower = power * scaleFactor 
    adjturn = turn * scaleFactor
    lm = adjPower + adjturn
    rm = adjPower - adjturn
    
    # Control speed of change of motor powers to prevent stressing gearboxes with sudden changes
    if abs(realLM - lm) > maxMChangeRate:
        if realLM > lm:
            realLM = realLM - maxMChangeRate
        else:
            realLM = realLM + maxMChangeRate
    else:
        realLM = lm

    if abs(realRM - rm) > maxMChangeRate:
        if realRM > rm:
            realRM = realRM - maxMChangeRate
        else:
            realRM = realRM + maxMChangeRate
    else:
        realRM = rm

    #set the real power for each motor
    robot.setMotorsPower(int(realLM),int(realRM))

    message = f"P:{power:.2f},T:{turn:.2f},A:{vAngle*180/math.pi:.2f},SF:{scaleFactor:.2f},lm:{lm:.2f}/{realLM:.2f},rm:{rm:.2f}/{realRM:.2f}"


def initStatus(status):
    """Callback function which displays status during initialisation"""
    if status == 0 :
        print("Supported controller connected")
        robot.setAllLEDsColor(0,0,255)
    elif status < 0 :
        print("No supported controller detected")
        for i in range(1,7):
            robot.setAllLEDsColor(255,0,0)
            sleep(0.25)
            robot.setLEDsAllOff()
            robot.showLEDs()
            sleep(0.25)
    else :
        print(f"Waiting for controller {status}")
        if status < 9 :
            robot.setLEDColor(status-1,96,0,96)
        elif status < 17 :
            robot.setLEDColor(status-9,96,96,0)
        elif status < 25 :
            robot.setLEDColor(status-17,160,80,0)
        elif status < 33 :
            robot.setLEDColor(status-25,164,2,2)

        robot.showLEDs()


def leftTrigChangeHandler(val):
    """Handler function for left analogue trigger"""
    #Spin left at full speed
    global power, turn
    power = 0
    turn = -(val+1)/2


def rightTrigChangeHandler(val):
    """Handler function for right analogue trigger"""
    #Spin right at full speed
    global power, turn
    power = 0
    turn = (val+1)/2


def leftStickChangeHandler(valLR, valUD):
    """Handler function for left analogue stick"""
    global power
    power = -valUD/speedDampening


def rightStickChangeHandler(valLR, valUD):
    """Handler function for right analogue stick"""
    global turn
    turn = valLR/speedDampening


def leftFrontBtn1Handler(val):
    global speedDampening
    if val == 1 :
        speedDampening = slowModeSpeedDampening # Slow mode
    else :
        speedDampening = defaultSpeedDampening


def rightFrontBtn1Handler(val):
    global speedDampening
    if val == 1 :
        speedDampening = 1 # Fast mode (full speed)
    else :
        speedDampening = defaultSpeedDampening


def hatHandler(valLR, valUD):
    """Handler function for hat 4 way controller"""
    global shutdownFlag1
    
    if valUD == -1:
        shutdownFlag1 = True
    else:
        shutdownFlag1 = False


def squareButtonHandler(btnState):
    """Handler function for square button"""
    global shutdownFlag2
    
    if btnState == 1:
        shutdownFlag2 = True
    else:
        shutdownFlag2 = False


def selectButtonHandler(btnState):
    """Handler function for select button"""
    global shutdownFlag3
    
    if btnState == 1:
        shutdownFlag3 = True
    else:
        shutdownFlag3 = False


def main():
    global message, ledPos, ledDir
    ## Check that required hardware is connected ##

    #Initialise the controller board


    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        cnt = RobotController(robot.getRobotName(), initStatus,
                              leftTriggerChanged = leftTrigChangeHandler,
                              rightTriggerChanged = rightTrigChangeHandler,
                              leftStickChanged = leftStickChangeHandler,
                              rightStickChanged = rightStickChangeHandler,
                              leftBtn1Changed = leftFrontBtn1Handler,
                              rightBtn1Changed = rightFrontBtn1Handler,
                              hatChanged = hatHandler,
                              squareBtnChanged = squareButtonHandler,
                              selectBtnChanged = selectButtonHandler)

        if cnt.initialised :
            keepRunning = True
            #Indicate success here, we are ready to run
            robot.setAllLEDsColor(0,255,0)
            sleep(1)
            showBatteryStatus()
        else :
            keepRunning = False

        battReadInterval = 0
        battReadCounter = 0
        battV = 0
        led1 = 2 #Brightness multiple for LED 1
        led2 = 1 #Brightness multiple for LED 2
        led3 = 0.5 #Brightness multiple for LED 3
        ledUpdateInterval = 0
        ledColour = battPowerColour

        # -------- Main Program Loop -----------
        while keepRunning == True :
            cnt.message = message

            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()

            # Send pulse to watchdog to keep motors alive
            robot.keepAlive()

            message = "Power={0:.2f}, Turn={1:.2f}".format(power,turn)
            message = f"Power={power:.2f}, Turn={turn:.2f}, Shutdown({shutdownFlag1},{shutdownFlag2},{shutdownFlag3})"
            
            motorSpeed()

            #Update LED animation
            ledUpdateInterval += 1
            if ledUpdateInterval > 1:
                if speedDampening == defaultSpeedDampening:
                    ledColour = battPowerColour
                elif speedDampening == slowModeSpeedDampening:
                    ledColour = (0, 0, 100) # Show blue for slow (fine control) mode
                else:
                    ledColour = (100, 0, 0) # Show red for full power (turbo) mode
                ledUpdateInterval = 0
                robot.setLEDsAllOff()
                robot.setLEDColor(ledPos,  int(ledColour[0]*led1), int(ledColour[1]*led1), int(ledColour[2]*led1) )
                ledPos2 = ledPos-ledDir
                if -1 < ledPos2 < 8:
                    robot.setLEDColor(ledPos2, int(ledColour[0]*led2), int(ledColour[1]*led2), int(ledColour[2]*led2) )
                ledPos3 = ledPos2-ledDir
                if -1 < ledPos3 < 8:
                    robot.setLEDColor(ledPos3, int(ledColour[0]*led3), int(ledColour[1]*led3), int(ledColour[2]*led3) )
                robot.showLEDs()
                ledPos += ledDir
                if ledPos > 7:
                    ledDir = -1
                    ledPos = 7
                elif ledPos < 0:
                    ledDir = 1
                    ledPos = 0

            # Read battery voltage no more often than 20 cycles and only when motors are off
            battReadInterval += 1
            if (battReadInterval > 20) and (power == 0) and (turn == 0):
                # Add battery voltage to variable to average after 10 readings
                battV = battV + robot.getBatteryVoltage()
                battReadInterval = 0 # Reset so another read will happen in 20 cycles
                battReadCounter = battReadCounter + 1
                # Update voltage indicator with average voltage reading every 10 reads
                if battReadCounter > 10:
                    showBatteryStatus(battV/battReadCounter)
                    battV = 0
                    battReadCounter = 0

            # Trigger exit if shutdown condition met
            if shutdownFlag1 and shutdownFlag2 and shutdownFlag3:
                keepRunning = False

    finally:
        #Clean up and turn off Blinkt LEDs
        robot.shutdownHardware()
        pygame.quit()

        # Trigger shutdown if condition met
        if shutdownFlag1 and shutdownFlag2 and shutdownFlag3:
            # Only works if running as sudo
            system("shutdown now")


if __name__ == '__main__':
    main()
