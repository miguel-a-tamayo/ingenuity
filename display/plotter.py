"""
Author: Miguel Tamayo

plotter.py
Contains class for PyQtGraph widget
"""

from PyQt6.QtCore import pyqtSignal

from constants.simulationConstants import (plotBlue, plotGreen, plotRed, plotWhite, plotBlack, plotGrey)

import pyqtgraph as pg

class Plotter(pg.PlotWidget):
    """
    Class representing PyQtGraph plot widget

    :param title: plot title
    :param xLabel: x-axis label
    :param yLabel: y-axis label
    :param numLines: number of lines to be drawn on the plot
    :param legends: list of legend names for lines
    """

    updatePlotSignal = pyqtSignal(float, list) # signal that will trigger a plot update
    def __init__(self,
                 title: str,
                 xLabel: str,
                 yLabel: str,
                 numPlots: int = 1,
                 legends: list = None) -> None:
        super().__init__(parent=None)

        self.lineColors = [plotBlue, plotRed, plotGreen]
        self.x = []
        self.dataSets = []
        self.plotLines = []

        # figure attributes
        self.setBackground(plotWhite)
        # self.setFixedSize(275, 350)

        # plot attributes
        self.plotItem = self.getPlotItem()
        self.plotItem.setTitle(title, color=plotBlack)
        self.plotItem.setLabel(axis='bottom', text=xLabel, color=plotBlack)
        self.plotItem.setLabel(axis='left', text=yLabel, color=plotBlack)
        self.plotItem.showGrid(x=True, y=True)
        self.plotItem.getAxis('bottom').setTextPen('k')
        self.plotItem.getAxis('left').setTextPen('k')

        if legends:
            self.plotItem.addLegend(labelTextColor=plotBlack, brush=plotGrey)

        # itereate over the number of lines and add a plot isntance
        for idx in range(numPlots):
            self.dataSets.append([]) # append a list for this line set
            if legends:
                self.plotLines.append(self.plotItem.plot(name=legends[idx], pen=pg.mkPen(self.lineColors[idx])))
            else:
                self.plotLines.append(self.plotItem.plot(pen=pg.mkPen(self.lineColors[idx])))
        
        self.updatePlotSignal.connect(self.updatePlot)
    
    def updatePlot(self, x: float, newData: list) -> None:
        """
        Adds new data to the plot

        :param x: x-axis value
        :param newData: y-axis value for each line to be plotted
        """

        self.x.append(x) # add x point
        for dataSet, plotLine, dataPoint in zip(self.dataSets, self.plotLines, newData):
            dataSet.append(dataPoint) # append the data to its corresponding list
            plotLine.setData(self.x, dataSet) # update the plot
        
        return None
    
    def resetPlot(self) -> None:
        """
        Clears all the plots and erases the stored data
        """

        self.x.clear()
        for dataSet, plotLine in zip(self.dataSets, self.plotLines):
            dataSet.clear()
            plotLine.setData(self.x, dataSet)

        return None