import sys

import numpy as np
import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets

from display.ingenuityDisplay import VehicleDisplay
from display.plotter import Plotter
from display.slider import Slider
from model.states import VehicleState

class IngenuityWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("INGENUITY SIMULATION")
        self.simulationPaused = True # begin with a paused simulation
        self.time = 0 # simulation time

        ### ~~~ pyqt6 application window --- ###
        self.setStyleSheet("background-color: white;")

        ### --- main widget --- ###
        # this is the widget that takes the entire screen
        mainWidget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

        # left side contains the canvas and simulation control
        leftWidget = QtWidgets.QWidget()
        leftLayout = QtWidgets.QVBoxLayout()
        leftWidget.setLayout(leftLayout)

        # contains the tabs with different plots
        rightWidget = QtWidgets.QTabWidget()

        ### --- vehicle widget --- ###
        self.vehicleWidget = VehicleDisplay()
        self.vehicleState = VehicleState()

        ### --- control sliders --- ###
        controlSlidersWidget = QtWidgets.QWidget()
        controlSlidersLayout = QtWidgets.QGridLayout()

        self.fxSlider = Slider(label="Fx", minVal=-10, maxVal=10, initVal=0, orientation=1);
        self.fySlider = Slider(label="Fy", minVal=-10, maxVal=10, initVal=0, orientation=1);
        self.fzSlider = Slider(label="Fz", minVal=-10, maxVal=10, initVal=0, orientation=1);

        self.pnSlider = Slider(label="pn", minVal=-10, maxVal=10, initVal=0, orientation=1); self.pnSlider.valueChangedSignal.connect(self.updateSim)
        self.peSlider = Slider(label="pe", minVal=-10, maxVal=10, initVal=0, orientation=1); self.peSlider.valueChangedSignal.connect(self.updateSim)
        self.pdSlider = Slider(label="pd", minVal=-10, maxVal=10, initVal=0, orientation=1); self.pdSlider.valueChangedSignal.connect(self.updateSim)

        self.rollSlider = Slider(label="roll", minVal=-180, maxVal=180, initVal=0, orientation=1);      self.rollSlider.valueChangedSignal.connect(self.updateSim)
        self.pitchSlider = Slider(label="pitch", minVal=-180, maxVal=180, initVal=0, orientation=1);    self.pitchSlider.valueChangedSignal.connect(self.updateSim)
        self.yawSlider = Slider(label="yaw", minVal=-180, maxVal=180, initVal=0, orientation=1);        self.yawSlider.valueChangedSignal.connect(self.updateSim)

        controlSlidersLayout.addWidget(self.pnSlider, 0, 0); controlSlidersLayout.addWidget(self.peSlider, 0, 1); controlSlidersLayout.addWidget(self.pdSlider, 0, 2)
        controlSlidersLayout.addWidget(self.rollSlider, 1, 0); controlSlidersLayout.addWidget(self.pitchSlider, 1, 1); controlSlidersLayout.addWidget(self.yawSlider, 1, 2)

        for i in range(3):
            controlSlidersLayout.setColumnStretch(i, 1)
        for i in range(2):
            controlSlidersLayout.setRowStretch(i, 1)

        controlSlidersWidget.setLayout(controlSlidersLayout)

        ### --- states tab --- ###
        statesWidget = QtWidgets.QWidget()
        statesLayout = QtWidgets.QGridLayout()
        statesWidget.setLayout(statesLayout)

        self.pnPlot = Plotter("Position North", "", "Position [m]")
        self.pePlot = Plotter("Position East", "", "Position [m]")
        self.pdPlot = Plotter("Altitude", "", "Position [m]")

        self.yawPlot = Plotter("Yaw", "", "Yaw [deg]")
        self.pitchPlot = Plotter("Pitch", "", "Pitch [deg]")
        self.rollPlot = Plotter("Roll", "", "Roll [deg]")

        statesLayout.addWidget(self.pnPlot, 0, 0); statesLayout.addWidget(self.pePlot, 0, 1); statesLayout.addWidget(self.pdPlot, 0, 2)
        statesLayout.addWidget(self.yawPlot, 1, 0); statesLayout.addWidget(self.pitchPlot, 1, 1); statesLayout.addWidget(self.rollPlot, 1, 2)
        
        ### --- add widgets to the main layout --- ###
        leftLayout.addWidget(self.vehicleWidget)
        leftLayout.addWidget(controlSlidersWidget)
        leftLayout.addWidget(self.vehicleWidget, stretch=3)
        leftLayout.addWidget(controlSlidersWidget, stretch=1)

        rightWidget.addTab(statesWidget, "States")
        
        layout.addWidget(leftWidget, stretch=2)
        layout.addWidget(rightWidget, stretch=3)

        self.vehicleWidget.setMinimumSize(200, 200)

        self.resize(1200, 800)

    def updateSim(self, newValue) -> None:
        self.time += 1

        # update the plots
        self.pnPlot.updatePlotSignal.emit(self.time, [self.pnSlider.getSliderValue()])
        self.pePlot.updatePlotSignal.emit(self.time, [self.peSlider.getSliderValue()])
        self.pdPlot.updatePlotSignal.emit(self.time, [self.pdSlider.getSliderValue()])

        self.yawPlot.updatePlotSignal.emit(self.time, [self.yawSlider.getSliderValue()])
        self.pitchPlot.updatePlotSignal.emit(self.time, [self.pitchSlider.getSliderValue()])
        self.rollPlot.updatePlotSignal.emit(self.time, [self.rollSlider.getSliderValue()])

        # update the vehicle
        self.vehicleWidget.updateVehicle(self.pnSlider.getSliderValue(), self.peSlider.getSliderValue(), self.pdSlider.getSliderValue(),
                                         self.yawSlider.getSliderValue()*np.pi/180.0, self.pitchSlider.getSliderValue()*np.pi/180.0, self.rollSlider.getSliderValue()*np.pi/180.0)
        return None

def main():
    ingenuityApp = QtWidgets.QApplication(sys.argv)
    window = IngenuityWindow()
    window.show()
    sys.exit(ingenuityApp.exec())

if __name__ == "__main__":
    main()