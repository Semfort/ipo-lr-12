import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QTableWidgetItem, QApplication, QWidget, QPushButton, QMainWindow, QStatusBar, QTableWidget, QHeaderView, QComboBox, QLabel, QFrame, QMessageBox, QLineEdit, QCheckBox
from PyQt6.QtGui import QKeyEvent, QShowEvent
from PyQt6.QtCore import Qt, pyqtSignal
from transport import Ship, Truck, TransportCompany, Client
#import transport as tr
import json

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.company = TransportCompany("My Transport Company")

        self.cv_window = ChangeVehicle(self.company)
        self.cv_window.vehicle_changed.connect(self.on_vehicle_changed)
        self.av_window = AddVehicle()
        self.av_window.vehicle_added.connect(self.add_vehicle_to_table)
        self.cc_window = ChangeClient(self.company)
        self.cc_window.client_changed.connect(self.on_client_changed)
        self.au_window = AddClient()
        self.au_window.client_added.connect(self.add_client_to_table)
        self.aw_window = AboutWindow()
        
        self.setWindowTitle(self.company.name)
        self.setFixedSize(1100, 700)

        central = QWidget()
        self.setCentralWidget(central)

        label = QLabel("Выберите таблицу:", central)
        label.setGeometry(50, 55, 200, 25)

        self.combo = QComboBox(central)
        self.combo.setGeometry(50, 80, 140, 35)
        self.combo.addItems(["Клиенты", "Транспорт"])
        self.combo.currentTextChanged.connect(self.on_combo_changed)

        btn_delete = QPushButton("Удалить элемент", central)
        btn_delete.setGeometry(50, 125, 140, 40)
        btn_delete.clicked.connect(self.delete_selected_row)

        for y in [170, 300, 488]:
            line_h = QFrame(central)
            line_h.setFrameShape(QFrame.Shape.HLine)
            line_h.setGeometry(20, y, 200, 30)

        line_v = QFrame(central)
        line_v.setFrameShape(QFrame.Shape.VLine)
        line_v.setGeometry(240, 25, 2, 630)

        btn1 = QPushButton("Добавить клиента", central)
        btn1.setGeometry(50, 200, 140, 40)
        btn1.clicked.connect(self.open_add_client)

        btn2 = QPushButton("Изменить клиента", central)
        btn2.setGeometry(50, 250, 140, 40)
        btn2.clicked.connect(self.open_change_client)

        btn3 = QPushButton("Добавить транспорт", central)
        btn3.setGeometry(50, 340, 140, 40)
        btn3.clicked.connect(self.open_add_vehicle)

        btn4 = QPushButton("Изменить транспорт", central)
        btn4.setGeometry(50, 390, 140, 40)
        btn4.clicked.connect(self.open_change_vehicle)

        btn5 = QPushButton("Распределить грузы", central)
        btn5.setGeometry(50, 440, 140, 40)
        btn5.clicked.connect(self.optimize_distribution)

        btn6 = QPushButton("Экспорт результата", central)
        btn6.setGeometry(50, 525, 140, 40)
        btn6.clicked.connect(self.export_to_json)

        btn7 = QPushButton("О программе", central)
        btn7.setGeometry(50, 575, 140, 40)
        btn7.clicked.connect(self.open_about_program)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Программа запущена")

        self.table = QTableWidget(0, 3, central)
        self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
        self.table.setGeometry(325, 85, 700, 500)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def on_combo_changed(self, text):
        try:
            self.table.setRowCount(0)
            if text == "Клиенты":
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
                for client in self.company.clients:
                    self.add_client_row(client)
            elif text == "Транспорт":
                self.table.setColumnCount(6)
                self.table.setHorizontalHeaderLabels(
                    ["ID", "Тип", "Вместительность", "Текущая загрузка", "Цвет", "Название"])
                for vehicle in self.company.vehicles:
                    self.add_vehicle_row(vehicle)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при загрузке таблицы: {str(e)}", 5000)

    def open_add_client(self):
        self.au_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.au_window.show()

    def open_change_client(self):
        self.cc_window.load_clients(self.company)
        self.cc_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.cc_window.show()

    def open_add_vehicle(self):
        self.av_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.av_window.show()

    def open_change_vehicle(self):
        self.cv_window.load_vehicles(self.company)
        self.cv_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.cv_window.show()

    def open_about_program(self):
        self.aw_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.aw_window.show()

    def add_client_to_table(self, name: str, weight: float, is_vip: bool):
        client = Client(name, weight, is_vip)
        self.company.add_client(client)
        if self.combo.currentText() == "Клиенты":
            self.add_client_row(client)
        else:
            self.combo.setCurrentText("Клиенты")
        self.status_bar.showMessage(f"Клиент '{name}' добавлен", 3000)

    def add_vehicle_to_table(self, vehicle):
        self.company.add_vehicle(vehicle)
        if self.combo.currentText() == "Транспорт":
            self.add_vehicle_row(vehicle)
        else:
            self.combo.setCurrentText("Транспорт")
        self.status_bar.showMessage(f"Транспорт '{vehicle.vehicle_id}' добавлен", 3000)

    def add_client_row(self, client):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(client.name))
        self.table.setItem(row, 1, QTableWidgetItem(str(client.cargo_weight)))
        self.table.setItem(row, 2, QTableWidgetItem("VIP" if client.is_vip else "Обычный"))

    def add_vehicle_row(self, vehicle):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(vehicle.vehicle_id))
        self.table.setItem(row, 1, QTableWidgetItem(vehicle.__class__.__name__))
        self.table.setItem(row, 2, QTableWidgetItem(str(vehicle.capacity)))
        self.table.setItem(row, 3, QTableWidgetItem(str(vehicle.current_load)))
        if isinstance(vehicle, Truck):
            self.table.setItem(row, 4, QTableWidgetItem(vehicle.color))
            self.table.setItem(row, 5, QTableWidgetItem("-"))
        elif isinstance(vehicle, Ship):
            self.table.setItem(row, 4, QTableWidgetItem("-"))
            self.table.setItem(row, 5, QTableWidgetItem(vehicle.name))

    def on_cell_double_clicked(self, row, column):
        if self.combo.currentText() == "Клиенты":
            self.open_change_client()
        elif self.combo.currentText() == "Транспорт":
            self.open_change_vehicle()

    def delete_selected_row(self):
        row = self.table.currentRow()
        if row == -1:
            self.status_bar.showMessage("Выберите элемент для удаления", 3000)
            return

        if self.combo.currentText() == "Клиенты":
            del self.company.clients[row]
            self.status_bar.showMessage("Клиент удален", 3000)
        elif self.combo.currentText() == "Транспорт":
            del self.company.vehicles[row]
            self.status_bar.showMessage("Транспорт удален", 3000)
        self.table.removeRow(row)

    def on_client_changed(self, index, name, weight, is_vip):
        self.refresh_table()
        self.status_bar.showMessage(f"Клиент '{name}' изменен", 3000)

    def on_vehicle_changed(self, index, vehicle):
        self.refresh_table()
        self.status_bar.showMessage(f"Транспорт '{vehicle.vehicle_id}' изменен", 3000)

    def optimize_distribution(self):
        try:
            self.company.optimize_cargo_distribution()
            self.combo.currentTextChanged.disconnect()
            self.combo.setCurrentText("Транспорт")
            self.refresh_table()
            self.combo.currentTextChanged.connect(self.on_combo_changed)
            self.status_bar.showMessage("Распределение грузов успешно завершено", 5000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка распределения: {str(e)}", 5000)

    def refresh_table(self):
        self.on_combo_changed(self.combo.currentText())

    def export_to_json(self):
        try:
            data = {
                "clients": [{"name": c.name, "cargo_weight": c.cargo_weight, "is_vip": c.is_vip} for c in self.company.clients],
                "vehicles": [{"vehicle_id": v.vehicle_id, "type": v.__class__.__name__, "capacity": v.capacity, "current_load": v.current_load} for v in self.company.vehicles]
            }
            with open("company_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "Экспорт", "Данные сохранены в company_data.json")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось экспортировать данные: {e}")

class AddClient(QMainWindow):
    client_added = pyqtSignal(str, float, bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить клиента")
        self.setFixedSize(500, 220)

        central = QWidget()
        self.setCentralWidget(central)

        self.line_add_name = QLineEdit(central)
        self.line_add_name.setPlaceholderText("Введите имя клиента")
        self.line_add_name.setGeometry(50, 30, 375, 30)

        self.line_add_weight = QLineEdit(central)
        self.line_add_weight.setPlaceholderText("Введите вес груза")
        self.line_add_weight.setGeometry(50, 80, 375, 30)

        self.check_vip = QCheckBox("VIP-клиент", central)
        self.check_vip.move(53, 130)
        self.check_vip.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        btn = QPushButton("Добавить", central)
        btn.setGeometry(50, 170, 120, 40)
        btn.clicked.connect(self.on_add_client)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(330, 170, 120, 40)
        btn_close.clicked.connect(self.close)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def clear_fields(self):
        self.line_add_name.clear()
        self.line_add_weight.clear()
        self.check_vip.setChecked(False)

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        self.clear_fields()

    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        field.clear()

    def on_add_client(self):
        name = self.line_add_name.text().strip()
        weight_text = self.line_add_weight.text().strip()
        
        if not name:
            self.show_warning("Имя клиента не может быть пустым", self.line_add_name)
            return
            
        try:
            weight = float(weight_text)
        except ValueError:
            self.show_warning("Вес груза должен быть числом", self.line_add_weight)
            return
            
        is_vip = self.check_vip.isChecked()
        
        self.client_added.emit(name, weight, is_vip)
        
        self.clear_fields()
        self.close()

class ChangeClient(QMainWindow):
    client_changed = pyqtSignal(int, str, float, bool)

    def __init__(self, company=None):
        super().__init__()
        self.company = company
        self.setWindowTitle("Изменить клиента")
        self.setFixedSize(600, 500)

        central = QWidget()
        self.setCentralWidget(central)

        self.table = QTableWidget(0, 3, central)
        self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
        self.table.setGeometry(20, 20, 560, 350)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.edit_widget = QWidget(central)
        self.edit_widget.setGeometry(20, 380, 560, 80)
        self.edit_widget.hide()

        self.line_name = QLineEdit(self.edit_widget)
        self.line_name.setGeometry(10, 0, 200, 30)
        self.line_name.setPlaceholderText("Имя клиента")

        self.line_weight = QLineEdit(self.edit_widget)
        self.line_weight.setGeometry(220, 0, 150, 30)
        self.line_weight.setPlaceholderText("Вес груза")

        self.check_vip = QCheckBox("VIP-клиент", self.edit_widget)
        self.check_vip.move(380, 5)

        btn_save = QPushButton("Сохранить", self.edit_widget)
        btn_save.setGeometry(480, 0, 70, 30)
        btn_save.clicked.connect(self.on_save)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(460, 450, 120, 40)
        btn_close.clicked.connect(self.close)

        self.current_index = None

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def load_clients(self, company):
        self.company = company
        if company is None or not hasattr(company, 'clients'):
            return

        clients_list = company.clients
        self.table.setRowCount(0)
        for idx, client in enumerate(clients_list):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(client.name))
            self.table.setItem(row, 1, QTableWidgetItem(str(client.cargo_weight)))
            self.table.setItem(row, 2, QTableWidgetItem("VIP" if client.is_vip else "Обычный"))

    def on_cell_double_clicked(self, row, column):
        if self.company is None:
            return

        clients_list = self.company.clients if hasattr(self.company, 'clients') else []
        if row < len(clients_list):
            self.current_index = row
            client = clients_list[row]
            self.load_client(client, row)
            self.edit_widget.show()

    def load_client(self, client, index):
        self.current_index = index
        self.line_name.setText(client.name)
        self.line_weight.setText(str(client.cargo_weight))
        self.check_vip.setChecked(client.is_vip)

    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        field.clear()

    def on_save(self):
        if self.current_index is None or self.company is None:
            return

        name = self.line_name.text().strip()
        weight_text = self.line_weight.text().strip()

        if not name or len(name) < 2 or not name.isalpha():
            self.show_warning("Имя должно содержать минимум 2 буквы", self.line_name)
            return
        try:
            weight = float(weight_text)
            if weight <= 0 or weight > 10000:
                self.show_warning("Вес должен быть >0 и <10000", self.line_weight)
                return
        except ValueError:
            self.show_warning("Вес должен быть числом", self.line_weight)
            return

        is_vip = self.check_vip.isChecked()

        clients_list = self.company.clients if hasattr(self.company, 'clients') else []
        if self.current_index < len(clients_list):
            clients_list[self.current_index].name = name
            clients_list[self.current_index].cargo_weight = weight
            clients_list[self.current_index].is_vip = is_vip

            self.table.setItem(self.current_index, 0, QTableWidgetItem(name))
            self.table.setItem(self.current_index, 1, QTableWidgetItem(str(weight)))
            self.table.setItem(self.current_index, 2, QTableWidgetItem("VIP" if is_vip else "Обычный"))

            self.client_changed.emit(self.current_index, name, weight, is_vip)

            self.edit_widget.hide()
            self.current_index = None
            QMessageBox.information(self, "Успех", "Клиент успешно изменен")

class ChangeVehicle(QMainWindow):
    vehicle_changed = pyqtSignal(int, object)

    def __init__(self, company=None):
        super().__init__()
        self.company = company
        self.setWindowTitle("Изменить транспорт")
        self.setFixedSize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)

        self.table = QTableWidget(0, 6, central)
        self.table.setHorizontalHeaderLabels(["ID", "Тип", "Вместительность", "Текущая загрузка", "Цвет", "Название"])
        self.table.setGeometry(20, 20, 760, 400)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.edit_widget = QWidget(central)
        self.edit_widget.setGeometry(20, 440, 760, 70)
        self.edit_widget.hide()

        self.label_type = QLabel("Тип:", self.edit_widget)
        self.label_type.setGeometry(10, 5, 100, 25)

        self.label_type_value = QLabel("", self.edit_widget)
        self.label_type_value.setGeometry(10, 30, 100, 25)
        self.label_type_value.setStyleSheet("QLabel { background-color: #e0e0e0; padding: 4px; border-radius: 3px; }")

        self.label_capacity = QLabel("Вместительность:", self.edit_widget)
        self.label_capacity.setGeometry(120, 5, 150, 25)

        self.line_capacity = QLineEdit(self.edit_widget)
        self.line_capacity.setGeometry(120, 30, 150, 30)
        self.line_capacity.setPlaceholderText("Вместительность")

        self.label_color = QLabel("Цвет:", self.edit_widget)
        self.label_color.setGeometry(280, 5, 150, 25)
        self.label_color.hide()

        self.line_color = QLineEdit(self.edit_widget)
        self.line_color.setGeometry(280, 30, 150, 30)
        self.line_color.hide()

        self.label_name = QLabel("Название:", self.edit_widget)
        self.label_name.setGeometry(280, 5, 150, 25)
        self.label_name.hide()

        self.line_name = QLineEdit(self.edit_widget)
        self.line_name.setGeometry(280, 30, 150, 30)
        self.line_name.hide()

        btn_save = QPushButton("Сохранить", self.edit_widget)
        btn_save.setGeometry(450, 30, 100, 30)
        btn_save.clicked.connect(self.on_save)

        btn_cancel = QPushButton("Отмена", self.edit_widget)
        btn_cancel.setGeometry(560, 30, 100, 30)
        btn_cancel.clicked.connect(self.cancel_edit)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(660, 550, 120, 40)
        btn_close.clicked.connect(self.close)

        self.current_index = None
        self.current_vehicle = None

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


    def load_vehicles(self, company):
        self.company = company
        vehicles_list = company.vehicles if hasattr(company, 'vehicles') else []
        self.table.setRowCount(0)
        for idx, vehicle in enumerate(vehicles_list):
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(vehicle.vehicle_id))
            self.table.setItem(row, 1, QTableWidgetItem(vehicle.__class__.__name__))
            self.table.setItem(row, 2, QTableWidgetItem(str(vehicle.capacity)))
            self.table.setItem(row, 3, QTableWidgetItem(str(vehicle.current_load)))
            
            if isinstance(vehicle, Truck):
                self.table.setItem(row, 4, QTableWidgetItem(vehicle.color))
                self.table.setItem(row, 5, QTableWidgetItem("-"))
            elif isinstance(vehicle, Ship):
                self.table.setItem(row, 4, QTableWidgetItem("-"))
                self.table.setItem(row, 5, QTableWidgetItem(vehicle.name))
            else:
                self.table.setItem(row, 4, QTableWidgetItem("-"))
                self.table.setItem(row, 5, QTableWidgetItem("-"))

    def on_cell_double_clicked(self, row, column):
        if self.company is None:
            return

        vehicles_list = self.company.vehicles if hasattr(self.company, 'vehicles') else []
        if row < len(vehicles_list):
            self.current_index = row
            vehicle = vehicles_list[row]
            self.load_vehicle(vehicle, row)
            self.edit_widget.show()

    def load_vehicle(self, vehicle, index):
        self.current_index = index
        self.current_vehicle = vehicle

        self.label_type_value.setText(vehicle.__class__.__name__)
        self.line_capacity.setText(str(vehicle.capacity))

        if isinstance(vehicle, Truck):
            self.label_color.show()
            self.line_color.show()
            self.label_name.hide()
            self.line_name.hide()
            self.line_color.setText(vehicle.color)
        elif isinstance(vehicle, Ship):
            self.label_color.hide()
            self.line_color.hide()
            self.label_name.show()
            self.line_name.show()
            self.line_name.setText(vehicle.name)

    def cancel_edit(self):
        self.edit_widget.hide()
        self.current_index = None
        self.current_vehicle = None

    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        if field:
            field.clear()

    def on_save(self):
        if self.current_index is None or self.company is None or self.current_vehicle is None:
            return

        capacity_text = self.line_capacity.text().strip()
        try:
            capacity = float(capacity_text)
            if capacity <= 0:
                self.show_warning("Вместительность должна быть больше 0", self.line_capacity)
                return
        except ValueError:
            self.show_warning("Вместительность должна быть числом", self.line_capacity)
            return

        vehicles_list = self.company.vehicles if hasattr(self.company, 'vehicles') else []
        if self.current_index >= len(vehicles_list):
            return

        vehicles_list[self.current_index].capacity = capacity

        if isinstance(self.current_vehicle, Truck):
            color = self.line_color.text().strip()
            if not color:
                self.show_warning("Цвет грузовика не может быть пустым", self.line_color)
                return
            vehicles_list[self.current_index].color = color
            self.table.setItem(self.current_index, 2, QTableWidgetItem(str(capacity)))
            self.table.setItem(self.current_index, 4, QTableWidgetItem(color))

        elif isinstance(self.current_vehicle, Ship):
            name = self.line_name.text().strip()
            if not name:
                self.show_warning("Название судна не может быть пустым", self.line_name)
                return
            vehicles_list[self.current_index].name = name
            self.table.setItem(self.current_index, 2, QTableWidgetItem(str(capacity)))
            self.table.setItem(self.current_index, 5, QTableWidgetItem(name))

        self.vehicle_changed.emit(self.current_index, vehicles_list[self.current_index])

        self.edit_widget.hide()
        self.current_index = None
        self.current_vehicle = None
        QMessageBox.information(self, "Успех", "Транспорт успешно изменен")

