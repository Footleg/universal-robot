# Simple test program for the robot interface using an Inventor HAT Mini
from time import sleep
from RobotHardware_InventorHATmini import Robot

battPowerColour = (0,255,255) # This will get updated to colour indicating battery level
def showBatteryStatus(v=0):
    global battPowerColour

    # Set min and max voltage range for colours (min will be shown as red, max as green)
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

# Create robot hardware instance
robot = Robot()

print(f"Robot Name: {robot.getRobotName()}" )

# Get battery voltage and set a colour for LEDs based on this
showBatteryStatus()

# Report encoders positions
print(f"Encoders A: {robot.getEncoderCount(0)}; B: {robot.getEncoderCount(1)};")

# Start motor A
robot.setMotorPower(0,100)
for i in range(12):
    sleep(0.25)
    print(f"Encoders A: {robot.getEncoderCount(0)}; B: {robot.getEncoderCount(1)};")

# Stop motor A and start motor B in reverse
robot.setMotorsPower(0,-100)
for i in range(12):
    sleep(0.25)
    print(f"Encoders A: {robot.getEncoderCount(0)}; B: {robot.getEncoderCount(1)};")
# Drop motor B to half speed
robot.setMotorPower(1,-50)
print(f"Encoders A: {robot.getEncoderCount(0)}; B: {robot.getEncoderCount(1)};")
sleep(3)
# Stop both motors
robot.setMotorsPower(0,0)
print(f"Encoders A: {robot.getEncoderCount(0)}; B: {robot.getEncoderCount(1)};")

# LED show (3 LED long Larson scanner bar)
ledPos = 0 #Position of LED scanning cursor used for animation
ledDir = 1 #Direction LED scanning cursor is moving
led1 = 2 #Brightness multiple for LED 1
led2 = 1 #Brightness multiple for LED 2
led3 = 0.5 #Brightness multiple for LED 3
ledUpdateInterval = 0
ledColour = battPowerColour

for i in range(100):
    #Update LED animation
    ledUpdateInterval += 1
    if ledUpdateInterval > 1:
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

    #print(f"LED pos: {ledPos}")
    sleep(0.01)


robot.shutdownHardware()
