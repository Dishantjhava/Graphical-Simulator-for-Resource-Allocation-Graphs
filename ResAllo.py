import sys
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ResourceAllocationSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph = nx.DiGraph()
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)  # Initialize canvas before calling initUI()
        self.pos = {}
        self.resource_capacities = {}
        self.resource_allocations = {}

        self.initUI()