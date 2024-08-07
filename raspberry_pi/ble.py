import bluetooth
import time

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
        data = "Hello from Raspberry Pi"
        client_socket.send(data.encode())
        print("Sent:", data)
        time.sleep(1)  # Wait for 1 second before sending the next message
    except KeyboardInterrupt:
        break

# Close the client socket
client_socket.close()

# Close the server socket
server_socket.close()

