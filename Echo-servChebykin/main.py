import socket
import threading

class ChatServer:
    def init(self):
        self.host = "0.0.0.0"
        self.port = 9999
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("[+] Сервер запущен и ожидает подключений.")

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                message = client_socket.recv(1024).decode().strip()
                if not message:
                    break
                print(f"[{client_address[0]}:{client_address[1]}] {message}")
                self.broadcast(message, client_socket)
        except ConnectionResetError:
            pass
        finally:
            self.remove_client(client_socket)

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.sendall(message.encode())
                except BrokenPipeError:
                    self.remove_client(client)

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            client_socket.close()

    def start(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"[+] Подключился новый клиент: {client_address[0]}:{client_address[1]}")
                self.clients.append(client_socket)
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
        except KeyboardInterrupt:
            print("[+] Остановка сервера.")
            self.server_socket.close()

if name == "main":
    server = ChatServer()
    server.start()