import socket  # Import socket library

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define server details
server_ip = '127.0.0.1'  # Server IP (localhost for testing)
server_port = 12345       # Same port as server

# Connect to the server
client_socket.connect((server_ip, server_port))

# Send message to the server
client_socket.send("Hello, Server!".encode())

# Receive response from the server
response = client_socket.recv(1024).decode()
print(f"Server: {response}")

# Close the socket
client_socket.close()