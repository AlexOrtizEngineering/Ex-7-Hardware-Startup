#      ******************************************************************
#      *                                                                *
#      *   This program demonstrates how to use the DPiStepper Board    *
#      *                                                                *
#      *            Stan Reifel                     8/21/2022           *
#      *                                                                *
#      * This has been modified from the original DPiStepper_Example.py *
#      *  to make it easier to run in an ipython3 console so that       *
#      *  students can execute the code one line at a time and observe  *
#      *  the behavior of the stepper motors                            *
#      *                                                                *
#      *  Lyle Harlow 01/04/2023                                        *
#      *                                                                *
#      ******************************************************************


from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import *
from time import sleep

#
# create the DPiStepper object, one object should be created for each DPiStepper
# board that you are using.
#
dpiStepper = DPiStepper()

#
# Up to 4 DPiStepper boards can be connected together  Each board is addressed
# (0 - 3) by configuring its jumpers.  If no jumpers are installed, the board number
# is 0.  Note: After changing the jumpers, the board must be power-cycled.
#

#
# In this example, we will be using board number 0.
#
dpiStepper.setBoardNumber(0)

#
# Most DPi library functions return True if the function executes successfully or
# False if it fails.  It's best practice to check the return value of every library
# call to verify success.  Often however, checking every call is a pain.  At a
# minimum, a program should always check the first call made to the library to insure
# the connection to the board is working.
#
# There are many reasons that a function might fail:
#    + The DPi board is not powered.
#    + The board is not plugged into the DPiNetwork, or plugged in incorrectly.
#    + The network is not terminated properly.  Termination jumpers must be set on the
#      network's last board and none others.
#    + The board's LCD is displaying a menu, or menu command.  It is not at the home
#      screen.
#    + The "Board Number" is not set correctly.
#    + One or more of the arguments passed to the library function are out of range or
#      invalid.
#

#
# This is the first library call that communicates with board.  Be sure to check the
# return value insuring everything is working.
#
# Initialize the board to its default values.
#
if dpiStepper.initialize() != True:
    print("Communication with the DPiStepper board failed.")

#
# Enable the stepper motors, when disabled the motors are turned off and spin freely.
#
dpiStepper.enableMotors(True)

#
# Microstepping determines the number of steps per revolution of the motor.  The choices
# for microstepping are 1, 2, 4, 8, 16 or 32.  By choosing 1, the motor will require 200
# steps to make one full rotation. Choosing 2 will require 400 steps, choosing 8 will need
# 1600.  More steps gives you several advantages: 1) Greater angular resolution. 2) Runs
# smoother with less vibration.  3) Motors run more quietly.  The downside to large
# microstepping values is that the DPiStepper board has to work harder to generate more
# steps for the same amount of rotation. For most applications, choosing 8 or 16 works
# well. For applications when the motors spins fast (ie > 10 RPS), it may be advantages
# to use 8, 4 or 2.
#

#
# Set microstepping to 8X, resulting in 1600 steps per revolution of the motor's shaft.
#
microstepping = 8
dpiStepper.setMicrostepping(microstepping)

#
# Before making the motors move, you will want to set the motor's speed and rate of
# acceleration.  A good starting speed is one revolution/second. With 8X microstepping
# that is 1600 steps/second. Also, setting the acceleration to the same value as the speed
# often works well.
#

#
# Set the speed for motors 0 & 1 to one revolution per second.
#
speed_steps_per_second = 200 * microstepping
accel_steps_per_second_per_second = speed_steps_per_second
dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)
dpiStepper.setSpeedInStepsPerSecond(1, speed_steps_per_second)
dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)
dpiStepper.setAccelerationInStepsPerSecondPerSecond(1, accel_steps_per_second_per_second)

#
# It's now time to check the status of the motor:
# get stepper status
#  Enter:  stepperNum = stepper driver number (0 - 2)
#  Exit:   [0]: True returned on success, else False
#          [1]: True returned if motor is stopped
#          [2]: True returned if motors are enabled
#          [3]: True returned if the "Homing" switch indicates "At home"
#

stepperStatus = dpiStepper.getStepperStatus(0)
print(f"Pos = {stepperStatus}")

#
# It's now time to move a motor: rotate stepper 0, one full revolution, wait until the motor stops.
#

stepper_num = 0
steps = 1600
wait_to_finish_moving_flg = True
dpiStepper.moveToRelativePositionInSteps(stepper_num, steps, wait_to_finish_moving_flg)

#
# It's now time to home the motor: Move the stepper until the home sensor is activated so the computer knows where in its rotation the motor is
#
#
# home the motor by moving until the homing sensor is activated, then set the
# position to zero with units in steps
#  Enter:  stepperNum = stepper driver number (0 - 2)
#          directionTowardHome = 1 to move in a positive direction, -1 to move in
#            a negative directions
#          speedInStepsPerSecond = speed to accelerate up to while moving toward
#            home, units in steps/second
#          maxDistanceToMoveInSteps = unsigned maximum distance to move toward
#            home before giving up
#  Exit:   True returned if successful, else False
#

directionToMoveTowardHome = 1 # 1 Positive Direction -1 Negative Direction
homeSpeedInStepsPerSecond = speed_steps_per_second / 2
homeMaxDistanceToMoveInSteps = 3200

dpiStepper.moveToHomeInSteps(stepper_num, directionToMoveTowardHome, homeSpeedInStepsPerSecond,homeMaxDistanceToMoveInSteps)

#
# Start stepper 0 rotating one turn CW, and stepper 1 rotating two turns CCW.
#
steps_per_rotation = 1600
wait_to_finish_moving_flg = False
dpiStepper.moveToRelativePositionInSteps(0, 1 * steps_per_rotation, wait_to_finish_moving_flg)
dpiStepper.moveToRelativePositionInSteps(1, -2 * steps_per_rotation, wait_to_finish_moving_flg)

