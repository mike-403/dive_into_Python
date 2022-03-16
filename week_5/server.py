import socket


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((self.host, self.port))

    def put(self, command, value, time):
        self.sock.sendall(('{}, {}, {}'.format(command, value, time).encode("utf8")))
        self.sock.close()

    def get(self, command):
        sock.sendall(command.encode("utf8"))
        sock.close()

with socket.socket() as sock:
    sock.bind(("", 10001))
    sock.listen()
    while True:
        conn, addr = sock.accept()
        conn.settimeout(5)  # timeout := None|0|gt 0
        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                    print(response)
                except socket.timeout:
                    print("close connection by timeout")
                    break

                if not data:
                    break
                print(data.decode("utf8"))


"""while True:
    data = conn.recv(1024)
    if not data:
        break
    request = data.decode('utf-8')
    print(f'Получен запрос: {ascii(request)}')
    print(f'Отправлен ответ {ascii(response.decode("utf-8"))}')
    conn.send(response)

conn.close()"""



