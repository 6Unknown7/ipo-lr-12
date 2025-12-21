from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QTableWidgetItem, QDialog, QMessageBox, QFileDialog
)
from PyQt6.QtGui import QAction, QFont
from transport import Client, Truck, Train, TransportCompany
import json
import re


def kg_to_tons(kg: float) -> float:
    return kg / 1000.0


class ClientDialog(QDialog):
    def __init__(self, parent=None, client: Client = None):
        super().__init__(parent)
        self.setWindowTitle("Клиент")
        self.resize(300, 150)
        layout = QtWidgets.QFormLayout(self)

        self.name_edit = QtWidgets.QLineEdit()
        self.weight_edit = QtWidgets.QLineEdit()
        self.vip_check = QtWidgets.QCheckBox()

        self.name_edit.setPlaceholderText("Только буквы, минимум 2 символа")
        self.weight_edit.setPlaceholderText("Вес в кг (<=10000)")

        layout.addRow("Имя клиента:", self.name_edit)
        layout.addRow("Вес груза (кг):", self.weight_edit)
        layout.addRow("VIP:", self.vip_check)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

        # Сделать Save кнопкой по умолчанию для Enter
        try:
            save_btn = btns.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
            if save_btn:
                save_btn.setDefault(True)
                save_btn.setAutoDefault(True)
        except Exception:
            pass

        # Тултипы для полей
        self.name_edit.setToolTip("Введите имя клиента (только буквы, минимум 2 символа)")
        self.weight_edit.setToolTip("Вес груза в килограммах (положительное, <=10000)")
        self.vip_check.setToolTip("Отметьте, если клиент VIP")

        if client:
            self.name_edit.setText(client.name)
            self.weight_edit.setText(str(int(client.cargo_weight * 1000)))
            self.vip_check.setChecked(client.is_vip)

    def accept(self) -> None:
        name = self.name_edit.text().strip()
        weight_text = self.weight_edit.text().strip()

        if len(name) < 2 or not re.match(r'^[A-Za-zА-Яа-яЁё\s-]+$', name):
            QMessageBox.warning(self, "Ошибка", "Имя клиента должно содержать только буквы и быть не короче 2 символов")
            self.name_edit.clear()
            return

        try:
            weight_kg = float(weight_text)
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Вес груза должен быть числом")
            self.weight_edit.clear()
            return

        if weight_kg <= 0 or weight_kg > 10000:
            QMessageBox.warning(self, "Ошибка", "Вес груза должен быть >0 и <=10000 кг")
            self.weight_edit.clear()
            return

        self.client_data = {
            'name': name,
            'cargo_weight_t': kg_to_tons(weight_kg),
            'is_vip': bool(self.vip_check.isChecked())
        }
        super().accept()

    def keyPressEvent(self, event):
        # Enter = accept, Esc = reject
        try:
            if event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
                self.accept()
                return
            if event.key() == QtCore.Qt.Key.Key_Escape:
                self.reject()
                return
        except Exception:
            pass
        super().keyPressEvent(event)


