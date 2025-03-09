#include <iostream>
#include <string>
#include <thread>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 12345
#define SERVER_IP "127.0.0.1"

using namespace std;

// Function to receive messages
void receiveMessages(int client_fd) {
    char buffer[1024];
    while (true) {
        int bytes_received = recv(client_fd, buffer, 1024, 0);
        if (bytes_received <= 0) {
            cout << "Disconnected from server.\n";
            break;
        }
        cout << string(buffer, bytes_received) << endl;
    }
}

int main() {
    int client_fd;
    struct sockaddr_in server_addr;

    // Create socket
    client_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (client_fd == -1) {
        cerr << "Socket creation failed\n";
        return -1;
    }

    // Set up server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    // Connect to server
    if (connect(client_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        cerr << "Connection failed\n";
        return -1;
    }

    cout << "Connected to server!\n";

    // Start receiving messages in a new thread
    thread receiver([&]() { receiveMessages(client_fd); });
    receiver.detach();  // Runs independently

    // Send messages
    string message;
    while (true) {
        getline(cin, message);
        if (message == "exit") break;
        send(client_fd, message.c_str(), message.length(), 0);
    }

    close(client_fd);
    return 0;
}