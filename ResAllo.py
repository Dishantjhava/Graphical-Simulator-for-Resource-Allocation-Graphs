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
    def initUI(self):
        self.setWindowTitle("Resource Allocation Graph Simulator")
        self.setGeometry(100, 100, 800, 600)
        
        self.button_add_process = QPushButton("Add Process", self)
        self.button_add_resource = QPushButton("Add Resource", self)
        self.button_allocate = QPushButton("Allocate Resource", self)
        self.button_request = QPushButton("Request Resource", self)
        self.button_release = QPushButton("Release Resource", self)
        self.button_check_deadlock = QPushButton("Check Deadlock", self)
        
        self.button_add_process.clicked.connect(self.add_process)
        self.button_add_resource.clicked.connect(self.add_resource)
        self.button_allocate.clicked.connect(self.allocate_resource)
        self.button_request.clicked.connect(self.request_resource)
        self.button_release.clicked.connect(self.release_resource)
        self.button_check_deadlock.clicked.connect(self.detect_deadlock)
        
        layout = QVBoxLayout()
        layout.addWidget(self.button_add_process)
        layout.addWidget(self.button_add_resource)
        layout.addWidget(self.button_allocate)
        layout.addWidget(self.button_request)
        layout.addWidget(self.button_release)
        layout.addWidget(self.button_check_deadlock)
        layout.addWidget(self.canvas)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    def add_process(self):
        process_id, ok = QInputDialog.getText(self, "Add Process", "Enter process ID (e.g., P1):")
        if ok and process_id and process_id not in self.graph:
            self.graph.add_node(process_id, type='process')
            self.draw_graph()
    def add_resource(self):
        resource_id, ok1 = QInputDialog.getText(self, "Add Resource", "Enter resource ID (e.g., R1):")
        capacity, ok2 = QInputDialog.getInt(self, "Resource Capacity", "Enter maximum capacity:", min=1)
        if ok1 and ok2 and resource_id and resource_id not in self.graph:
            self.graph.add_node(resource_id, type='resource')
            self.resource_capacities[resource_id] = capacity
            self.resource_allocations[resource_id] = 0
            self.draw_graph()
