from transport import Client, Truck, Train, TransportCompany

def main():
    """Основная функция программы - меню транспортной компании."""
    
    # Создаем транспортную компанию с названием "Быстрая Доставка"
    company = TransportCompany("Быстрая Доставка")
    
    # Основной цикл меню
    while True:
        print("\n" + "=" * 50)
        print("МЕНЮ ТРАНСПОРТНОЙ КОМПАНИИ")
        print("=" * 50)
        print("1. Добавить транспортное средство")
        print("2. Добавить клиента")
        print("3. Показать все транспортные средства")
        print("4. Показать всех клиентов")
        print("5. Распределить грузы оптимально")
        print("6. Показать отчет о распределении")
        print("0. Выход")
        
        # Получаем выбор пользователя
        choice = input("\nВыберите действие: ")
        
        if choice == "1":
            # Добавление нового транспортного средства
            print("\nДобавление транспортного средства:")
            print("1. Грузовик")
            print("2. Поезд")
            
            vehicle_type = input("Выберите тип транспорта: ")
            
            try:
                # Получаем грузоподъемность
                capacity = float(input("Введите грузоподъемность (тонн): "))
                
                # Создаем транспорт в зависимости от типа
                if vehicle_type == "1":
                    color = input("Введите цвет грузовика: ")
                    vehicle = Truck(capacity, color)
                elif vehicle_type == "2":
                    cars = int(input("Введите количество вагонов: "))
                    vehicle = Train(capacity, cars)
                else:
                    print("Неверный выбор типа транспорта!")
                    continue
                
                # Добавляем транспорт в компанию
                company.add_vehicle(vehicle)
                print(f"Транспорт успешно добавлен! ID: {vehicle.vehicle_id}")
                
            except ValueError as e:
                print(f"Ошибка: {e}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
        
        elif choice == "2":
            # Добавление нового клиента
            print("\nДобавление клиента:")
            
            try:
                # Получаем данные клиента
                name = input("Введите имя клиента: ")
                cargo_weight = float(input("Введите вес груза (тонн): "))
                vip_input = input("VIP клиент? (да/нет): ").lower()
                
                # Определяем VIP-статус
                is_vip = vip_input in ['да', 'yes', 'y', 'д']
                
                # Создаем клиента
                client = Client(name, cargo_weight, is_vip)
                company.add_client(client)
                print(f"Клиент {name} успешно добавлен!")
                
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        elif choice == "3":
            # Показ всех транспортных средств
            print("\nВсе транспортные средства:")
            vehicles = company.list_vehicles()
            
            if vehicles:
                # Выводим пронумерованный список транспорта
                for i, vehicle in enumerate(vehicles, 1):
                    print(f"{i}. {vehicle}")
            else:
                print("Транспортные средства отсутствуют")
        
        elif choice == "4":
            # Показ всех клиентов
            print("\nВсе клиенты:")
            if company.clients:
                # Выводим пронумерованный список клиентов
                for i, client in enumerate(company.clients, 1):
                    print(f"{i}. {client}")
            else:
                print("Клиенты отсутствуют")
        
        elif choice == "5":
            # Оптимальное распределение грузов
            if not company.vehicles:
                print("Ошибка: Нет транспортных средств!")
                continue
            if not company.clients:
                print("Ошибка: Нет клиентов!")
                continue
            
            try:
                print("\nНачинаем распределение грузов...")
                # Выполняем распределение
                used_vehicles = company.optimize_cargo_distribution()
                print(f"Распределение завершено! Использовано {len(used_vehicles)} единиц транспорта")
                
            except Exception as e:
                print(f"Ошибка при распределении: {e}")
        
        elif choice == "6":
            # Показ отчета о распределении
            print(company.get_distribution_report())
        
        elif choice == "0":
            # Выход из программы
            print("До свидания!")
            break
        
        else:
            # Некорректный выбор
            print("Неверный выбор. Попробуйте снова.")

# Точка входа в программу
if __name__ == "__main__":
    main() 
