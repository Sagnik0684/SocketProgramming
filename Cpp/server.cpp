#include <iostream>
#include <string>
#include <vector>
#include <unistd.h>     // For close()
#include <arpa/inet.h>  // For socket functions
#include <sys/socket.h>
#include <sys/select.h> // For select()

#define PORT 12345
#define MAX_CLIENTS 10

using namespace std;

vector<int> clients; // Stores all connected client sockets

// Function to broadcast a message to all clients except sender
void broadcastMessage(string message, int sender_fd) {
    for (int client_fd : clients) {
        if (client_fd != sender_fd) {
            send(client_fd, message.c_str(), message.length(), 0);
        }
    }
}

int main() {
    int server_fd, new_client;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_size = sizeof(client_addr);

    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        cerr << "Error creating socket\n";
        return -1;
    }

    // Set up server address struct
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    // Allow reuse of the port
    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        cerr << "setsockopt failed\n";
        return -1;
    }
    // Bind socket to port
    if (::bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        cerr << "Binding failed\n";
        return -1;
    }

    // Start listening for connections
    if (listen(server_fd, MAX_CLIENTS) < 0) {
        cerr << "Error listening\n";
        return -1;
    }

    cout << "Server listening on port " << PORT << "...\n";

    fd_set read_fds;
    int max_sd;

    while (true) {
        FD_ZERO(&read_fds);
        FD_SET(server_fd, &read_fds);
        max_sd = server_fd;

        // Add all clients to read_fds
        for (int client_fd : clients) {
            FD_SET(client_fd, &read_fds);
            if (client_fd > max_sd) max_sd = client_fd;
        }

        // Wait for activity
        int activity = select(max_sd + 1, &read_fds, NULL, NULL, NULL);
        if (activity < 0) {
            cerr << "Select error\n";
            continue;
        }

        // Check for new client connection
        if (FD_ISSET(server_fd, &read_fds)) {
            new_client = accept(server_fd, (struct sockaddr*)&client_addr, &addr_size);
            if (new_client < 0) {
                cerr << "Client accept failed\n";
                continue;
            }

            cout << "New client connected: " << new_client << endl;
            clients.push_back(new_client);
        }

        // Check for messages from clients
        for (auto it = clients.begin(); it != clients.end(); ) {
            int client_fd = *it;

            if (FD_ISSET(client_fd, &read_fds)) {
                char buffer[1024] = {0};
                int bytes_received = recv(client_fd, buffer, 1024, 0);

                if (bytes_received <= 0) {
                    // Client disconnected
                    cout << "Client " << client_fd << " disconnected\n";
                    close(client_fd);
                    it = clients.erase(it);
                } else {
                    string message = "Client " + to_string(client_fd) + ": " + string(buffer);
                    cout << message << endl;
                    broadcastMessage(message, client_fd);
                    ++it;
                }
            } else {
                ++it;
            }
        }
    }

    close(server_fd);
    return 0;
}