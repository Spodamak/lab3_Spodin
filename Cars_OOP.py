class Car:
    def __init__(self, manufacturer, model, car_type, number, color, dtp):
        # Конструктор класса Car, инициализирует объект с переданными атрибутами
        self.manufacturer = manufacturer
        self.model = model
        self.car_type = car_type
        self.number = number
        self.color = color
        self.dtp = dtp

    def __str__(self):
        # Метод, возвращающий строковое представление объекта Car
        return f"{self.manufacturer} {self.model} ({self.car_type}) ({self.number}) {self.color},{self.dtp}"


class CarManager:
    def __init__(self):
        # Конструктор класса CarManager, инициализирует объект управления автомобилями
        self.cars = self.load_cars_from_file('cars.txt')

    def load_cars_from_file(self, filename):
        # Метод загрузки данных об автомобилях из файла
        cars = []
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                car = {}
                for line in lines:
                    line = line.strip()
                    if line.startswith("Производитель: "):
                        _, car['manufacturer'] = line.split(": ", 1)
                    elif line.startswith("Модель: "):
                        _, car['model'] = line.split(": ", 1)
                    elif line.startswith("Вид машины: "):
                        _, car['car_type'] = line.split(": ", 1)
                    elif line.startswith("Номер автомобиля: "):
                        _, car['number'] = line.split(": ", 1)
                    elif line.startswith("Цвет автомобиля: "):
                        _, car['color'] = line.split(": ", 1)
                    elif line.startswith("Был ли автомобиль в ДТП: "):
                        _, car['dtp'] = line.split(": ", 1)
                    elif not line:
                        cars.append(Car(**car))
                        car = {}
        except FileNotFoundError:
            pass
        return cars

    def save_cars_to_file(self, filename):
        # Метод сохранения данных об автомобилях в файл
        with open(filename, 'w') as file:
            for car in self.cars:
                file.write(f"Производитель: {car.manufacturer}\n")
                file.write(f"Модель: {car.model}\n")
                file.write(f"Вид машины: {car.car_type}\n")
                file.write(f"Номер автомобиля: {car.number}\n")
                file.write(f"Цвет автомобиля: {car.color}\n")
                file.write(f"Был ли автомобиль в ДТП: {car.dtp}\n")
                file.write("\n")

    def search_cars(self, search_criteria):
        # Метод поиска автомобилей по критерию
        matched_cars = []

        for car in self.cars:
            if 'дтп' in search_criteria.lower() and car.dtp.lower() == 'да':
                matched_cars.append(car)
            if any(value.lower().startswith(search_criteria.lower()) for value in car.__dict__.values()):
                matched_cars.append(car)

        return matched_cars

    def print_car_list(self, cars=None):
        # Метод вывода списка автомобилей
        cars_to_print = cars if cars else self.cars
        if not cars_to_print:
            print("Список автомобилей пуст.")
        else:
            for i, car in enumerate(cars_to_print):
                print(f"{i + 1}. {car}")

    def get_car_type(self, choice):
        # Метод получения типа машины по выбору пользователя
        car_types = ["Легковая", "Грузовая", "Мотоцикл", "Бронетехника"]
        try:
            index = int(choice) - 1
            return car_types[index] if 0 <= index < len(car_types) else "Неопределен"
        except ValueError:
            return "Неопределен"

    def input_car_data(self):
        # Метод ввода данных о новом автомобиле
        manufacturer = input("Введите производителя: ")
        model = input("Введите модель: ")

        print("Выберите вид машины:")
        print("1. Легковая")
        print("2. Грузовая")
        print("3. Мотоцикл")
        print("4. Бронетехника")
        car_type_choice = input("Введите номер вида машины (1, 2, 3 или 4): ")

        car_type = self.get_car_type(car_type_choice)

        car_number = input("Введите номер автомобиля: ")
        car_color = input("Введите цвет автомобиля: ")

        dtp_choice = input("Был ли автомобиль в ДТП? (1 - Да, 2 - Нет): ")
        car_dtp = "Да" if dtp_choice == '1' else "Нет"

        return Car(manufacturer, model, car_type, car_number, car_color, car_dtp)

    def edit_car_data(self, car):
        # Метод редактирования данных об автомобиле
        while True:
            print("1. Редактировать производителя")
            print("2. Редактировать модель")
            print("3. Редактировать вид машины")
            print("4. Редактировать номер автомобиля")
            print("5. Редактировать цвет автомобиля")
            print("6. Редактировать информацию о ДТП")
            print("7. Удалить машину")
            choice = input("Выберите, что вы хотите редактировать (1-7, или 'Enter' для отмены): ")

            if not choice:
                # Если пользователь нажал Enter, выводим сообщение и выходим из редактирования
                print("Редактирование отменено\n")
                return False

            if choice == '1':
                car.manufacturer = input("Введите нового производителя: ")
            elif choice == '2':
                car.model = input("Введите новую модель: ")
            elif choice == '3':
                car.car_type = self.get_car_type(input("Введите номер вида машины (1, 2 или 3): "))
            elif choice == '4':
                car.number = input("Введите новый номер автомобиля: ")
            elif choice == '5':
                car.color = input("Введите новый цвет автомобиля: ")
            elif choice == '6':
                car.dtp = "Да" if input("Был ли автомобиль в ДТП? (1 - Да, 2 - Нет): ") == '1' else "Нет"
            elif choice == '7':
                return True  # удалить

    def main(self):
        while True:
            print("1. Вывести список автомобилей")
            print("2. Добавить автомобиль")
            print("3. Редактировать автомобиль")
            print("4. Поиск автомобилей")
            print("5. Сохранить и выйти\n")

            choice = input("Выберите действие: ")

            if choice == '1':
                self.print_car_list()
                print('\n')
            elif choice == '2':
                car_data = self.input_car_data()
                self.cars.append(car_data)
                print("Автомобиль добавлен.")
            elif choice == '3':
                while True:
                    self.print_car_list()
                    if not self.cars:
                        print("Список автомобилей пуст.")
                        break
                    car_index = int(
                        input("Введите номер автомобиля для редактирования (Enter для отмены): ") or '0') - 1
                    if car_index == -1:
                        print("Редактирование отменено\n")
                        break
                    if 0 <= car_index < len(self.cars):
                        if self.edit_car_data(self.cars[car_index]):
                            del self.cars[car_index]
                            print("Машина удалена.")
                        break
                    else:
                        print("Некорректный номер автомобиля.")
            elif choice == '4':
                search_criteria = input("Введите критерий поиска: ")
                matched_cars = self.search_cars(search_criteria)
                if not matched_cars:
                    print("Машина не найдена.")
                else:
                    self.print_car_list(matched_cars)
            elif choice == '5':
                self.save_cars_to_file('cars.txt')
                print("Информация об автомобилях сохранена.")
                break


if __name__ == "__main__":
    car_manager = CarManager()
    car_manager.main()
