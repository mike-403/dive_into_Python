import asyncio

data_storage = dict()

class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        """Создаёт канал связи"""
        self.transport = transport

    def data_received(self, data):
        """Запись полученных данных"""
        self.transport.write(self.process(data.decode('utf-8').strip('\r\n')).encode('utf-8'))

    def process(self, command):
        """Разделение строки и направление на обработку комманд"""
        slices = command.split(' ')
        if slices[0] == 'get':
            if len(slices[1:]) != 1:
                return 'error\nwrong command\n\n'
            else:
                return self.get_decoder(slices[1])
        elif slices[0] == 'put':
            if len(slices[1:]) != 3:
                return 'error\nwrong command\n\n'
            else:
                return self.put_decoder(slices[1], slices[2], slices[3])
        else:
            return 'error\nwrong command\n\n'

    def get_decoder(self, key):
        """Обработка команды get"""
        res = 'ok\n'
        if key == '*':
            for key, values in data_storage.items():
                for value in values:
                    res = res + key + ' ' + value[1] + ' ' + value[0] + '\n'
        else:
            if key in data_storage:
                for value in data_storage[key]:
                    res = res + key + ' ' + value[1] + ' ' + value[0] + '\n'

        return res + '\n'

    def put_decoder(self, key, value, timestamp):
        """Обработка команды get"""
        if key == '*':
            return 'error\nkey cannot contain *\n\n'
        if not key in data_storage:
            data_storage[key] = list()
        if not (timestamp, value) in data_storage[key]:
            try:
                data_storage[key].append((str(int(timestamp)), str(float(value))))
            except:
                return 'error\nwrong command\n\n'
            data_storage[key].sort(key=lambda tup: tup[0])
        return 'ok\n\n'

def run_server(host, port):
    """Создание копии класса сервера с заданными параметрами"""
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

#if __name__ == "__main__":
    #run_server("127.0.0.1", 8888)