class VehicleDialog(QDialog):
    def __init__(self, parent=None, vehicle=None):
        super().__init__(parent)
        self.setWindowTitle("Транспорт")
        self.resize(320, 200)
        layout = QtWidgets.QFormLayout(self)

        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["Грузовик", "Поезд"])
        self.capacity_edit = QtWidgets.QLineEdit()
        self.extra_edit = QtWidgets.QLineEdit()

        self.capacity_edit.setPlaceholderText("Грузоподъемность (тонн)")
        self.extra_edit.setPlaceholderText("Цвет (для грузовика) или кол-во вагонов (для поезда)")

        layout.addRow("Тип транспорта:", self.type_combo)
        layout.addRow("Грузоподъемность (т):", self.capacity_edit)
        layout.addRow("Дополнительно:", self.extra_edit)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

        # Сделать Save кнопкой по умолчанию
        try:
            save_btn = btns.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
            if save_btn:
                save_btn.setDefault(True)
                save_btn.setAutoDefault(True)
        except Exception:
            pass

        # Тултипы для полей
        self.type_combo.setToolTip("Выберите тип транспорта")
        self.capacity_edit.setToolTip("Грузоподъемность в тоннах (положительное число)")
        self.extra_edit.setToolTip("Цвет грузовика или количество вагонов для поезда")

        if vehicle:
            if isinstance(vehicle, Truck):
                self.type_combo.setCurrentText("Грузовик")
                self.extra_edit.setText(vehicle.color)
            elif isinstance(vehicle, Train):
                self.type_combo.setCurrentText("Поезд")
                self.extra_edit.setText(str(vehicle.number_of_cars))
            self.capacity_edit.setText(str(vehicle.capacity))

    def accept(self) -> None:
        vtype = self.type_combo.currentText()
        try:
            capacity = float(self.capacity_edit.text().strip())
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Грузоподъемность должна быть числом")
            self.capacity_edit.clear()
            return

        if capacity <= 0:
            QMessageBox.warning(self, "Ошибка", "Грузоподъемность должна быть положительной")
            self.capacity_edit.clear()
            return

        extra = self.extra_edit.text().strip()
        if vtype == "Грузовик":
            if not extra:
                QMessageBox.warning(self, "Ошибка", "Укажите цвет грузовика")
                return
            self.vehicle_data = {'type': 'truck', 'capacity': capacity, 'color': extra}
        else:
            try:
                cars = int(extra)
                if cars <= 0:
                    raise ValueError()
            except Exception:
                QMessageBox.warning(self, "Ошибка", "Количество вагонов должно быть положительным целым числом")
                self.extra_edit.clear()
                return
            self.vehicle_data = {'type': 'train', 'capacity': capacity, 'cars': cars}

        super().accept()

    def keyPressEvent(self, event):
        try:
            if event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
                self.accept()
                return
            if event.key() == QtCore.Qt.Key.Key_Escape:
                self.reject()
                return
        except Exception:
            pass
        super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Транспортная компания — GUI")
        self.resize(900, 600)

        self.company = TransportCompany("Быстрая Доставка")

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # Toolbar buttons
        toolbar = QtWidgets.QHBoxLayout()
        add_client_btn = QtWidgets.QPushButton("Добавить клиента")
        add_client_btn.setToolTip("Добавить нового клиента")
        add_client_btn.clicked.connect(self.add_client)
        add_vehicle_btn = QtWidgets.QPushButton("Добавить транспорт")
        add_vehicle_btn.setToolTip("Добавить новое транспортное средство")
        add_vehicle_btn.clicked.connect(self.add_vehicle)
        distribute_btn = QtWidgets.QPushButton("Распределить грузы")
        distribute_btn.setToolTip("Запустить оптимальное распределение грузов")
        distribute_btn.clicked.connect(self.distribute)
        delete_btn = QtWidgets.QPushButton("Удалить выбранное")
        delete_btn.setToolTip("Удалить выбранные записи из таблицы")
        delete_btn.clicked.connect(self.delete_selected)
        export_btn = QtWidgets.QPushButton("Экспорт отчёта")
        export_btn.setToolTip("Экспортировать результат распределения в файл")
        export_btn.clicked.connect(self.export_result)

        toolbar.addWidget(add_client_btn)
        toolbar.addWidget(add_vehicle_btn)
        toolbar.addWidget(distribute_btn)
        toolbar.addWidget(delete_btn)
        toolbar.addWidget(export_btn)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        # Tables
        tables_layout = QtWidgets.QHBoxLayout()

        # Клиенты: фильтр + таблица
        clients_layout = QtWidgets.QVBoxLayout()
        self.clients_filter = QtWidgets.QLineEdit()
        self.clients_filter.setPlaceholderText("Фильтр клиентов по имени...")
        self.clients_filter.setToolTip("Вводите часть имени для фильтрации списка клиентов")
        self.clients_filter.textChanged.connect(self.filter_clients)
        clients_layout.addWidget(self.clients_filter)

        self.clients_table = QtWidgets.QTableWidget(0, 3)
        self.clients_table.setHorizontalHeaderLabels(["Имя", "Вес (т)", "VIP"])
        self.clients_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.clients_table.cellDoubleClicked.connect(self.edit_client)
        # Растягиваем столбцы равномерно
        # равномерная растяжка колонок для таблицы клиентов
        try:
            self.clients_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception:
            try:
                self.clients_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            except Exception:
                pass
        # включаем сортировку
        self.clients_table.setSortingEnabled(True)
        # Выделение строк и множественный выбор
        self.clients_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.clients_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        # Стилизация выделения (синяя подсветка)
        try:
            self.clients_table.setStyleSheet("QTableWidget::item:selected{background-color: #0078d7; color: white;}")
        except Exception:
            pass

        clients_layout.addWidget(self.clients_table)

        # Транспорт: фильтр + таблица
        vehicles_layout = QtWidgets.QVBoxLayout()
        self.vehicles_filter = QtWidgets.QLineEdit()
        self.vehicles_filter.setPlaceholderText("Фильтр транспорта по ID или типу...")
        self.vehicles_filter.setToolTip("Фильтр по ID или типу транспорта")
        self.vehicles_filter.textChanged.connect(self.filter_vehicles)
        vehicles_layout.addWidget(self.vehicles_filter)

        self.vehicles_table = QtWidgets.QTableWidget(0, 4)
        self.vehicles_table.setHorizontalHeaderLabels(["ID", "Тип", "Грузоподъемность (т)", "Загрузка (т)"])
        self.vehicles_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.vehicles_table.cellDoubleClicked.connect(self.edit_vehicle)
        # Настройка размеров столбцов: ID/Тип/Грузоподъемность по содержимому, загрузка растягивается
        try:
            header = self.vehicles_table.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception:
            try:
                header = self.vehicles_table.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
            except Exception:
                pass
        # включаем сортировку
        self.vehicles_table.setSortingEnabled(True)

        # Выделение строк и множественный выбор для транспорта (удобное удаление)
        self.vehicles_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.vehicles_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        try:
            self.vehicles_table.setStyleSheet("QTableWidget::item:selected{background-color: #0078d7; color: white;}")
        except Exception:
            pass

        vehicles_layout.addWidget(self.vehicles_table)

        tables_layout.addLayout(clients_layout)
        tables_layout.addLayout(vehicles_layout)

        layout.addLayout(tables_layout)

        # Status bar
        self.status = self.statusBar()
        self.status.showMessage("Готово")

        # Menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")
        export_action = QAction("Экспорт результата", self)
        export_action.triggered.connect(self.export_result)
        file_menu.addAction(export_action)

        save_action = QAction("Сохранить данные", self)
        save_action.triggered.connect(self.save_state)
        file_menu.addAction(save_action)

        load_action = QAction("Загрузить данные", self)
        load_action.triggered.connect(self.load_state)
        file_menu.addAction(load_action)

        about_menu = menubar.addMenu("Справка")
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)

    def refresh_tables(self):
        # Clients
        self.clients_table.setRowCount(0)
        for client in self.company.clients:
            row = self.clients_table.rowCount()
            self.clients_table.insertRow(row)
            self.clients_table.setItem(row, 0, QTableWidgetItem(client.name))
            self.clients_table.setItem(row, 1, QTableWidgetItem(f"{client.cargo_weight:.2f}"))
            self.clients_table.setItem(row, 2, QTableWidgetItem("Да" if client.is_vip else "Нет"))

        # Vehicles
        self.vehicles_table.setRowCount(0)
        for vehicle in self.company.vehicles:
            row = self.vehicles_table.rowCount()
            self.vehicles_table.insertRow(row)
            self.vehicles_table.setItem(row, 0, QTableWidgetItem(vehicle.vehicle_id))
            vtype = "Грузовик" if isinstance(vehicle, Truck) else "Поезд"
            self.vehicles_table.setItem(row, 1, QTableWidgetItem(vtype))
            self.vehicles_table.setItem(row, 2, QTableWidgetItem(f"{vehicle.capacity:.2f}"))
            self.vehicles_table.setItem(row, 3, QTableWidgetItem(f"{vehicle.current_load:.2f}"))

        # После обновления таблиц применяем текущие фильтры
        self.filter_clients(self.clients_filter.text())
        self.filter_vehicles(self.vehicles_filter.text())

    def add_client(self):
        dlg = ClientDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.client_data
            client = Client(data['name'], data['cargo_weight_t'], data['is_vip'])
            self.company.add_client(client)
            self.status.showMessage("Клиент добавлен", 5000)
            self.refresh_tables()

    def add_vehicle(self):
        dlg = VehicleDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d = dlg.vehicle_data
            if d['type'] == 'truck':
                v = Truck(d['capacity'], d['color'])
            else:
                v = Train(d['capacity'], d['cars'])
            self.company.add_vehicle(v)
            self.status.showMessage("Транспорт добавлен", 5000)
            self.refresh_tables()

    def edit_client(self, row, _col):
        client = self.company.clients[row]
        dlg = ClientDialog(self, client)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d = dlg.client_data
            client.name = d['name']
            client.cargo_weight = d['cargo_weight_t']
            client.is_vip = d['is_vip']
            self.status.showMessage("Клиент обновлён", 5000)
            self.refresh_tables()

    def edit_vehicle(self, row, _col):
        vehicle = self.company.vehicles[row]
        dlg = VehicleDialog(self, vehicle)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d = dlg.vehicle_data
            # recreate vehicle to simplify
            if d['type'] == 'truck':
                new_v = Truck(d['capacity'], d['color'])
            else:
                new_v = Train(d['capacity'], d['cars'])
            new_v.vehicle_id = vehicle.vehicle_id
            self.company.vehicles[row] = new_v
            self.status.showMessage("Транспорт обновлён", 5000)
            self.refresh_tables()

    def delete_selected(self):
        # try vehicles selection first (удобнее удалять транспорт)
        vsel = self.vehicles_table.selectionModel().selectedRows()
        csel = self.clients_table.selectionModel().selectedRows()
        if vsel:
            rows = sorted([r.row() for r in vsel], reverse=True)
            for r in rows:
                del self.company.vehicles[r]
            self.status.showMessage("Выбранный транспорт удалён", 5000)
            self.refresh_tables()
            return
        if csel:
            rows = sorted([r.row() for r in csel], reverse=True)
            for r in rows:
                del self.company.clients[r]
            self.status.showMessage("Выбранные клиенты удалены", 5000)
            self.refresh_tables()
            return
        QMessageBox.information(self, "Удаление", "Ничего не выбрано для удаления")

    def filter_clients(self, text: str):
        text = text.lower().strip()
        for r in range(self.clients_table.rowCount()):
            item = self.clients_table.item(r, 0)
            visible = True
            if text:
                visible = item and text in item.text().lower()
            self.clients_table.setRowHidden(r, not visible)

    def filter_vehicles(self, text: str):
        text = text.lower().strip()
        for r in range(self.vehicles_table.rowCount()):
            id_item = self.vehicles_table.item(r, 0)
            type_item = self.vehicles_table.item(r, 1)
            visible = True
            if text:
                id_match = id_item and text in id_item.text().lower()
                type_match = type_item and text in type_item.text().lower()
                visible = id_match or type_match
            self.vehicles_table.setRowHidden(r, not visible)

    def distribute(self):
        if not self.company.vehicles:
            QMessageBox.warning(self, "Ошибка", "Нет транспортных средств!")
            return
        if not self.company.clients:
            QMessageBox.warning(self, "Ошибка", "Нет клиентов!")
            return
        used = self.company.optimize_cargo_distribution()
        self.refresh_tables()
        report = self.company.get_distribution_report()
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Результат распределения")
        dlg.setText(report)
        dlg.exec()

    def export_result(self):
        report = self.company.get_distribution_report()
        if "Грузы еще не распределены" in report:
            QMessageBox.warning(self, "Ошибка", "Распределение не выполнено — нечего экспортировать")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить отчет", filter="Text Files (*.txt);;All Files (*)")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(report)
            self.status.showMessage(f"Отчет сохранён: {path}", 5000)

    def save_state(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить данные", filter="JSON Files (*.json);;All Files (*)")
        if not path:
            return
        data = {
            'clients': [{'name': c.name, 'cargo_weight_t': c.cargo_weight, 'is_vip': c.is_vip} for c in self.company.clients],
            'vehicles': []
        }
        for v in self.company.vehicles:
            if isinstance(v, Truck):
                data['vehicles'].append({'type': 'truck', 'capacity': v.capacity, 'color': v.color, 'id': v.vehicle_id})
            else:
                data['vehicles'].append({'type': 'train', 'capacity': v.capacity, 'cars': v.number_of_cars, 'id': v.vehicle_id})
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.status.showMessage(f"Данные сохранены: {path}", 5000)

    def load_state(self):
        path, _ = QFileDialog.getOpenFileName(self, "Загрузить данные", filter="JSON Files (*.json);;All Files (*)")
        if not path:
            return
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.company.clients = [Client(c['name'], c['cargo_weight_t'], c.get('is_vip', False)) for c in data.get('clients', [])]
        self.company.vehicles = []
        for v in data.get('vehicles', []):
            if v['type'] == 'truck':
                obj = Truck(v['capacity'], v.get('color', ''))
            else:
                obj = Train(v['capacity'], v.get('cars', 1))
            obj.vehicle_id = v.get('id', obj.vehicle_id)
            self.company.vehicles.append(obj)
        self.refresh_tables()
        self.status.showMessage(f"Данные загружены: {path}", 5000)

    def show_about(self):
        QMessageBox.information(self, "О программе", "ЛР 13\nВариант: 1\nРазработчик: Королёв Даниил Игоревич")


def run_app():
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    return app.exec()
