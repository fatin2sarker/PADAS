import socket
import time

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Host and port for the server
host = ""  # Leave empty to accept connections from any address
port = 1

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections (maximum 1 client)
server_socket.listen(1)

print("Waiting for connection...")

# Accept incoming connection
client_socket, address = server_socket.accept()
print("Accepted connection from", address)

# Send data over the socket
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
