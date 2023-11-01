#!/usr/bin/env python3
""" Example of a robot using tank steering with two motors for left and right tracks.
    This robot uses the Intentor HAT mini board from Pimoroni.
"""
from robotinterface import RobotInterface
from inventorhatmini import InventorHATMini, MOTOR_A, MOTOR_B, NUM_LEDS
from ioexpander.common import PID, NORMAL_DIR, REVERSED_DIR
from inventorhatmini.plasma import Plasma

class Robot(RobotInterface):
    _instance = None

    """ Prevent multiple instances of robot class in same program """
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Constants
        GEAR_RATIO = 50                         # The gear ratio of the motors
        
        # Create a new InventorHATMini (this will init the LEDs so needs sudo privileges)
        self.board = InventorHATMini(motor_gear_ratio=GEAR_RATIO,init_leds=True)

        # Access the motors from Inventor and enable them
        self.m1 = self.board.motors[MOTOR_A]
        self.m2 = self.board.motors[MOTOR_B]

        # Set up the encoders
        self.enc1 = self.board.encoders[MOTOR_A]
        self.enc2 = self.board.encoders[MOTOR_B]

        # Set the motor and encoder's directions for this robot
        self.m1.direction(NORMAL_DIR)
        self.enc1.direction(NORMAL_DIR)
        self.m2.direction(NORMAL_DIR)
        self.enc2.direction(NORMAL_DIR)

        # Enable the motors
        self.m1.enable()
        self.m2.enable()

    def shutdownHardware(self):
        # Stop motors
        self.m1.disable()
        self.m2.disable()
        print("Motors disabled")
        self.setLEDsAllOff()

    def setMotorPower(self, motorIndex: int, power: int):
        """
            Set the power for the specified motor of the robot.
            Motors are referenced by index from 0 to n.
            Power levels are a percentage of full power, and can be
            negative to run the motor in reverse. -100 would be full 
            reverse speed. 100 would be full speed forwards.
        """
        if motorIndex == 0:
            self.m1.speed(-power/100)
        elif motorIndex == 1:
            self.m2.speed(power/100)

    def setMotorsPower(self, leftMotor: int, rightMotor: int):
        """
            Set the power for the left and right motors of the robot.
            Power levels are a percentage of full power, and can be
            negative to run the motor in reverse. -100 would be full 
            reverse speed. 100 would be full speed forwards.
        """
        #set the power for each motor
        self.m1.speed(-leftMotor/100)
        self.m2.speed(rightMotor/100)
    
    def getEncoderCount(self, motorIndex: int):
        """
            Read the position of the specified encoder.
            Encoders are referenced by index from 0 to n corresponding
            to the motors.
            Returns the encoder count for the specified motor.
        """
        capture = self.readEncoder(motorIndex)
            
        return capture.count
    
    def readEncoder(self, motorIndex: int):
        if motorIndex == 0:
            capture = self.enc1.capture()
        elif motorIndex == 1:
            capture = self.enc2.capture()
            
        return capture

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
        return 0

    def getRobotName(self) -> str:
        """
            Returns the name of the robot or hardware
        """
        return "Triangle Tracks"
        
    def getLEDCount(self) -> int:
        """
            Returns the LED count of the robot
        """
        return NUM_LEDS
    
    def setLEDColor(self, ledIdx: int, red: int, green, blue: int):
        """
            Set the colour of an RGB LED on the robot
        """
        self.board.leds.set_rgb(ledIdx, red, green, blue)

    def showLEDs(self):
        """
            Update all LEDs with their programmed colours
        """
        self.board.leds.show()
        
    def setAllLEDsColor(self, red: int, green: int, blue: int):
        """
            Set the colour of all RGB LEDs on the robot
        """
        for i in range(NUM_LEDS):
            self.board.leds.set_rgb(i, red, green, blue)
        self.showLEDs()
    
    def setLEDsAllOff(self):
        """
            Set the colour of all RGB LEDs on the robot
        """
        self.board.leds.clear()
        