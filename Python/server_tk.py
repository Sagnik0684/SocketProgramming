import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Server details
server_ip = "127.0.0.1"
server_port = 12345

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)

clients = {}  # Store connected clients
client_counter = 1  # Assigns unique client IDs

# Function to broadcast messages to all clients
def broadcast_message(message, sender_socket=None):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, message + "\n")
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

    for client in clients:
        if client != sender_socket:
            client.send(message.encode())

# Function to handle each client
def handle_client(client_socket, client_address):
    global client_counter
    client_id = client_counter
    clients[client_socket] = client_id
    client_counter += 1

    welcome_message = f"Client #{client_id} connected from {client_address}"
    broadcast_message(welcome_message)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            formatted_message = f"Client #{client_id}: {message}"
            broadcast_message(formatted_message)
        except:
            break

    disconnect_message = f"Client #{client_id} disconnected."
    broadcast_message(disconnect_message)
    del clients[client_socket]
    client_socket.close()

# Function to accept clients
def accept_clients():
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

# Create the Tkinter UI
root = tk.Tk()
root.title("Server Chat Log")

chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=50, height=20)
chat_box.pack(padx=10, pady=10)

# Start the server thread
threading.Thread(target=accept_clients, daemon=True).start()

# Run the Tkinter event loop
root.mainloop()

# Close server socket when GUI is closed
server_socket.close()