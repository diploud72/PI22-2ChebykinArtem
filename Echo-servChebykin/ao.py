import socket
import threading

class ChatClient:
    def init(self):
        self.host = input("Введите IP адрес сервера: ")
        self.port = int(input("Введите порт сервера: "))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = input("Введите ваше имя: ")

    def send_message(self):
        try:
            while True:
                message = input("")
                self.client_socket.sendall(f"{self.username}: {message}".encode())
        except KeyboardInterrupt:
            self.client_socket.close()

    def receive_messages(self):
        try:
            while True:
                message = self.client_socket.recv(1024).decode()
                print(message)
        except KeyboardInterrupt:
            self.client_socket.close()

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            send_thread = threading.Thread(target=self.send_message)
            receive_thread = threading.Thread(target=self.receive_messages)
            send_thread.start()
            receive_thread.start()
        except ConnectionRefusedError:
            print("Не удалось подключиться к серверу.")
            self.client_socket.close()

if name == "main":
    client = ChatClient()
    client.connect()