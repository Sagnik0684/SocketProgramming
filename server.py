import socket  # Import socket library

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define server details
server_ip = '127.0.0.1'  # Localhost
server_port = 12345       # Port number

# Bind the socket to the address and port
server_socket.bind((server_ip, server_port))

# Start listening for connections (max 1 client in queue)
server_socket.listen(1)
print(f"Server listening on {server_ip}:{server_port}...")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Receive data from the client
message = client_socket.recv(1024).decode()
print(f"Client: {message}")

# Send response to the client
client_socket.send("Hello, Client! Connection Successful.".encode())

# Close connections
client_socket.close()
server_socket.close()