#
# now wait for both motors to stop
#
while dpiStepper.getAllMotorsStopped() == False:
    sleep(0.02)

sleep(2)

#
# When you issue a "Move" command, you can tell the motor to start counting steps from its
# current position. That's a "Relative" move.  It will move the exact number of steps given,
# to a new coordinate that is relative to where the move started from.
#
# You can also issue a "Move" command using a coordinate system that is referenced to a fixed
# location. These are "Absolute" moves.  For example, when you begin, the motor will be at
# position 0.  If you issue an AbsoluteMove to 100, it will move 100 steps to coordinate
# 100. Now if you issue a command to move to 200, it will move 100 more steps, stopping at
# coordinate 200. Finally sending a move to 0 will cause the motor to rotate backwards 200
# steps, returning to coordinate 0.
#

#
# In the examples above, we used "Relative" moves.  Here we will move using "Absolute"
# coordinates instead.  Start by setting stepper 0 to coordinate 0.
#
stepper_num = 0
dpiStepper.setCurrentPositionInSteps(stepper_num, 0)

#
# Move one rotation to coordinate 1600, then another rotation to 3200, finally back 2 turns to coord 0
#
wait_to_finish_moving_flg = True
dpiStepper.moveToAbsolutePositionInSteps(stepper_num, 1600, wait_to_finish_moving_flg)
dpiStepper.moveToAbsolutePositionInSteps(stepper_num, 3200, wait_to_finish_moving_flg)
dpiStepper.moveToAbsolutePositionInSteps(stepper_num, 0, wait_to_finish_moving_flg)

#
# For fun, let's ask the motor where it is, it should be back to coordinate 0.
#
currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
print(f"Pos = {currentPosition}")

#
# In all the examples above, we used units of "Steps" to tell the motor how far and how
# fast to go. Frequently issuing motion commands in Steps isn't very intuitive. The
# DPiStepper library includes 3 different units of distance that you can use to control
# the motors: (steps, millimeters and revolutions). Choose the one that's most intuitive
# for your application. If your mechanism is linear, choose Millimeters.  If its
# rotational, choose Revolutions.
#

#
# Now we are programming a linear mechanism so this example will use units in Millimeters.
# The first thing to do is tell the library now many steps it takes to move 1mm.
#
stepper_num = 0
dpiStepper.setStepsPerMillimeter(stepper_num, 64)

#
# Set the motors speed and rate of acceleration.
#
speed_in_mm_per_sec = 100
accel_in_mm_per_sec_per_sec = 100
dpiStepper.setSpeedInMillimetersPerSecond(stepper_num, speed_in_mm_per_sec)
dpiStepper.setAccelerationInMillimetersPerSecondPerSecond(stepper_num, accel_in_mm_per_sec_per_sec)

#
# Do a move 100 millimeters backwards from the motor's current position
#
dpiStepper.moveToRelativePositionInMillimeters(stepper_num, -100, True)

#
# In the following example we are assuming the stepper motor is now driving a rotating
# table with a 1:1 gear reduction between the table and the motor.  In this case it
# makes most sense to have our code use units of the "Table's rotation". Start by
# specifing the number of steps it takes to make the table go around once.
#
stepper_num = 0
gear_ratio = 1
motorStepPerRevolution = 1600 * gear_ratio
dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)

#
# Set the speed so the table goes all the way around in 2 seconds
#
speed_in_revolutions_per_sec = 2.0
accel_in_revolutions_per_sec_per_sec = 2.0
dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)

#
# To begin with, tell the library the table is at 0.0, which is the 12 0'clock position
#
dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

#
# Now let's move the motor to move 4 times, a quarter turn each, using absolute coodinates to
# the 3 o'clock, 6 o'clock, 9 o'clock and 12 o'clock positions
#
waitToFinishFlg = True
dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0.25, waitToFinishFlg)
sleep(1)
dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0.5, waitToFinishFlg)
sleep(1)
dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0.75, waitToFinishFlg)
sleep(1)
dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 1.0, waitToFinishFlg)
sleep(1)

#
# all done now, disable the motors
#
dpiStepper.enableMotors(False)

#
# Here is another way to verify communication with the board is work. "Ping" it.
#
if dpiStepper.ping() != True:
    print("Communication with the DPiStepper board failed.")

#
# This command can be useful for diagnostic purposes, it gets the number of times a command
# was sent to the board, but the communication failed.  If communication fails, the DPi
# library adds one to the error count, then automatically resends the command.  If that
# fails 3 times in a row, the function gives up and returns "False".
#
comm_errors = dpiStepper.getCommErrorCount()
print(f"Communication errors count = {comm_errors}")


#
# There are more commands in the library.  Check its source code to learn more.  The source code is DPiStepper.py
# Here are some of the additional commands:
#
#    waitUntilMotorStops(stepperNum)
#    getMotionComplete(stepperNum)
#    getCurrentPositionInSteps(stepperNum)
#    getCurrentVelocityInStepsPerSecond(stepperNum)
#    decelerateToAStop(stepperNum)
#    emergencyStop(stepperNum)
#    getCurrentPositionInMillimeters(stepperNum)
#    getCurrentVelocityInMillimetersPerSecond(stepperNum)
#    moveToHomeInMillimeters(stepperNum, directionTowardHome, speedInMillimetersPerSecond, maxDistanceToMoveInMillimeters)
#    getCurrentPositionInRevolutions(stepperNum)
#    getCurrentVelocityInRevolutionsPerSecond(stepperNum)
#    moveToHomeInRevolutions(stepperNum, directionTowardHome, speedInRevolutionsPerSecond, maxDistanceToMoveInRevolutions)
#
