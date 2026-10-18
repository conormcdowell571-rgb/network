import threading
import socket
#Set the port and socket for the server
host = "127.0.0.1"
port = 56789
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients  = []
names = []

#When a client sends a message to the server, broadcast it to everyone
def broadcast(message):
    for client in clients:
        client.send(message)

#Call the broadcast function if a message is sent
def handle_client(client):
    while True:
        try: 
            message = client.recv(1024)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f"{name} has left".encode("utf-8"))
            names.remove(name)
            break

#Run the server and send status updates
def receive():
    while True:
        print("Server is running and listening")
        client, address = server.accept()
        print(f"Connection established with {str(address)}")
        client.send("name?".encode("utf-8"))
        name = client.recv(1024)
        names.append(name)
        clients.append(client)
        print(f"The name of this client is {name}".encode("utf-8"))
        broadcast(f"{name} has connected\n".encode("utf-8"))
        client.send("You are connected".encode("utf-8"))
        thread = threading.Thread(target = handle_client, args = (client,))
        thread.start()

if __name__ == "__main__":
    receive()