from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import pyautogui
import pytesseract
from PIL import Image
import re


class Account:
    def __init__(self, name, tax_rate):
        self.name = name
        self.tax_rate = tax_rate
        self.resources = {"food": 0, "wood": 0, "stone": 0, "gold": 0}

    def add_resources(self, food, wood, stone, gold):
        self.resources["food"] += food * self.tax_rate
        self.resources["wood"] += wood * self.tax_rate
        self.resources["stone"] += stone * self.tax_rate
        self.resources["gold"] += gold * self.tax_rate

    def update_tax(self, new_tax):
        self.tax_rate = new_tax


class ResourceManager:
    def __init__(self):
        self.total_resources = {"food": 0, "wood": 0, "stone": 0, "gold": 0}
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def update_total_resources(self):
        for key in self.total_resources:
            self.total_resources[key] = sum(account.resources[key] for account in self.accounts)

    def reset_resources(self):
        for account in self.accounts:
            account.resources = {"food": 0, "wood": 0, "stone": 0, "gold": 0}
        self.total_resources = {"food": 0, "wood": 0, "stone": 0, "gold": 0}


class ResourceApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Resource Manager")
        self.setGeometry(100, 100, 400, 300)
        self.target_title = "Rise of Kingdoms"
        self.timer = QtCore.QTimer(self)
        # Colors and styles
        self.setStyleSheet("""
        QWidget {
            background-color: #2a2a2a;
        }
        QPushButton {
            background-color: #3a3a3a; 
            color: #f5f5f5;             
            border: 2px solid #4a90e2;  
            border-radius: 8px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #4a4a4a;  
            border: 2px solid #357ab2;  
        }
        QLabel {
            font-size: 16px;
            color: #f5f5f5;
            background-color: transparent;
            text-align: left !important;                
        }
        QComboBox {
            border: 2px solid #4a90e2; 
            border-radius: 8px;
            padding: 3px;
            font-size: 14px;
            background-color: #3a3a3a !important;
            color: white !important;
        }
        QComboBox::drop-down {
            background-color: #2a2a2a !important;
            border: 2px solid #4a90e2 !important;
            width: 10px;
            border-radius: 5px;
        }
        QComboBox::down-arrow {
            image: url(Media/UI/down_arrow.svg);
            padding-top: 2px;
            width: 10px;
            height: 10px;           
        }
        QCheckBox {
            font-size: 16px;
            color: #f5f5f5;
        }
        """)

        self.account_selector = QtWidgets.QComboBox(self)
        self.account_selector.addItems(["JustKirill", "FarmKirill", "KirillFarm1", "KirillFarm2"])

        self.screenshot_button = QtWidgets.QPushButton("Сделать скриншот", self)
        self.screenshot_button.clicked.connect(self.take_screenshot)

        self.calculate_button = QtWidgets.QPushButton("Посчитать ресурсы", self)
        self.calculate_button.clicked.connect(self.calculate_resources)

        self.tax_button = QtWidgets.QPushButton("Изменить налог", self)
        self.tax_button.clicked.connect(self.change_tax)

        self.reset_button = QtWidgets.QPushButton("Сбросить", self)
        self.reset_button.clicked.connect(self.reset_resources)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.account_selector)
        layout.addWidget(self.screenshot_button)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.tax_button)
        layout.addWidget(self.reset_button)
        self.setLayout(layout)

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        self.extract_resources("screenshot.png")
        QtWidgets.QMessageBox.information(self, "Скриншот", "Скриншот сохранен и обработан!")

    def extract_resources(self, image_path):
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang="eng")
        print("Распознанный текст:\n", text)

        resources = {"food": 0, "wood": 0, "stone": 0, "gold": 0}
        lines = text.split("\n")
        resource_keys = {"Food": "food", "Wood": "wood", "Stone": "stone", "Gold": "gold"}

        for line in lines:
            for key in resource_keys:
                if key in line:
                    numbers = re.findall(r"(\d+(\.\d+)?M?)", line)  # Ищем числа
                    if numbers:
                        last_number = numbers[-1][0]  # Берём последнее число
                        try:
                            value = float(last_number.replace("M", "")) * 1_000_000 if "M" in last_number else float(
                                last_number)
                            resources[resource_keys[key]] = value
                        except ValueError:
                            print(f"Ошибка обработки строки: {line}")
                    else:
                        print(f"Не найдено число в строке: {line}")

        print("Извлечённые ресурсы:", resources)

        account_name = self.account_selector.currentText()
        for account in resource_manager.accounts:
            if account.name == account_name:
                account.add_resources(resources["food"], resources["wood"], resources["stone"], resources["gold"])
                print(f"Ресурсы добавлены на аккаунт {account_name}: {account.resources}")
                break

    def calculate_resources(self):
        resource_manager.update_total_resources()
        message = "\n".join(
            [f"{key.capitalize()}: {value/1000000:.2f}M" for key, value in resource_manager.total_resources.items()])
        QtWidgets.QMessageBox.information(self, "Итоговые ресурсы", message)

    def change_tax(self):
        new_tax, ok = QtWidgets.QInputDialog.getDouble(self, "Изменение налога", "Введите новый налог:", 1.0, 0.1, 1.0,
                                                       2)
        if ok:
            account_name = self.account_selector.currentText()
            for account in resource_manager.accounts:
                if account.name == account_name:
                    account.update_tax(new_tax)
                    QtWidgets.QMessageBox.information(self, "Налог", f"Налог для {account_name} изменен на {new_tax}")
                    break

    def reset_resources(self):
        resource_manager.reset_resources()
        QtWidgets.QMessageBox.information(self, "Сброс", "Ресурсы сброшены!")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    resource_manager = ResourceManager()
    for name, rate in {"JustKirill": 1, "FarmKirill": 0.81, "KirillFarm1": 0.81, "KirillFarm2": 0.78}.items():
        resource_manager.add_account(Account(name, rate))
    ex = ResourceApp()
    ex.show()
    sys.exit(app.exec_())
