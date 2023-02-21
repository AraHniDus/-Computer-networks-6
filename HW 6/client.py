import socket
import random
from threading import Thread
from datetime import datetime

SERVER_HOST = "127.0.0.1" # IP-адрес сервера
SERVER_PORT = 55555 # порт сервера
separator_token = "<SEP>" # мы будем использовать это, чтобы разделить имя клиента и сообщение

# инициализирует TCP-сокет
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# подключиться к серверу
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
# запрашивать у клиента имя
name = input("Enter your name: ")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    # входное сообщение, которое мы хотим отправить на сервер
    to_send =  input()
    # способ выйти из программы
    if to_send.lower() == 'q':
        break
    # добавить дату, время и имя
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f"[{date_now}] {name}{separator_token}{to_send}"
    # отправляет сообщение
    s.send(to_send.encode())

# закрывает сокет
s.close()