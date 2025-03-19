import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphWindow(QtWidgets.QWidget):
    """
    Окно с вкладками для отображения графиков ресурсов.
    """
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.initUI()

    def initUI(self):
        # Создаем вкладки
        self.tabs = QtWidgets.QTabWidget(self)

        # Добавляем вкладки для каждого аккаунта
        accounts = ["JustKirill", "KirillFarm0", "KirillFarm1", "KirillFarm2", "KirillFarm3", "KirillFarm4"]
        for account in accounts:
            self.add_tab(account)

        # Добавляем вкладку для итоговых данных
        self.add_tab("Итого")

        # Основной layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # Настройка окна
        self.setWindowTitle("Графики ресурсов")
        self.resize(800, 600)

    def add_tab(self, account_name):
        """
        Добавляет вкладку с графиком для указанного аккаунта или итоговых данных.
        """
        # Создаем виджет для вкладки
        tab = QtWidgets.QWidget()
        self.tabs.addTab(tab, account_name)

        # Создаем фигуру и оси
        figure = Figure()
        axes = figure.add_subplot(111)

        # Строим график
        if account_name == "Итого":
            axes.plot(self.df["Дата"], self.df["Итого_food"], label="Food")
            axes.plot(self.df["Дата"], self.df["Итого_wood"], label="Wood")
            axes.plot(self.df["Дата"], self.df["Итого_stone"], label="Stone")
            axes.plot(self.df["Дата"], self.df["Итого_gold"], label="Gold")
            title = "Итоговые ресурсы"
        else:
            axes.plot(self.df["Дата"], self.df[f"{account_name}_food"], label="Food")
            axes.plot(self.df["Дата"], self.df[f"{account_name}_wood"], label="Wood")
            axes.plot(self.df["Дата"], self.df[f"{account_name}_stone"], label="Stone")
            axes.plot(self.df["Дата"], self.df[f"{account_name}_gold"], label="Gold")
            title = f"Ресурсы аккаунта: {account_name}"

        # Настройка графика
        axes.set_xlabel("Дата")
        axes.set_ylabel("Ресурсы (М)")
        axes.set_title(title)
        axes.legend()
        axes.grid()

        # Создаем холст для отображения графика
        canvas = FigureCanvas(figure)

        # Добавляем холст на вкладку
        layout = QtWidgets.QVBoxLayout(tab)
        layout.addWidget(canvas)
        tab.setLayout(layout)


def load_data():
    """
    Загружает данные из CSV-файла.
    """
    df = pd.read_csv("resources.csv", parse_dates=["Дата"], dayfirst=True)

    # Преобразуем данные для графиков
    accounts = ["JustKirill", "KirillFarm0", "KirillFarm1", "KirillFarm2", "KirillFarm3", "KirillFarm4"]
    for account in accounts:
        df[f"{account}_food"] = df[account].apply(lambda x: float(x.split(";")[0]))
        df[f"{account}_wood"] = df[account].apply(lambda x: float(x.split(";")[1]))
        df[f"{account}_stone"] = df[account].apply(lambda x: float(x.split(";")[2]))
        df[f"{account}_gold"] = df[account].apply(lambda x: float(x.split(";")[3]))

    # Итоговые ресурсы
    df["Итого_food"] = df["Итого"].apply(lambda x: float(x.split(";")[0]))
    df["Итого_wood"] = df["Итого"].apply(lambda x: float(x.split(";")[1]))
    df["Итого_stone"] = df["Итого"].apply(lambda x: float(x.split(";")[2]))
    df["Итого_gold"] = df["Итого"].apply(lambda x: float(x.split(";")[3]))

    return df


def main():
    # Загружаем данные
    df = load_data()

    # Создаем приложение
    app = QtWidgets.QApplication(sys.argv)

    # Создаем окно с вкладками
    window = GraphWindow(df)
    window.show()

    # Запускаем приложение
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()