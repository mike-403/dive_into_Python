


import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = int(port)
        self.timeout = int(timeout)

    def send(self, cmd):
        """Создание канала с сервером"""
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            sock.sendall(cmd.encode("utf8"))
            buf = sock.recv(1024)
            return buf.decode('utf-8')

    def put(self, key, val, timestamp=None):
        """Обработка команды отправки метрики"""
        resp = self.send('put ' + key + ' ' + str(val) + ' ' + str(timestamp if timestamp else int(time.time())) + '\n')
        if resp[0:3] != 'ok\n':
            raise ClientError(resp)

    def get(self, key):
        """Обработка команды получения метрики"""
        resp = self.send('get ' + key + '\n')
        if resp[0:3] != 'ok\n':
            raise ClientError(resp)
        ret = dict()
        lines = resp.split('\n')
        try:
            for i in lines[1:-2]:
                info = i.split(' ')
                info_key = info[0]
                info_val = float(info[1])
                info_ts = int(info[2])
                if info_key not in ret:
                    ret[info_key] = list()
                ret[info_key].append((info_ts, info_val))
                ret[info_key].sort(key=lambda tup: tup[0])
        except:
            raise ClientError(Exception)

        return ret


