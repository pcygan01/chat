from threading import Thread
import socket
import select
host = "localhost"
port = 65432


def receive(tcp_socket, udp_socket):
    # print("receive sie wywoluje")
    while True:
        readable, _, _ = select.select([tcp_socket, udp_socket], [], [])
        for socket in readable:

            if socket == tcp_socket:
                data = tcp_socket.recv(1024)
                if not data:
                    continue
                print(data.decode("utf-8"))
            elif socket == udp_socket:
                data, _ = udp_socket.recvfrom(1024)
                if not data:
                    continue
                print(data.decode("utf-8"))

if __name__ == '__main__':
    nick = input("Choose nickname: ")
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((host, port))
    tcp_socket.send(bytes(f"{nick} joined the chat!", 'utf-8'))
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, tcp_socket.getsockname()[1]))
    Thread(target=receive, args=(tcp_socket, udp_socket), daemon=True).start()
    while True:
        udp = False
        text = input()
        if not text:
            continue
        if text == "U":
            print("Your next message will be sent by UDP:")
            text = input()
            udp = True
        if text in ('q', 'quit', 'disconnect') and not udp:
            tcp_socket.send(bytes(f"{nick} has left the chat!", "utf-8"))
            tcp_socket.send(bytes(text, 'utf-8'))
            tcp_socket.close()
            raise SystemExit

        text = f"{nick}: " + text
        if udp:
            udp_socket.sendto(bytes(text, 'utf-8'), (host, port))
        else:
            tcp_socket.send(bytes(text, 'utf-8'))
        # data = tcp_socket.recv(1024)
        # print("received: " + data.decode("utf-8"))