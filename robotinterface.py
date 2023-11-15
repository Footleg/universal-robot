#!/usr/bin/env python3
""" 
    Robot hardware abstraction interface

    Copyright (C) 2023 Paul 'Footleg' Fretwell
    Released under the GNU GPL v3 license
    Code repo: https://github.com/Footleg/universal-robot

    This interface provides all the interface methods for a robot, 
    independent of the specific hardware. Robot hardware classes will 
    implement the methods in this interface to make them work with the 
    specific hardware on that robot. At this stage, the interface covers
    twin motor tank steering robots with support for motor encoders, battery
    voltage monitoring and controlling RGB LEDs. There is also support for
    watchdog implementations (to enable robots to automatically shut down if
    communication is broken).

    Using this interface to talk to the robot hardware enables robot control
    programs to be used universally with a variety of robots, each with 
    different hardware. Enhancements made to the Universal Robot program will
    be available on all the robots since one program runs on all of them.
"""
class RobotInterface:
    def shutdownHardware(self):
        """
            Stop all motors and turn off any LEDs and other hardware which
            can be powered down.
        """
        pass

    def getRobotName(self) -> str:
        """
            Returns the name of the robot or hardware
        """
        return "name not set"
        
    
    def setMotorPower(self, motorIndex: int, power: int):
        """
            Set the power for the specified motor of the robot.
            Motors are referenced by index from 0 to n.
            Power levels are a percentage of full power, and can be
            negative to run the motor in reverse. -100 would be full 
            reverse speed. 100 would be full speed forwards.
        """
        pass
    
    def setMotorsPower(self, leftMotor: int, rightMotor: int):
        """
            Set the power for the left and right motors of the robot.
            Power levels are a percentage of full power, and can be
            negative to run the motor in reverse. -100 would be full 
            reverse speed. 100 would be full speed forwards.
        """
        pass
    
    def getEncoderCount(self, motorIndex: int) -> int:
        """
            Read the position of the specified encoder.
            Encoders are referenced by index from 0 to n corresponding
            to the motors.
            Returns the encoder count for the specified motor.
        """
        return 0

    def keepAlive(self):
        """ 
            Keep robot alive. This is a watchdog method to tell the robot
            out code is still talking to it. If this method is not called
            before the watchdog timeout (on robots with a watchdog safety
            implementation) then the robot motors will automatically be 
            powered off.
        """
        pass

    def getBatteryVoltage(self) -> float:
        """ Returns the voltage of the robot battery """
        pass

    def getLEDCount(self) -> int:
        """
            Returns the LED count of the robot
        """
        return 0
        
    def setLEDColor(self, ledIdx: int, red: int, green: int, blue: int):
        """
            Set the colour of an RGB LED on the robot
        """
        pass
        
    def showLEDs(self):
        """
            Update all LEDs with their programmed colours
        """
        pass
        
    def setAllLEDsColor(self, red: int, green: int, blue: int):
        """
            Set the colour of all RGB LEDs on the robot
        """
        pass
    
    def setLEDsAllOff(self):
        """
            Set the colour of all RGB LEDs on the robot
        """
        pass

    def buttonPressed(self, btnIndex: int) -> int:
        """
            Return pressed state of requested button
        """
        return False
        
