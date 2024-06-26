import RPi.GPIO as GPIO
import bluetooth
import time

def main():
    # Set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Set the pin number you want to monitor
    pin = 17

    # Set the pin as input
    GPIO.setup(pin, GPIO.IN)

    # Initial state of the pin
    GPIO.input(pin)

    try:
        # Create a Bluetooth server socket
        server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        # Bluetooth port number
        port = 1

        # Bind the server socket to any available port
        server_socket.bind(("", port))

        # Listen for incoming connections (maximum 1 client)
        server_socket.listen(1)

        print("Waiting for connection...")

        # Accept incoming connection
        client_socket, address = server_socket.accept()
        print("Accepted connection from", address)

        # Send data over Bluetooth
        while True:
            try:
                # Read the current state of the pin
                current_state = GPIO.input(pin)
                
                # Check if the state has changed
                 if current_state == GPIO.HIGH:
                    print("Check blind spot!")
                    # Send "Check blind spot" to the client
                    client_socket.send("Check blind spot".encode())
                else:
                    print("All clear!")
                    # Send "All clear" to the client
                    client_socket.send("All clear".encode())
                
                # Receive data from the client
                received_data = client_socket.recv(1024).decode().strip()
                    
                time.sleep(0.1)  # Delay for a short time to avoid busy waiting

            except KeyboardInterrupt:
                break

        # Close the client socket
        client_socket.close()

        # Close the server socket
        server_socket.close()

    finally:
        GPIO.cleanup()  # Clean up GPIO on exit

if __name__ == "__main__":
    main()
