from argparse import ArgumentParser
from json import loads, dumps
from os import remove
from os.path import exists, join
import tempfile


storage_path = join(tempfile.gettempdir(), 'storage.data')


def clear():
    remove(storage_path)


def new_data():
    # Если нет открытого файла, возвращает словарь
    # Если есть открытый файл, возвращает данные из него в виде словаря

    if not exists(storage_path):
        return {}

    with open(storage_path, 'r') as f:
        new_data = f.read()
        if new_data:
            return loads(new_data)

        return {}


def put(key, value):
    # Принимает ключ и значение
    # Если ключ уже есть в словаре, добавляет ему новое значение
    # Если ключа нет, создаёт новую пару ключ-значение
    # В конце записывает данные в файл (создаёт файл, если его нет)

    data = new_data()
    if key in data:
        data[key].append(value)
    else:
        data[key] = [value]

    with open(storage_path, 'w') as f:
        f.write(dumps(data))


def get(key):
    data = new_data()
    return data.get(key)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--key', help='Key')
    parser.add_argument('--val', help='Value')
    parser.add_argument('--clear', action='store_true', help='Clear')

    args = parser.parse_args()

    if args.clear:
        clear()
    elif args.key and args.val:
        put(args.key, args.val)
    elif args.key:
        if get(args.key) == None:
            print("")
        else:
            print(*get(args.key), sep=", ")
    else:
        print('Error')
