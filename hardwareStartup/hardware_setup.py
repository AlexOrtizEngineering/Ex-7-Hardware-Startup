import os
os.environ['DISPLAY'] = ":0.0"

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton

from kivy.animation import Animation
from kivy.clock import Clock

from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import *
from time import sleep

from datetime import datetime
time = datetime

# Set up the screens
SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
NEW_SCREEN_NAME = 'new'

# Global motor variables
motor_flag = False
motor_direction = 1
motor_speed = 200

# Class to handle running the GUI Application
class ProjectNameGUI(App):
    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER

# Set the window color to white
Window.clearcolor = (1, 1, 1, 1)

# Define motor and motor board
dpiStepper = DPiStepper()
dpiStepper.setBoardNumber(0)
stepper_num = 0
if not dpiStepper.initialize():
    print("Communication with the DPiStepper board failed.")

# Class to handle the main screen and its associated touch events
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def on_enter(self):
        if not motor_flag:
            self.motor_button.text = "Stepper motor disabled"
            self.motor_button.color = (1, 0, 0, 1)
        else:
            print("Error disabling motors")

    def turn_on_and_off(self):
        global motor_flag

        ref = self.motor_button.text
        if ref == "Stepper motor disabled":
            self.motor_button.text = "Stepper motor enabled"
            self.motor_button.color = (0, 1, 0, 1)
            motor_flag = True
        elif ref == "Stepper motor enabled":
            self.motor_button.text = "Stepper motor disabled"
            self.motor_button.color = (1, 0, 0, 1)
            motor_flag = False
        else:
            print("Error updating button")

    def update_motor_direction(self):
        global motor_direction

        if motor_direction == 1:
            motor_direction = -1
            self.update_direction.text = "Motor direction: counter-clockwise"
            self.update_direction.color = (1, 1, 0, 1)
        elif motor_direction == -1:
            motor_direction = 1
            self.update_direction.text = "Motor direction: clockwise"
            self.update_direction.color = (0, 1, 1, 1)
        else:
            print("Error updating motor direction")

    def update_motor_speed(self, slider, value):
        global motor_speed
        self.slider_value_label.text = f'Motor speed: {int(value)}'
        motor_speed = int(value)

    def get_status(self):
        """
                [0]: True returned on success, else False
                [1]: True returned if motor is stopped
                [2]: True returned if motors are enabled
                [3]: True returned if the "Homing" switch indicates "At home"
        """
        stepperStatus = dpiStepper.getStepperStatus(0)
        print(f"Pos = {stepperStatus}")

    def special_event(self):
        if motor_flag:
            SCREEN_MANAGER.current = 'new'

# Function to run motor
def run_motor():
    microstepping = 8
    dpiStepper.setMicrostepping(microstepping)

    speed_steps_per_second = motor_speed * microstepping
    accel_steps_per_second_per_second = speed_steps_per_second
    dpiStepper.setSpeedInStepsPerSecond(stepper_num, speed_steps_per_second)
    dpiStepper.setAccelerationInStepsPerSecondPerSecond(stepper_num, accel_steps_per_second_per_second)

    steps_per_rotation = 1600
    wait_to_finish_moving_flg = False
    dpiStepper.moveToRelativePositionInSteps(stepper_num, motor_direction  * steps_per_rotation, wait_to_finish_moving_flg)

# Constantly running to check motor status and enable or disable accordingly
def update_motor_movement(self):
    if not motor_flag:
        dpiStepper.enableMotors(False)
    elif motor_flag:
        dpiStepper.enableMotors(True)
        run_motor()

Clock.schedule_interval(update_motor_movement, 0.000001)

