from adafruit_servokit import ServoKit
import time

# Setup the ServoKit class.
kit = ServoKit(channels=16)

# Define function for stopping motor
def motor_stop():
    kit.continuous_servo[7].throttle = 0.0 #7
    print("stop")

# Define function for moving motor forward
def motor_forward(throttle_value):
    kit.continuous_servo[7].throttle = throttle_value #7
    print("forward")

# Define function for moving motor backward
# muss 2 mal ausgeführt werden, beim ersten mal stop motor, beim zweiten mal fährt rückwärts
def motor_backward(throttle_value):
    kit.continuous_servo[7].throttle = -throttle_value #7
    print("Backward")

# Main function
if __name__ == '__main__':
    while True:
        try:
            command = input("Enter command (f, b, s): ")
            if command == 'f':
                throttle_value = float(input("Enter throttle value between -1.0 and 1.0: "))
                motor_forward(throttle_value)
            elif command == 'b':
                throttle_value = float(input("Enter throttle value between -1.0 and 1.0: "))
                motor_backward(throttle_value)
            elif command == 's':
                motor_stop()
            else:
                print("Unknown command")
        except KeyboardInterrupt:
            print('Motor gestoppt')
            break
