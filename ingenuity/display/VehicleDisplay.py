"""
Author: Miguel Tamayo

ingenuityDisplay.py
displays the vehicle in an OpenGL window
"""

from PyQt6 import (QtCore, QtWidgets)
from pyqtgraph import (opengl, Vector)

from constants.simulationConstants import(openGL_window_height, openGL_window_width)

defaultZoom = 10
defaultAzimuth = 45
defaultElevation = 30

class VehicleDisplay(QtWidgets.QWidget):
    updatePositionSignal = QtCore.pyqtSignal(list)
    
    def __init__(self, parent = None):
        super().__init__(parent)

        widgetLayout = QtWidgets.QVBoxLayout()
        self.setLayout(widgetLayout)

        self.track = True # track ingenuity
        self.trail = True # trail that follows ingenuity

        self.lastPos = Vector(0, 0, 0)
        
        self.openGLWindow = opengl.GLViewWidget()
        self.openGLWindow.setGeometry(0, 0, openGL_window_width, openGL_window_height)
        grid = opengl.GLGridItem()
        grid.scale(100, 100, 1)
        grid.setSize(100, 100, 1)
        self.openGLWindow.addItem(grid)

        widgetLayout.addWidget(self.openGLWindow)
        
        # and an arbitrary camera starting position
        self.openGLWindow.setCameraPosition(distance=defaultZoom, elevation=defaultElevation, azimuth=defaultAzimuth)

        
