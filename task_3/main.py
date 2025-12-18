class Truck(Vehicle):
    def __init__(self, capacity: float, color: str):
        """Конструктор класса Truck (Грузовик)."""
        # Вызываем конструктор родительского класса Vehicle
        super().__init__(capacity)
        
        # Валидируем цвет и устанавливаем атрибут
        self._validate_color(color)
        self.color = color
    
    def _validate_color(self, color: str):
        """Валидация цвета грузовика."""
        # Проверка, что цвет - непустая строка
        if not isinstance(color, str) or not color.strip():
            raise ValueError("Цвет должен быть непустой строкой")
    
    def __str__(self):
        """Строковое представление грузовика."""
        # Получаем базовую строку из родительского класса
        base_str = super().__str__()
        # Добавляем информацию о типе и цвете
        return f"{base_str}, Тип: Грузовик, Цвет: {self.color}"


class Train(Vehicle):
    def __init__(self, capacity: float, number_of_cars: int):
        """Конструктор класса Train (Поезд)."""
        # Вызываем конструктор родительского класса
        super().__init__(capacity)
        
        # Валидируем количество вагонов и устанавливаем атрибут
        self._validate_cars(number_of_cars)
        self.number_of_cars = number_of_cars
    
    def _validate_cars(self, number_of_cars: int):
        """Валидация количества вагонов поезда."""
        # Проверка, что количество вагонов - положительное целое число
        if not isinstance(number_of_cars, int) or number_of_cars <= 0:
            raise ValueError("Количество вагонов должно быть положительным целым числом")
    
    def __str__(self):
        """Строковое представление поезда."""
        # Получаем базовую строку из родительского класса
        base_str = super().__str__()
        # Добавляем информацию о типе и количестве вагонов
        return f"{base_str}, Тип: Поезд, Вагонов: {self.number_of_cars}"


class TransportCompany:
    def __init__(self, name: str):
        """Конструктор класса TransportCompany (Транспортная компания)."""
        # Валидируем название компании
        self._validate_name(name)
        self.name = name
        self.vehicles = []  # Список транспортных средств
        self.clients = []   # Список клиентов
    
    def _validate_name(self, name: str):
        """Валидация названия компании."""
        # Проверка, что название - непустая строка
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название компании должно быть непустой строкой")
    
    def add_vehicle(self, vehicle: Vehicle):
        """Добавление транспортного средства в компанию."""
        # Проверка типа добавляемого транспорта
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Можно добавлять только объекты класса Vehicle или его наследников")
        self.vehicles.append(vehicle)
    
    def add_client(self, client: Client):
        """Добавление клиента в компанию."""
        # Проверка типа добавляемого клиента
        if not isinstance(client, Client):
            raise TypeError("Можно добавлять только объекты класса Client")
        self.clients.append(client)
    
    def list_vehicles(self):
        """Получение списка всех транспортных средств компании."""
        return self.vehicles
    
    def optimize_cargo_distribution(self):
        """
        Оптимизирует распределение грузов по транспортным средствам.
        Правила:
        1. VIP-клиенты обслуживаются первыми
        2. Используется минимальное количество транспорта
        """
        # Сортируем клиентов: VIP первыми (VIP=True имеют приоритет)
        sorted_clients = sorted(self.clients, key=lambda x: not x.is_vip)
        
        # Сортируем транспорт по грузоподъемности (от большего к меньшему)
        sorted_vehicles = sorted(self.vehicles, key=lambda x: x.capacity, reverse=True)
        
        # Подготавливаем транспорт к распределению (сбрасываем загрузку)
        for vehicle in sorted_vehicles:
            vehicle.current_load = 0
            vehicle.clients_list = []
        
        # Распределяем грузы
        used_vehicles = []  # Список использованного транспорта
        for client in sorted_clients:
            client_loaded = False
            
            # Пытаемся загрузить в уже используемый транспорт
            for vehicle in used_vehicles:
                if vehicle.can_load(client.cargo_weight):
                    vehicle.load_cargo(client)
                    client_loaded = True
                    break
            
            # Если не поместилось, ищем новый транспорт
            if not client_loaded:
                for vehicle in sorted_vehicles:
                    if vehicle not in used_vehicles and vehicle.can_load(client.cargo_weight):
                        vehicle.load_cargo(client)
                        used_vehicles.append(vehicle)
                        client_loaded = True
                        break
            
            # Если груз не удалось разместить
            if not client_loaded:
                print(f"Предупреждение: Груз клиента {client.name} ({client.cargo_weight}т) "
                      f"не поместился ни в один транспорт")
        
        return used_vehicles  # Возвращаем список использованного транспорта
    
    def get_distribution_report(self):
        """Генерация отчета о распределении грузов."""
        # Шапка отчета
        report = f"Отчет компании '{self.name}':\n"
        report += "=" * 50 + "\n"
        
        # Статистика по клиентам
        total_cargo = sum(client.cargo_weight for client in self.clients)
        vip_cargo = sum(client.cargo_weight for client in self.clients if client.is_vip)
        
        report += f"Всего клиентов: {len(self.clients)}\n"
        report += f"VIP клиентов: {sum(1 for client in self.clients if client.is_vip)}\n"
        report += f"Общий вес грузов: {total_cargo}т\n"
        report += f"Вес грузов VIP: {vip_cargo}т\n\n"
        
        # Информация о использованном транспорте
        used_vehicles = [v for v in self.vehicles if v.current_load > 0]
        
        if used_vehicles:
            report += "Использованный транспорт:\n"
            for vehicle in used_vehicles:
                report += f"\n{vehicle}\n"
                
                # Информация о клиентах в транспорте
                if vehicle.clients_list:
                    report += "  Клиенты в этом транспорте:\n"
                    for client in vehicle.clients_list:
                        vip_status = " (VIP)" if client.is_vip else ""
                        report += f"    - {client.name}{vip_status}: {client.cargo_weight}т\n"
                
                # Коэффициент загрузки транспорта (в процентах)
                report += f"  Коэффициент загрузки: {(vehicle.current_load / vehicle.capacity * 100):.1f}%\n"
        else:
            report += "Грузы еще не распределены\n"
        
        return report