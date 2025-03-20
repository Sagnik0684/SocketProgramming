import socket
import threading

server_ip = '127.0.0.1'
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)

print(f"Server listening on {server_ip}:{server_port}...")

clients = {}  # Stores {client_socket: client_id}
client_counter = 1  # Assigns unique serial numbers

def handle_client(client_socket, client_address):
    global client_counter
    client_id = client_counter
    clients[client_socket] = client_id
    client_counter += 1
    
    print(f"New Client #{client_id} connected from {client_address}")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Client #{client_id}: {message}")

            # Send confirmation to the sender
            client_socket.send(f"Message received by server (Client #{client_id})".encode())

            # Broadcast message to all clients except sender
            for client in clients:
                if client != client_socket:
                    client.send(f"Client #{client_id}: {message}".encode())
        except:
            break

    print(f"Client #{client_id} disconnected.")
    del clients[client_socket]
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()