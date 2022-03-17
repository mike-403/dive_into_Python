import socket


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def put(self, command, value, timestamp):
        info = '{}, {}, {}'.format(command, value, timestamp)
        return self.send(info)

    def get(self, command):
        self.send(command)
        data = self.sock.recv(1024)
        print(data.decode("utf8"))
        self.sock.close()

    def send(self, info):
        with socket.create_connection((self.host, self.port), self.timeout) as self.sock:
            self.sock.sendall(info.encode("utf8"))




