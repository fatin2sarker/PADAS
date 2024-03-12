import bluetooth
import RPi.GPIO as GPIO
import time

def main():
# Create a Bluetooth RFCOMM server socket
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 3
    server_socket.bind(("", port))
    server_socket.listen(1)

    print("Waiting for connection...")
    client_socket, address = server_socket.accept()
    print("Accepted connection from", address)

# Set up GPIO Pin 11
    GPIO.setmode(GPIO.BCM)
    pin = 17
    GPIO.setup(pin, GPIO.IN)
    prev_state = GPIO.input(pin)

    try:
        while True:
            # Read the current state of the pin
            current_state = GPIO.input(pin)
        
            # Check if the state has changed
            if current_state != prev_state:
                data = "Check Blindspot"
                client_socket.send(data.encode())
                print("Sent:", data)
                time.sleep(1)

            # Update the previous state
            #prev_state = current_state
        
            # Delay for a short time to avoid busy waiting
            #time.sleep(0.1)

    except KeyboardInterrupt:
        # Close the client socket
        client_socket.close()
        # Close the server socket
        server_socket.close()
        GPIO.cleanup()  # Clean up GPIO on exit
        
      

if __name__ == "__main__":
    main()
