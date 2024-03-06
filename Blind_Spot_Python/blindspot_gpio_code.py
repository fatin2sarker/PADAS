import RPi.GPIO as GPIO
import time

def main():
    # Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set the pin number you want to monitor
pin = 17

# Set the pin as input
GPIO.setup(pin, GPIO.IN)

# Initial state of the pin
prev_state = GPIO.input(pin)

try:
    while True:
        # Read the current state of the pin
        current_state = GPIO.input(pin)
        
        # Check if the state has changed
        if current_state != prev_state:
            print("check blindspot!")

        # Update the previous state
        prev_state = current_state
        
        # Delay for a short time to avoid busy waiting
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on exit

if __name__ == "__main__":
    main()
