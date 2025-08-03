"""
Author: Miguel Tamayo

ingenuityDisplay.py
Displays the vehicle in an OpenGL window
"""

from PyQt6 import (QtCore, QtWidgets)
from pyqtgraph import (opengl, Vector)

from constants.simulationConstants import (openGL_window_width, openGL_window_height,
                                           defaultZoom, defaultElevation, defaultAzimuth,
                                           metersToPixel)
from model.ingenuityDraw import IngenuityDraw

import numpy as np


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
        # self.openGLWindow.setGeometry(0, 0, openGL_window_width, openGL_window_height)
    
        grid = opengl.GLGridItem()
        grid.scale(100, 100, 1)
        grid.setSize(100, 100, 1)
        self.openGLWindow.addItem(grid)

        widgetLayout.addWidget(self.openGLWindow)
        
        # and an arbitrary camera starting position
        self.openGLWindow.setCameraPosition(distance = defaultZoom,
                                            elevation = defaultElevation,
                                            azimuth = defaultAzimuth)

        ### --- draw the vehicle --- ###
        self.vehicleDrawing = IngenuityDraw() # copy of the vehicle
        
        # grab the vertices for the vehicle on each update
        vertices, axes, origin = self.vehicleDrawing.getNewPoints(0., 0., 0., 0., 0., 0.)
        newVertices = [[point * metersToPixel for point in vertex] for vertex in vertices]
        newVertices = np.array(newVertices)

        # faces and colors only need to be done once
        newFaces = np.array(self.vehicleDrawing.faces)
        newColors = np.array(self.vehicleDrawing.colors)

        # convert the vertices to meshdata which allows not to have to translate the points every time
        self.vehicleMesh = opengl.MeshData(vertexes = newVertices,
                                           faces = newFaces,
                                           faceColors = newColors)

        # create the mesh item
        self.openGLVehicle = opengl.GLMeshItem(meshdata = self.vehicleMesh,
                                               drawEdges = True,
                                               smooth = False,
                                               computeNormals = False)
        
        self.openGLWindow.addItem(self.openGLVehicle)

        ### --- draw the body axis --- ###
        newAxes = [[point * metersToPixel for point in vertex] for vertex in axes]
        self.enu_east = opengl.GLLinePlotItem(pos=np.array([origin, newAxes[0]]),
                                              color=(0, 1, 0, 1), width=2, antialias=True)

        self.enu_north = opengl.GLLinePlotItem(pos=np.array([origin, newAxes[1]]),
                                               color=(1, 0, 0, 1), width=2, antialias=True)

        self.enu_up = opengl.GLLinePlotItem(pos=np.array([origin, newAxes[2]]),
                                            color=(0, 0, 1, 1), width=2, antialias=True)

        # Add to OpenGL scene
        self.openGLWindow.addItem(self.enu_east)
        self.openGLWindow.addItem(self.enu_north)
        self.openGLWindow.addItem(self.enu_up)

    def updateVehicle(self, x: float, y: float, z: float, yaw: float, pitch: float, roll: float) -> None:
        """
        updates the vehicle position and attitude and draws the new vehicle

        :param x: new x position
        :param y: new y position
        :param z: new z position

        :param yaw: new yaw atittude
        :param pitch: new pitch attitude
        :param roll: new roll attitude
        """

        vertices, axes, origin = self.vehicleDrawing.getNewPoints(x, y, z, yaw, pitch, roll)
        newVertices = [[point * metersToPixel for point in vertex] for vertex in vertices]
        newOrigin = [point * metersToPixel for point in origin]
        newAxes = [[point * metersToPixel for point in vertex] for vertex in axes]

        self.vehicleMesh.setVertexes(newVertices) # update the mesh item
        self.openGLVehicle.setMeshData(meshdata=self.vehicleMesh, smooth=False, computeNormals=False)

        # update the axis of the vehicle
        self.enu_east.setData(pos=np.array([newOrigin, newAxes[0]]))
        self.enu_north.setData(pos=np.array([newOrigin, newAxes[1]]))
        self.enu_up.setData(pos=np.array([newOrigin, newAxes[2]]))
        return None
