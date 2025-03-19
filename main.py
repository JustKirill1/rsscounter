import sys
import pyautogui
import pytesseract
from PIL import Image
import re
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
import pygetwindow as gw
import configparser
import os
import csv_saver
from graph import GraphWindow, load_data
# Путь к файлу setting.ini
SETTINGS_FILE = "setting.ini"

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
        save_tax_to_ini(self.name, new_tax)


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


def load_tax_from_ini(account_name):
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)
    if "Taxes" in config and account_name in config["Taxes"]:
        return float(config["Taxes"][account_name])
    return 1.0  # Значение по умолчанию, если налог не найден


def save_tax_to_ini(account_name, tax_rate):
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)
    if "Taxes" not in config:
        config["Taxes"] = {}
    config["Taxes"][account_name] = str(tax_rate)
    with open(SETTINGS_FILE, "w") as configfile:
        config.write(configfile)


class ResourceApp(QtWidgets.QWidget):
    def __init__(self, window_title):
        super().__init__()
        self.window_title = window_title
        self.initUI()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon('Media/UI/prog_icon.png'))
        self.setWindowTitle("Resource Manager")
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
        self.account_selector.addItems(
            ["JustKirill", "KirillFarm0", "KirillFarm1", "KirillFarm2", "KirillFarm3", "KirillFarm4"])
        self.account_selector.setStyleSheet("""
               QComboBox {
                   background-color: #3a3a3a;  /* Темный фон */
                   color: #f5f5f5;             /* Белый текст */
                   border: 2px solid #4a90e2;  /* Синяя рамка */
                   border-radius: 8px;         /* Закругленные углы */
                   padding: 5px;               /* Отступы */
                   font-size: 14px;            /* Размер шрифта */
               }
               QComboBox::drop-down {
                   background-color: #2a2a2a;  /* Темный фон для стрелки */
                   border: 2px solid #4a90e2;  /* Синяя рамка */
                   border-radius: 5px;         /* Закругленные углы */
                   width: 20px;               /* Ширина стрелки */
               }
               QComboBox::down-arrow {
                   image: url(Media/UI/down_arrow.svg);  /* Иконка стрелки */
                   width: 10px;
                   height: 10px;
               }
               QComboBox QAbstractItemView {
                   background-color: #3a3a3a;  /* Темный фон выпадающего списка */
                   color: #f5f5f4;             /* Белый текст */
                   selection-background-color: #4a90e2;  /* Синий фон выбранного элемента */
                   selection-color: #ffffff;   /* Белый текст выбранного элемента */
                   border: 2px solid #4a90e2;  /* Синяя рамка */
               }
           """)

        # Кнопки
        self.screenshot_button = QtWidgets.QPushButton(self)
        self.screenshot_button.setIcon(QtGui.QIcon("Media/UI/screenshot.png"))
        self.screenshot_button.clicked.connect(self.take_screenshot)

        self.calculate_button = QtWidgets.QPushButton(self)
        self.calculate_button.setIcon(QtGui.QIcon("Media/UI/calculate.png"))
        self.calculate_button.clicked.connect(self.calculate_resources)

        self.tax_button = QtWidgets.QPushButton(self)
        self.tax_button.setIcon(QtGui.QIcon("Media/UI/tax.png"))
        self.tax_button.clicked.connect(self.change_tax)

        self.reset_button = QtWidgets.QPushButton(self)
        self.reset_button.setIcon(QtGui.QIcon("Media/UI/reset.png"))
        self.reset_button.clicked.connect(self.reset_resources)

        self.graph_button = QtWidgets.QPushButton(self)
        self.graph_button.setIcon(QtGui.QIcon("Media/UI/graph.png"))  # Иконка для кнопки
        self.graph_button.clicked.connect(self.open_graphs)
        self.graph_button.setToolTip("Открыть графики ресурсов")

        # Настройка размера кнопок
        button_size = QtCore.QSize(64, 64)  # Размер кнопок
        for button in [self.screenshot_button, self.calculate_button, self.tax_button, self.reset_button, self.graph_button]:
            button.setIconSize(button_size)
            button.setFixedSize(button_size)

        # Используем QGridLayout для расположения элементов
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.account_selector, 0, 0, 1, 2)  # Выпадающий список на всю ширину
        layout.addWidget(self.screenshot_button, 1, 0)
        layout.addWidget(self.calculate_button, 1, 1)
        layout.addWidget(self.tax_button, 2, 0)
        layout.addWidget(self.reset_button, 2, 1)
        layout.addWidget(self.graph_button, 3, 0)

        self.setLayout(layout)

        # Прозрачность и закрепление окна
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.75)

    def update_position(self):
        target_windows = gw.getWindowsWithTitle(self.window_title)
        if target_windows:
            target_window = target_windows[0]
            self.move(target_window.left + 5, target_window.top + int(target_window.height / 1.85))
            if not self.isVisible():
                self.show()

    def take_screenshot(self):
        # Загружаем изображение крестика (шаблон)
        cross_image = cv2.imread("Media/func/cross.png", cv2.IMREAD_GRAYSCALE)
        if cross_image is None:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Файл cross.png не найден или поврежден.")
            return

        # Делаем скриншот и преобразуем его в градации серого
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # Преобразуем в BGR (формат OpenCV)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)  # Преобразуем в градации серого

        # Ищем крестик на скриншоте
        result = cv2.matchTemplate(screenshot_gray, cross_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # Если уверенность совпадения высокая, обрезаем скриншот
        if max_val > 0.8:  # Порог уверенности (можно настроить)
            h, w = cross_image.shape
            cross_x, cross_y = max_loc

            # Определяем область для обрезки
            crop_x1 = cross_x - 1000  # Отступ от крестика
            crop_y1 = cross_y + 200  # Отступ от крестика
            crop_x2 = crop_x1 + 1000  # Ширина области
            crop_y2 = crop_y1 + 400  # Высота области

            # Проверяем, чтобы координаты не выходили за пределы изображения
            height, width = screenshot_gray.shape
            crop_x1 = max(0, crop_x1)
            crop_y1 = max(0, crop_y1)
            crop_x2 = min(width, crop_x2)
            crop_y2 = min(height, crop_y2)

            # Обрезаем скриншот
            cropped_screenshot = screenshot[crop_y1:crop_y2, crop_x1:crop_x2]
            cv2.imwrite("cropped_screenshot.png", cropped_screenshot)

            # Обрабатываем обрезанный скриншот
            resources = self.extract_resources("cropped_screenshot.png")

            # Отображаем распознанные ресурсы в QMessageBox
            resource_message = "\n".join(
                [f"{key.capitalize()}: {value / 1000000:.2f}М" for key, value in resources.items()])
            QtWidgets.QMessageBox.information(
                self,
                "Скриншот",
                f"Скриншот сохранен и обработан!\n\nРаспознанные ресурсы:\n{resource_message}"
            )

            # Добавляем ресурсы на аккаунт
            account_name = self.account_selector.currentText()
            for account in resource_manager.accounts:
                if account.name == account_name:
                    account.add_resources(resources["food"], resources["wood"], resources["stone"], resources["gold"])
                    print(f"Ресурсы добавлены на аккаунт {account_name}: {account.resources}")
                    break
        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Крестик не найден на скриншоте.")

    def extract_resources(self, image_path):
        try:
            # Открываем изображение
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Загружаем в градациях серого
            if image is None:
                print("Ошибка: Не удалось загрузить изображение.")
                return {"food": 0, "wood": 0, "stone": 0, "gold": 0}

            # Увеличиваем контрастность
            _, binary_image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

            # Сохраняем обработанное изображение для отладки
            cv2.imwrite("processed_screenshot.png", binary_image)

            # Распознаем текст с помощью pytesseract
            custom_config = r'--oem 3 --psm 6'  # Настройки для улучшения распознавания
            text = pytesseract.image_to_string(binary_image, config=custom_config, lang="eng")
            print("Распознанный текст:\n", text)

            # Если текст пустой, выводим предупреждение
            if not text.strip():
                print("Предупреждение: Текст на изображении не распознан.")
                return {"food": 0, "wood": 0, "stone": 0, "gold": 0}

            resources = {"food": 0, "wood": 0, "stone": 0, "gold": 0}
            lines = text.split("\n")
            resource_keys = {"Food": "food", "Wood": "wood", "Stone": "stone", "Gold": "gold"}

            # Обрабатываем строки
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Ищем название ресурса и числа в строке
                for key in resource_keys:
                    if key in line:
                        # Ищем числа в строке (например, "141.1M" или "382.5M")
                        numbers = re.findall(r"(\d+(?:\.\d+)?(?:M|K)?)", line)
                        if len(numbers) >= 2:  # Проверяем, что есть хотя бы два числа
                            # Берем второе число (например, "382.5M")
                            second_number = numbers[1]
                            try:
                                # Преобразуем число в float (учитываем "M" и "K")
                                if "M" in second_number:
                                    value = float(second_number.replace("M", "")) * 1_000_000
                                elif "K" in second_number:
                                    value = float(second_number.replace("K", "")) * 1_000
                                else:
                                    value = float(second_number)
                                resources[resource_keys[key]] = value
                            except ValueError as e:
                                print(f"Ошибка обработки числа в строке: {line}. Ошибка: {e}")
                        else:
                            print(f"Не найдено второе число в строке: {line}")

            print("Извлечённые ресурсы:", resources)
            return resources

        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")
            return {"food": 0, "wood": 0, "stone": 0, "gold": 0}

    def calculate_resources(self):
        resource_manager.update_total_resources()
        message = "\n".join(
            [f"{key.capitalize()}: {value / 1000000:.2f}М" for key, value in resource_manager.total_resources.items()])
        QtWidgets.QMessageBox.information(self, "Итоговые ресурсы", message)
        csv_saver.save_resources_to_csv(resource_manager)
    def change_tax(self):
        account_name = self.account_selector.currentText()
        current_tax = load_tax_from_ini(account_name)
        new_tax, ok = QtWidgets.QInputDialog.getDouble(self, "Изменение налога", "Введите новый налог:", current_tax, 0.1, 1.0, 2)
        if ok:
            for account in resource_manager.accounts:
                if account.name == account_name:
                    account.update_tax(new_tax)
                    QtWidgets.QMessageBox.information(self, "Налог", f"Налог для {account_name} изменен на {new_tax}")
                    break

    def reset_resources(self):
        resource_manager.reset_resources()
        QtWidgets.QMessageBox.information(self, "Сброс", "Ресурсы сброшены!")
    def open_graphs(self):
        """
        Открывает окно с графиками ресурсов.
        """
        # Загружаем данные
        df = load_data()

        # Создаем окно с графиками
        self.graph_window = GraphWindow(df)
        self.graph_window.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    resource_manager = ResourceManager()

    # Загружаем налоги из setting.ini
    for name in ["JustKirill", "KirillFarm0", "KirillFarm1", "KirillFarm2", "KirillFarm3", "KirillFarm4"]:
        tax_rate = load_tax_from_ini(name)
        resource_manager.add_account(Account(name, tax_rate))

    window_title = "Rise of Kingdoms"
    ex = ResourceApp(window_title)
    ex.show()
    sys.exit(app.exec_())