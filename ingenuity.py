import sys

import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets

from constants.simulationConstants import (window_width, window_height)
from display.VehicleDisplay import VehicleDisplay

class IngenuityWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("INGENUITY SIMULATION")
        self.simulationPaused = True # begin with a paused simulation

        ### ~~~ pyqt6 application window --- ###
        self.setGeometry(50, 50, window_width, window_height)
        self.setStyleSheet("background-color: grey;")

        ### --- main widget --- ###
        # this is the widget that takes the entire screen and is split in cells
        mainWidget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

        ### --- vehicle widget --- ###
        self.vehicleWidget = VehicleDisplay()
        layout.addWidget(self.vehicleWidget, 0, 0)


def main():
    ingenuityApp = QtWidgets.QApplication(sys.argv)
    window = IngenuityWindow()
    window.show()
    sys.exit(ingenuityApp.exec())

if __name__ == "__main__":
    main()