class AddVehicle(QMainWindow):
    vehicle_added = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить транспорт")
        self.setFixedSize(500, 250)

        central = QWidget()
        self.setCentralWidget(central)

        self.combo = QComboBox(central)
        self.combo.setGeometry(50, 50, 140, 30)
        self.combo.addItems(["Грузовик", "Судно"])

        self.line_capacity = QLineEdit(central)
        self.line_capacity.setPlaceholderText("Введите вместительность")
        self.line_capacity.setGeometry(50, 100, 375, 30)

        self.line_name = QLineEdit(central)
        self.line_name.setPlaceholderText("Введите имя")
        self.line_name.setGeometry(50, 150, 375, 30)

        self.line_color = QLineEdit(central)
        self.line_color.setPlaceholderText("Введите цвет")
        self.line_color.setGeometry(50, 150, 375, 30)
        self.line_color.hide()

        btn = QPushButton("Добавить", central)
        btn.setGeometry(50, 200, 120, 40)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(330, 200, 120, 40)
        btn_close.clicked.connect(self.close)

        btn.clicked.connect(self.on_add_vehicle)
        self.combo.currentTextChanged.connect(self.on_combo_changed)
        self.on_combo_changed(self.combo.currentText())

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def clear_fields(self):
        self.line_capacity.clear()
        self.line_name.clear()
        self.line_color.clear()
        self.combo.setCurrentIndex(0)
        self.on_combo_changed(self.combo.currentText())

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        self.clear_fields()

    def on_combo_changed(self, text):
        if text == "Грузовик":
            self.line_name.hide()
            self.line_name.clear()
            self.line_color.show()
        elif text == "Судно":
            self.line_color.hide()
            self.line_color.clear()
            self.line_name.show()

    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        field.clear()

    def on_add_vehicle(self):
        capacity_text = self.line_capacity.text().strip()
        try:
            capacity = float(capacity_text)
        except ValueError:
            self.show_warning("Вместимость должна быть числом", self.line_capacity)
            return

       
        if self.combo.currentText() == "Грузовик":
            if not self.line_color.text().strip():
                self.show_warning("Цвет грузовика не может быть пустым", self.line_color)
                return
            vehicle = Truck(capacity, self.line_color.text().strip())
        else:
            if not self.line_name.text().strip():
                self.show_warning("Имя судна не может быть пустым", self.line_name)
                return
            vehicle = Ship(capacity, self.line_name.text().strip())

        self.vehicle_added.emit(vehicle)
        self.clear_fields()
        self.close()


class AboutWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("О программе")
        self.setFixedSize(350, 250)

        central = QWidget()
        self.setCentralWidget(central)

        lb_lr = QLabel("Лабораторная 13", central)
        lb_lr.setStyleSheet("QLabel { border: 1px solid #808080; border-radius: 4px; background-color: #ffffff; padding: 8px; }")
        lb_lr.setGeometry(20, 20, 150, 40)

        lb_var = QLabel("Вариант 2", central)
        lb_var.setStyleSheet("QLabel { border: 1px solid #808080; border-radius: 4px; background-color: #ffffff; padding: 8px; }")
        lb_var.setGeometry(20, 80, 150, 40)

        lb_name = QLabel("Лоел 89 ТП", central)
        lb_name.setStyleSheet("QLabel { border: 1px solid #808080; border-radius: 4px; background-color: #ffffff; padding: 8px; }")
        lb_name.setGeometry(20, 140, 150, 40)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(20, 190, 140, 40)
        btn_close.clicked.connect(self.close)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    
    app.setStyleSheet("""
        QWidget {
            background-color: #f5f5f5;
            color: #1a1a1a;
            font-size: 13px;
        }
        
        QPushButton {
            background-color: white;
            border: 1px solid #b0b0b0;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover { background-color: #e8e8e8; }
        QPushButton:pressed { background-color: #d0d0d0; }
        
        QLineEdit, QComboBox {
            background-color: white;
            border: 1px solid #b0b0b0;
            border-radius: 4px;
            padding: 4px 8px;
        }
        QLineEdit:focus, QComboBox:hover { border-color: #606060; }
        
        QTableWidget {
            background-color: white;
            border: 1px solid #b0b0b0;
            border-radius: 4px;
        }
        QTableWidget::item:selected { background-color: #d0d0d0; }
        
        QHeaderView::section {
            background-color: #e0e0e0;
            border: none;
            border-bottom: 1px solid #b0b0b0;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #808080;
            border-radius: 3px;
            background-color: white;
        }
        QCheckBox::indicator:checked { background-color: #00FF00; }
        
        QStatusBar {
            background-color: #e0e0e0;
            border-top: 1px solid #a0a0a0;
        }
        
        QScrollBar:vertical, QScrollBar:horizontal {
            background-color: #f0f0f0;
            border-radius: 6px;
        }
        QScrollBar::handle {
            background-color: #c0c0c0;
            border-radius: 6px;
            min-height: 30px;
            min-width: 30px;
        }
        QScrollBar::handle:hover { background-color: #a0a0a0; }
    """)
    
    window = MainWindow()
    window.show()
    app.exec()