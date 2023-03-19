from threading import Thread
import socket
host = "127.0.0.1"
port = 65432

clients = {}

def receive_from_client(tcp_client_socket, client_address):
    print(f"Connected by {client_address}")
    # ip, port = client_address
    clients[client_address] = tcp_client_socket
    while True:
        data = tcp_client_socket.recv(1024)
        if not data:
            continue
        if data.decode("utf-8") in ('q', 'quit', 'disconnect'):
            clients.pop(client_address)
            tcp_client_socket.close()
            print(f"Client {client_address} has disconnected")
            if len(clients) == 0:
                print("Everyone has disconnected")
                raise SystemExit
            break
        for other_client_address, other_client_socket in clients.items():
            if other_client_socket != tcp_client_socket:
                other_client_socket.send(data)
                print(f"sent data from {client_address} to: {other_client_address} by TCP")

def receive_udp(udp_server_socket):
    while True:
        data, udp_client_address = udp_server_socket.recvfrom(1024)
        if not data:
            continue

        for other_client_address, other_client_socket in clients.items():
            if other_client_address != udp_client_address:
                udp_server_socket.sendto(data, other_client_address)
                print(f"sent data from {client_address} to: {other_client_address} by UDP")

if __name__ == '__main__':
    print("Server started!")
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind((host, port))
    tcp_server_socket.listen()
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind((host, port))
    Thread(target = receive_udp, args=(udp_server_socket,), daemon=True).start()
    while True:
        tcp_client_socket, client_address = tcp_server_socket.accept()
        Thread(target= receive_from_client, args=(tcp_client_socket, client_address), daemon=True).start()
