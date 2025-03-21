import socket
import threading

server_ip = '127.0.0.1'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Function to receive messages
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            # Only print received messages, not user input
            print(message)
        except:
            break

# Start receiving messages in a separate thread
threading.Thread(target=receive_messages, daemon=True).start()

while True:
    message = input()  
    if message.lower() == "exit":
        break
    client_socket.send(message.encode())

client_socket.close()