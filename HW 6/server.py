import socket
from threading import Thread

SERVER_HOST = "127.0.0.1" # IP-адрес сервера
SERVER_PORT = 55555 # порт сервера
separator_token = "<SEP>" # мы будем использовать это, чтобы разделить имя клиента и сообщение

# инициализируем список/набор всех подключенных клиентских сокетов
client_sockets = set()
# создать TCP-сокет
s = socket.socket()
# сделать порт многоразовым портом
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# привязать сокет к указанному нами адресу
s.bind((SERVER_HOST, SERVER_PORT))
# слушать предстоящие подключения
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    Эта функция продолжает прослушивать сообщение из сокета `cs`
    Всякий раз, когда сообщение получено, транслируйте его всем другим подключенным клиентам.
    """
    global msg
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator_token, ": ")
        for client_socket in client_sockets:
            client_socket.send(msg.encode())


while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

for cs in client_sockets:
    cs.close()
s.close()