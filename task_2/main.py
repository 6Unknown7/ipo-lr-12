import uuid  # Импортируем модуль для генерации уникальных ID

class Vehicle:
    def __init__(self, capacity: float):
        """Конструктор класса Vehicle (Транспортное средство)."""
        # Валидируем грузоподъемность перед созданием объекта
        self._validate_capacity(capacity)
        
        # Генерируем уникальный ID транспорта (первые 8 символов UUID)
        self.vehicle_id = str(uuid.uuid4())[:8]
        
        # Устанавливаем атрибуты объекта
        self.capacity = capacity      # Максимальная грузоподъемность
        self.current_load = 0         # Текущая загрузка (изначально 0)
        self.clients_list = []        # Список клиентов, чьи грузы загружены
    
    def _validate_capacity(self, capacity: float):
        """Валидация грузоподъемности транспортного средства."""
        # Проверка, что грузоподъемность - положительное число
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом")
    
    def load_cargo(self, client: Client):
        """Загрузка груза клиента в транспорт."""
        # Проверка, что передан объект класса Client
        if not isinstance(client, Client):
            raise TypeError("Можно загружать только объекты класса Client")
        
        # Проверка на перегрузку
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError(
                f"Перегруз! Текущая загрузка: {self.current_load}т, "
                f"груз клиента: {client.cargo_weight}т, "
                f"максимум: {self.capacity}т"
            )
        
        # Увеличиваем текущую загрузку на вес груза клиента
        self.current_load += client.cargo_weight
        
        # Добавляем клиента в список загруженных
        self.clients_list.append(client)
        
        return True  # Возвращаем True при успешной загрузке
    
    def can_load(self, cargo_weight: float) -> bool:
        """Проверка возможности загрузки груза определенного веса."""
        # Проверяем, поместится ли груз с учетом текущей загрузки
        return self.current_load + cargo_weight <= self.capacity
    
    def __str__(self):
        """Строковое представление транспортного средства."""
        return (f"Транспорт ID: {self.vehicle_id}, "
                f"Грузоподъемность: {self.capacity}т, "
                f"Текущая загрузка: {self.current_load}т, "
                f"Свободно: {self.capacity - self.current_load}т")
