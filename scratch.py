import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import qdarkstyle
from qdarkstyle.dark.palette import DarkPalette
from qdarkstyle.light.palette import LightPalette


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QDarkStyle Switch Example")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建Matplotlib图表并设置背景为透明
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.fig.patch.set_alpha(0.0)  # 设置图表背景为透明
        self.ax.patch.set_alpha(0.0)  # 设置轴区域背景为透明

        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # 添加切换按钮
        self.switch_button = QPushButton("Switch Theme")
        self.switch_button.clicked.connect(self.switch_theme)
        layout.addWidget(self.switch_button)

        # 设置 FigureCanvas 的父级部件背景为透明
        self.canvas.setStyleSheet("background:transparent;")
        self.canvas.setAttribute(Qt.WA_TranslucentBackground, True)

        # 确保主窗口的背景颜色也是透明的
        central_widget.setStyleSheet("background:transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.plot()

        # 初始设置为 LightPalette
        self.is_dark_theme = False
        self.apply_theme()

    def plot(self):
        self.ax.plot([0, 1, 2, 3], [0, 1, 4, 9], 'r-')
        self.canvas.draw()

    def switch_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet(qdarkstyle.load_stylesheet(palette=DarkPalette))
        else:
            self.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
