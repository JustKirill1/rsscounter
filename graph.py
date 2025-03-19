import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphWindow(QtWidgets.QWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.initUI()

    def initUI(self):
        # Создаем вкладки
        self.tabs = QtWidgets.QTabWidget(self)

        # График для Food
        self.tab1 = QtWidgets.QWidget()
        self.add_graph_to_tab(self.tab1, "Food", "Итого_food")
        self.tabs.addTab(self.tab1, "Food")

        # График для Wood
        self.tab2 = QtWidgets.QWidget()
        self.add_graph_to_tab(self.tab2, "Wood", "Итого_wood")
        self.tabs.addTab(self.tab2, "Wood")

        # График для Stone
        self.tab3 = QtWidgets.QWidget()
        self.add_graph_to_tab(self.tab3, "Stone", "Итого_stone")
        self.tabs.addTab(self.tab3, "Stone")

        # График для Gold
        self.tab4 = QtWidgets.QWidget()
        self.add_graph_to_tab(self.tab4, "Gold", "Итого_gold")
        self.tabs.addTab(self.tab4, "Gold")

        # Основной layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def add_graph_to_tab(self, tab, title, column):
        """
        Добавляет график на вкладку.
        :param tab: Вкладка, на которую добавляется график.
        :param title: Заголовок графика.
        :param column: Столбец данных для построения графика.
        """
        # Создаем фигуру и оси
        figure = Figure()
        axes = figure.add_subplot(111)

        # Строим график
        axes.plot(self.df["Дата"], self.df[column], label=title)
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
    df["Итого_food"] = df["Итого"].apply(lambda x: float(x.split(";")[0]))
    df["Итого_wood"] = df["Итого"].apply(lambda x: float(x.split(";")[1]))
    df["Итого_stone"] = df["Итого"].apply(lambda x: float(x.split(";")[2]))
    df["Итого_gold"] = df["Итого"].apply(lambda x: float(x.split(";")[3]))

    return df


if __name__ == "__main__":
    # Загружаем данные
    df = load_data()

    # Создаем приложение
    app = QtWidgets.QApplication(sys.argv)

    # Создаем окно с графиками
    window = GraphWindow(df)
    window.setWindowTitle("Графики ресурсов")
    window.resize(800, 600)
    window.show()

    # Запускаем приложение
    sys.exit(app.exec_())