#Пакет с хранением всех классов
import uuid

class Client:
    def __init__(self, name: str, cargo_weight: float, is_vip: bool = False):
        self._validate_data(name, cargo_weight, is_vip)
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
    
    def _validate_data(self, name: str, cargo_weight: float, is_vip: bool):
        """Валидация данных клиента"""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя клиента должно быть непустой строкой")
        if not isinstance(cargo_weight, (int, float)) or cargo_weight <= 0:
            raise ValueError("Вес груза должен быть положительным числом")
        if not isinstance(is_vip, bool):
            raise TypeError("is_vip должен быть булевым значением")
    
    def __str__(self):
        vip_status = "VIP" if self.is_vip else "Обычный"
        return f"Клиент: {self.name}, Груз: {self.cargo_weight}т, Статус: {vip_status}"


class Vehicle:
    def __init__(self, capacity: float):
        self._validate_capacity(capacity)
        self.vehicle_id = str(uuid.uuid4())[:8]
        self.capacity = capacity
        self.current_load = 0
        self.clients_list = []
    
    def _validate_capacity(self, capacity: float):
        """Валидация грузоподъемности"""
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом")
    
    def load_cargo(self, client: Client):
        """Загрузка груза клиента"""
        if not isinstance(client, Client):
            raise TypeError("Можно загружать только объекты класса Client")
        
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError(
                f"Перегруз! Текущая загрузка: {self.current_load}т, "
                f"груз клиента: {client.cargo_weight}т, "
                f"максимум: {self.capacity}т"
            )
        
        self.current_load += client.cargo_weight
        self.clients_list.append(client)
        return True
    
    def can_load(self, cargo_weight: float) -> bool:
        """Проверка, можно ли загрузить груз"""
        return self.current_load + cargo_weight <= self.capacity
    
    def __str__(self):
        return (f"Транспорт ID: {self.vehicle_id}, "
                f"Грузоподъемность: {self.capacity}т, "
                f"Текущая загрузка: {self.current_load}т, "
                f"Свободно: {self.capacity - self.current_load}т")


class Truck(Vehicle):
    def __init__(self, capacity: float, color: str):
        super().__init__(capacity)
        self._validate_color(color)
        self.color = color
    
    def _validate_color(self, color: str):
        """Валидация цвета"""
        if not isinstance(color, str) or not color.strip():
            raise ValueError("Цвет должен быть непустой строкой")
    
    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Тип: Грузовик, Цвет: {self.color}"


class Train(Vehicle):
    def __init__(self, capacity: float, number_of_cars: int):
        super().__init__(capacity)
        self._validate_cars(number_of_cars)
        self.number_of_cars = number_of_cars
    
    def _validate_cars(self, number_of_cars: int):
        """Валидация количества вагонов"""
        if not isinstance(number_of_cars, int) or number_of_cars <= 0:
            raise ValueError("Количество вагонов должно быть положительным целым числом")
    
    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Тип: Поезд, Вагонов: {self.number_of_cars}"


class TransportCompany:
    def __init__(self, name: str):
        self._validate_name(name)
        self.name = name
        self.vehicles = []
        self.clients = []
    
    def _validate_name(self, name: str):
        """Валидация названия компании"""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название компании должно быть непустой строкой")
    
    def add_vehicle(self, vehicle: Vehicle):
        """Добавление транспортного средства"""
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Можно добавлять только объекты класса Vehicle или его наследников")
        self.vehicles.append(vehicle)
    
    def add_client(self, client: Client):
        """Добавление клиента"""
        if not isinstance(client, Client):
            raise TypeError("Можно добавлять только объекты класса Client")
        self.clients.append(client)
    
    def list_vehicles(self):
        """Возвращает список всех транспортных средств"""
        return self.vehicles
    
    def optimize_cargo_distribution(self):
        """
        Оптимизирует распределение грузов:
        1. VIP клиенты обслуживаются первыми
        2. Используется минимальное количество транспорта
        """
        sorted_clients = sorted(self.clients, key=lambda x: not x.is_vip)
        sorted_vehicles = sorted(self.vehicles, key=lambda x: x.capacity, reverse=True)
        
        for vehicle in sorted_vehicles:
            vehicle.current_load = 0
            vehicle.clients_list = []
        
        used_vehicles = []
        for client in sorted_clients:
            client_loaded = False
            
            for vehicle in used_vehicles:
                if vehicle.can_load(client.cargo_weight):
                    vehicle.load_cargo(client)
                    client_loaded = True
                    break
            
            if not client_loaded:
                for vehicle in sorted_vehicles:
                    if vehicle not in used_vehicles and vehicle.can_load(client.cargo_weight):
                        vehicle.load_cargo(client)
                        used_vehicles.append(vehicle)
                        client_loaded = True
                        break
            
            if not client_loaded:
                print(f"Предупреждение: Груз клиента {client.name} ({client.cargo_weight}т) "
                      f"не поместился ни в один транспорт")
        
        return used_vehicles
    
    def get_distribution_report(self):
        """Генерирует отчет о распределении грузов"""
        report = f"Отчет компании '{self.name}':\n"
        report += "=" * 50 + "\n"
        
        total_cargo = sum(client.cargo_weight for client in self.clients)
        vip_cargo = sum(client.cargo_weight for client in self.clients if client.is_vip)
        
        report += f"Всего клиентов: {len(self.clients)}\n"
        report += f"VIP клиентов: {sum(1 for client in self.clients if client.is_vip)}\n"
        report += f"Общий вес грузов: {total_cargo}т\n"
        report += f"Вес грузов VIP: {vip_cargo}т\n\n"
        
        used_vehicles = [v for v in self.vehicles if v.current_load > 0]
        
        if used_vehicles:
            report += "Использованный транспорт:\n"
            for vehicle in used_vehicles:
                report += f"\n{vehicle}\n"
                if vehicle.clients_list:
                    report += "  Клиенты в этом транспорте:\n"
                    for client in vehicle.clients_list:
                        vip_status = " (VIP)" if client.is_vip else ""
                        report += f"    - {client.name}{vip_status}: {client.cargo_weight}т\n"
                report += f"  Коэффициент загрузки: {(vehicle.current_load / vehicle.capacity * 100):.1f}%\n"
        else:
            report += "Грузы еще не распределены\n"
        
        return report