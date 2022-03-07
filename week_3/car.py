import csv
import os


class CarBase:
    """Базовый класс автомобиля"""

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = self.value_check(brand)
        self.photo_file_name = self.foto_file_check(photo_file_name)
        self.carrying = float(self.value_check(carrying))

    @staticmethod
    def value_check(value):
        # Проверка, что обязательный атрибут не пустой
        if not value:
            raise ValueError
        return value

    @staticmethod
    def foto_file_check(value):
        # Проверка на допустимый формат файла
        if os.path.splitext(value)[-1] not in ['.jpg', '.jpeg', '.png', '.gif']:
            raise ValueError
        return value

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    """Класс легкового автомобиля"""

    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(self.value_check(passenger_seats_count))


class Truck(CarBase):
    """Класс грузового автомобиля"""

    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_lwh):
        super().__init__(brand, photo_file_name, carrying)
        try:
            l, w, h = list(body_lwh.split('x'))
            self.body_length = float(l)
            self.body_width = float(w)
            self.body_height = float(h)
        except:
            self.body_lwh = 0.0
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    """Класс спецтехники"""

    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = self.value_check(extra)


def parser(row):
    # Обработка данных
    if len(row) != 7:
        return None
    elif row[0] == 'car':
        car = Car(brand=row[1], passenger_seats_count=row[2], photo_file_name=row[3], carrying=row[5])
    elif row[0] == 'truck':
        car = Truck(brand=row[1], photo_file_name=row[3], body_lwh=row[4], carrying=row[5])
    elif row[0] == 'spec_machine':
        car = SpecMachine(brand=row[1], photo_file_name=row[3], carrying=row[5], extra=row[6])
    else:
        return None
    return car


def get_car_list(csv_filename):
    # Считывание данных и внесение данных в список
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        for row in reader:
            try:
                car = parser(row)
                if car is not None:
                    car_list.append(car)
            except:
                pass
        return car_list
