# Multi-Client Chat Application (C++ & Python)

This repository contains a multi-client chat application implemented in both **C++** and **Python**, supporting client-server communication using sockets.

## Features
- Supports multiple clients connected to a single server.
- Clients can send and receive messages independently.
- Cross-platform support (Windows & macOS).
- Logging for chat history.
- Future enhancements: Encryption, user registration.

---

## 🚀 Getting Started

### 1. Clone the Repository
```sh
git clone https://github.com/Sagnik0684/SocketProgramming.git
cd multi-client-chat


## 🔧 Setup Instructions

### C++ Implementation

#### **Windows**
```sh
# Install MinGW for g++
choco install mingw

# Compile the server and client
g++ server.cpp -o server.exe -lws2_32
g++ client.cpp -o client.exe -lws2_32

# Run the server
./server.exe

# Run multiple clients
./client.exe

#### **Mac**
# Install necessary compiler
brew install gcc

# Compile the server and client
g++ server.cpp -o server
g++ client.cpp -o client

g++ server.cpp -o server -std=c++20 -pthread
g++ client.cpp -o client -std=c++20 -pthread

# Run the server
./server

# Run multiple clients
./client

# Ensure Python is installed (use python3 for macOS)
python --version  # Check if Python is installed

# Run the server
python server.py

# Run multiple clients
python client.py