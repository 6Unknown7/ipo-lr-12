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