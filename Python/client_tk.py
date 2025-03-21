import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Server details
server_ip = "127.0.0.1"
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
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, message + "\n")
            chat_box.config(state=tk.DISABLED)
            chat_box.yview(tk.END)
        except:
            break

# Function to send messages
def send_message(event=None):  # ✅ Add 'event' parameter to handle Enter key
    message = message_entry.get()
    if message:
        client_socket.send(message.encode())
        message_entry.delete(0, tk.END)  # Clear input field

# Create the Tkinter UI
root = tk.Tk()
root.title("Chat Client")

# Chat display area
chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=50, height=20)
chat_box.pack(padx=10, pady=10)

# Message input field
message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5, side=tk.LEFT)
message_entry.bind("<Return>", send_message)  # ✅ Press Enter to send message

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=5, side=tk.RIGHT)

# Start receiving messages in a separate thread
threading.Thread(target=receive_messages, daemon=True).start()

# Run the Tkinter event loop
root.mainloop()

# Close socket when UI is closed
client_socket.close()