import bluetooth
import threading

class RaspberryPiBluetoothServer:
    def __init__(self):
        self.server_sock = None
        self.client_sock = None
        self.client_info = None

    def start_server(self):
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)

        port = self.server_sock.getsockname()[1]

        print("Waiting for connection on RFCOMM channel", port)

        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from", self.client_info)

    def receive_message(self):
        while True:
            data = self.client_sock.recv(1024)
            if not data:
                break
            print("Received message:", data.decode("utf-8"))

        print("Connection closed")
        self.client_sock.close()

    def send_message(self):
        while True:
            message = input("Enter message to send (or 'q' to quit): ")
            if message == 'q':
                break
            self.client_sock.send(message.encode("utf-8"))

        print("Connection closed")
        self.client_sock.close()

    def close(self):
        if self.client_sock:
            self.client_sock.close()
        if self.server_sock:
            self.server_sock.close()

if __name__ == "__main__":
    bluetooth_server = RaspberryPiBluetoothServer()

    # Start the server
    bluetooth_server.start_server()

    # Start receiving and sending messages in separate threads
    receive_thread = threading.Thread(target=bluetooth_server.receive_message)
    receive_thread.start()

    send_thread = threading.Thread(target=bluetooth_server.send_message)
    send_thread.start()

    # Wait for both threads to finish
    receive_thread.join()
    send_thread.join()

    # Close the connection
    bluetooth_server.close()
