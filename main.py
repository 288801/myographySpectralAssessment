import sys
import numpy as np
import matplotlib.pyplot as plt
import pywt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 200, 850, 180)
        self.setFixedSize(1050, 160)
        my_label = QLabel("Спектральная оценка миографии методом вейвлет")
        my_label.setFont(QFont('Serif', 24))
        my_label.setGeometry(40, -20, 950, 100)
        self.layout().addWidget(my_label)

        # Создаем кнопки
        self.button_load = QPushButton('Загрузить из файла', self)
        self.button_load.setGeometry(50, 100, 200, 30)
        self.button_load.clicked.connect(self.load_file)

        self.button_rr = QPushButton('Показать исходный график', self)
        self.button_rr.setGeometry(300, 100, 200, 30)
        self.button_rr.clicked.connect(self.plot)

        self.button_hf = QPushButton('Вейвлет спектрограмма', self)
        self.button_hf.setGeometry(550, 100, 200, 30)
        self.button_hf.clicked.connect(self.plot_wave)

        self.button_hf = QPushButton('Усредненный вейвлет спектр', self)
        self.button_hf.setGeometry(800, 100, 200, 30)
        self.button_hf.clicked.connect(self.plot_spec)

        # Создаем переменные для хранения данных
        self.filename = None
        self.data = None
        self.t = None
        self.cwtmatr = None
        self.freqs = None

    def load_file(self):
        # Открываем диалоговое окно для выбора файла
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '', '(*.asc)')

        if self.filename:
            # Считываем данные из файла
            self.data = np.loadtxt(self.filename)

            # Преобразуем данные в массив RR интервалов
            self.t = np.linspace(0, 1, len(self.data))
            self.cwtmatr, self.freqs = pywt.cwt(self.data, np.arange(1, 100), 'mexh', 1/200)

            # for i in range(len(self.freqs)):
            #     self.freqs[i] = self.freqs[i]*1000 + 10

    def plot(self):
        plt.plot(self.t, self.data, label="Исходный сигнал")
        plt.xlabel('Отсчеты (шт)')
        plt.show()

    def plot_wave(self):
        plt.imshow(abs(self.cwtmatr), extent=[0, len(self.data), self.freqs[-1], self.freqs[0]], cmap='viridis', aspect='auto',
                   label="Спокойное состояние")
        plt.colorbar()
        plt.xlabel('Отсчеты (шт)')
        plt.ylabel('Частота [Гц]')
        plt.show()

    def plot_spec(self):
        coeffs = list()
        for i in range(len(self.cwtmatr)):
            count = 0
            for j in range(len(self.cwtmatr[0])):
                count += abs(self.cwtmatr[i][j])
            coeffs.append(count / len(self.cwtmatr[0]))
        plt.plot(self.freqs, coeffs, label="Усредненный вейвлет спектр")
        plt.xlabel('Частота [Гц]')
        plt.show()


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
