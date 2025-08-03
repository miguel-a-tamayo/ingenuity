"""
Author: Miguel Tamayo

slider.py
Contains class for PyQt5 slider widget
"""

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont

class Slider(QWidget):
    """
    Class representing PyQt6 slider widget with lables and values

    :param min_val:         slider's minimum value
    :param max_val:         slider's maximum value
    :param initVal:         slider's initial value
    :param tickInterval:    slider's ticks
    :param orientation:     1 -> horizontal; 0 -> vertical
    """

    valueChangedSignal = pyqtSignal(float)

    def __init__(self,
                 label: str,
                 minVal: int,
                 maxVal: int,
                 initVal: float = 0,
                 orientation: int = 1) -> None:
        super().__init__(parent = None)

        self.initVal = initVal
        self.minVal = minVal
        self.maxVal = maxVal

        self.ticksMax = 1000
        self.ticksMin = 0

        self.ratio = (self.maxVal - self.minVal) / (self.ticksMax - self.ticksMin)

        layout = QHBoxLayout() # layout for the slider object

        # slider label
        layout.addWidget(QLabel(f"{label}"))

        self.valueTxt = QLabel()

        # slider object
        orientation = Qt.Orientation.Horizontal if orientation else Qt.Orientation.Vertical
        self.slider = QSlider(orientation=orientation)
        self.slider.setRange(self.ticksMin, self.ticksMax)
        self.slider.valueChanged.connect(self.updateValue)
        self.startTick = int((self.initVal - self.minVal) / self.ratio + self.ticksMin)
        self.slider.setValue(self.startTick)
        layout.addWidget(self.slider)

        # slider value text
        layout.addWidget(self.valueTxt)

        # set the widget's layout
        layout.addStretch()
        self.setLayout(layout)

        self.updateValue(self.startTick)
    
    def updateValue(self, newTick: int) -> None:
        """
        changes the displayed value on the slider and emmits a signal for any other outside updates

        :param value: new slider value
        """
        self.value = (float(newTick) - self.ticksMin) * self.ratio + self.minVal
        self.valueTxt.setText("{:.2f}".format(self.value))
        self.valueChangedSignal.emit(self.value)
    
    def resetSlider(self) -> None:
        """
        sets slider to the original position
        """
        self.slider.setValue(int(self.startTick))

    def getSliderValue(self) -> float:
        """
        wrapper function to get the slider's value

        :return value: slider's mapped value
        """

        return float(self.slider.value() - self.ticksMin) * self.ratio + self.minVal