# Class to handle the new event screen
class NewScreen(Screen):
    def __init__(self, **kwargs):
        super(NewScreen, self).__init__(**kwargs)

    def on_enter(self): #TODO last three get_position_in_units aren't updating display anymore
        Clock.schedule_once(lambda dt: self.motor_fun(), 0.01)

    # def motor_fun(self):
    #     global motor_flag
    #
    #     # Waits for motor to stop
    #     while not dpiStepper.getAllMotorsStopped():
    #         sleep(0.02)
    #
    #     # Prints the value of get_position_in_units to a label on the kivy screen, which should be 0.0
    #     val, position = dpiStepper.getCurrentPositionInRevolutions(stepper_num)
    #     if position != 0.0:
    #         dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)
    #     self.get_position_in_units()
    #
    #     # 15 revolutions clockwise at 1 revolution / sec. Then prints the value of get_position_in_units to a label on the kivy screen
    #     self.move_rev_per_sec(1.0, 15.0)
    #     self.get_position_in_units()
    #
    #     # Stops 10 seconds then turns clockwise for 10 revolutions at 5 rev / sec.Then prints the value of get_position_in_units to a label on the kivy screen
    #     sleep(10)
    #     self.move_rev_per_sec(5.0, 10.0)
    #     self.get_position_in_units()
    #
    #     # Stops for 8 seconds. Then goes home and stops for 30 seconds.Then prints the value of get_position_in_units to a label on the kivy screen
    #     sleep(8)
    #     dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0.0, True)
    #     self.get_position_in_units()
    #
    #     # Then turns counter-clockwise for 100 revolutions at 8 rev / sec. Then prints the value of get_position_in_units to a label on the kivy screen
    #     sleep(1)
    #     self.move_rev_per_sec(8.0, -100.0)
    #     self.get_position_in_units()
    #
    #     # Then stops for 10 seconds and then goes home and Then prints the value of get_position_in_units to a label on the kivy screen
    #     sleep(10)
    #     dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0.0, True)
    #     self.get_position_in_units()
    #
    #     # Disable motors and go back to main screen
    #     self.disable_motors()
    #     # Clock.schedule_once(lambda dt: self.transition_back(), 0.01)

    def motor_fun(self):
        global motor_flag
        Clock.schedule_once(lambda dt: self.wait_for_motor(), 0.01)

    def wait_for_motor(self):
        while not dpiStepper.getAllMotorsStopped():
            sleep(0.02)

        val, position = dpiStepper.getCurrentPositionInRevolutions(stepper_num)
        if position != 0.0:
            dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)
        self.get_position_in_units()

        Clock.schedule_once(lambda dt: self.first_motor_fun(), 1)

    def first_motor_fun(self):
        self.move_rev_per_sec(1.0, 15.0)
        Clock.schedule_once(lambda dt: self.get_position_in_units(), 0.01)
        Clock.schedule_once(lambda dt: self.continue_motor_fun(), 10)

    def continue_motor_fun(self):
        self.move_rev_per_sec(5.0, 10.0)
        self.get_position_in_units()
        Clock.schedule_once(lambda dt: self.next_motor_fun(), 8)

    def next_motor_fun(self):
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, 5)
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0.0, True)
        self.get_position_in_units()
        Clock.schedule_once(lambda dt: self.next_next_motor_fun(), 1)

    def next_next_motor_fun(self):
        self.move_rev_per_sec(8.0, -100.0)
        self.get_position_in_units()
        Clock.schedule_once(lambda dt: self.final_motor_fun(), 10)

    def final_motor_fun(self):
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, 8)
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0.0, True)
        self.get_position_in_units()
        Clock.schedule_once(lambda dt: self.disable_motors(), 5)

    def get_position_in_units(self):
        val, position_in_units = dpiStepper.getCurrentPositionInRevolutions(stepper_num)
        print(position_in_units)
        self.rev_label.text = f'Current position: {position_in_units}'

    def move_rev_per_sec(self, ratio, revs):
        global motor_flag
        dpiStepper.setStepsPerRevolution(stepper_num, 1600)
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, ratio)
        dpiStepper.moveToRelativePositionInRevolutions(stepper_num, revs, True)

    def disable_motors(self):
        global motor_flag
        dpiStepper.enableMotors(False)
        motor_flag = False
        print("Motors disabled")

    def transition_back(self):
        SCREEN_MANAGER.current = 'main'

# Load the widgets
Builder.load_file('main.kv')
Builder.load_file('new.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(NewScreen(name=NEW_SCREEN_NAME))

# Runs the GUI Application
if __name__ == "__main__":
    ProjectNameGUI().run()


# # Motor initialization + stepping
# dpiStepper = DPiStepper()
# dpiStepper.setBoardNumber(0)


# # Checks that initialization did occur
# if dpiStepper.initialize() != True:
#     print("Communication with the DPiStepper board failed.")

# # Enables the stepper motors
# dpiStepper.enableMotors(True)

# Sets the increments of microstepping and applies that to the motors
# microstepping = 8
# dpiStepper.setMicrostepping(microstepping)
# speed_steps_per_second = 200 * microstepping
# accel_steps_per_second_per_second = speed_steps_per_second
# dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)
# dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)

# #Prints a list of statuses
# """
#         [0]: True returned on success, else False
#         [1]: True returned if motor is stopped
#         [2]: True returned if motors are enabled
#         [3]: True returned if the "Homing" switch indicates "At home"
# """
# stepperStatus = dpiStepper.getStepperStatus(0)
# print(f"Pos = {stepperStatus}")

# # Move the motor, wait until it's done
# stepper_num = 0
# steps = 1600
# wait_to_finish_moving_flg = True
# if not dpiStepper.moveToRelativePositionInSteps(stepper_num, steps, wait_to_finish_moving_flg):
#     print("Error")

# # Move the motor CW
# steps_per_rotation = 3200
# wait_to_finish_moving_flg = False
# dpiStepper.moveToRelativePositionInSteps(stepper_num, 1 * steps_per_rotation, wait_to_finish_moving_flg)

# Wait for motors to stop
# while dpiStepper.getAllMotorsStopped() == False:
#     sleep(0.02)
#
# sleep(2)


# # Move motor to coordinate 0
# dpiStepper.setCurrentPositionInSteps(stepper_num, 0)
#
# # Move the motor to coordinate 1600, 3200, then  back to
# wait_to_finish_moving_flg = True
# dpiStepper.moveToAbsolutePositionInSteps(stepper_num, 1600, wait_to_finish_moving_flg)
# dpiStepper.moveToAbsolutePositionInSteps(stepper_num, 3200, wait_to_finish_moving_flg)
# dpiStepper.moveToAbsolutePositionInSteps(stepper_num, 0, wait_to_finish_moving_flg)

# # Ask the motor where it's position is
# currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
# print(f"Pos = {currentPosition}")

# # Move the motor by revolutions instead of steps
# gear_ratio = 1
# motorStepPerRevolution = 1600 * gear_ratio
# dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)
# # set speed so it goes around in 2 seconds
# speed_in_revolutions_per_sec = 2.0
# accel_in_revolutions_per_sec_per_sec = 2.0
# dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
# dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)
# dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)
# waitToFinishFlg = True
# dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0.25, waitToFinishFlg)
# sleep(1)
# dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0.5, waitToFinishFlg)
# sleep(1)
# dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0.75, waitToFinishFlg)
# sleep(1)
# dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 1.0, waitToFinishFlg)
# sleep(1)

# # Disable motors
# dpiStepper.enableMotors(False)