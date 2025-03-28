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
    def allocate_resource(self):
        process_id, ok1 = QInputDialog.getText(self, "Allocate Resource", "Enter process ID:")
        resource_id, ok2 = QInputDialog.getText(self, "Allocate Resource", "Enter resource ID:")
        if ok1 and ok2 and process_id in self.graph and resource_id in self.graph and self.graph.nodes[process_id]['type'] == 'process':
            if self.resource_allocations[resource_id] < self.resource_capacities[resource_id]:
                self.graph.add_edge(resource_id, process_id)
                self.resource_allocations[resource_id] += 1
            else:
                QMessageBox.warning(self, "Allocation Failed", f"Resource {resource_id} is fully allocated!")
        self.draw_graph()
    def request_resource(self):
        process_id, ok1 = QInputDialog.getText(self, "Request Resource", "Enter process ID:")
        resource_id, ok2 = QInputDialog.getText(self, "Request Resource", "Enter resource ID:")
        if ok1 and ok2 and process_id in self.graph and resource_id in self.graph:
            self.graph.add_edge(process_id, resource_id)
        self.draw_graph()
    def release_resource(self):
        process_id, ok1 = QInputDialog.getText(self, "Release Resource", "Enter process ID:")
        resource_id, ok2 = QInputDialog.getText(self, "Release Resource", "Enter resource ID:")
        if ok1 and ok2 and process_id in self.graph and resource_id in self.graph:
            if self.graph.has_edge(resource_id, process_id):
                self.graph.remove_edge(resource_id, process_id)
                self.resource_allocations[resource_id] = max(0, self.resource_allocations[resource_id] - 1)
            elif self.graph.has_edge(process_id, resource_id):
                self.graph.remove_edge(process_id, resource_id)
        self.draw_graph()
    def detect_deadlock(self):
        try:
            cycle = nx.find_cycle(self.graph, orientation='original')
            cycle_str = " -> ".join([f"{edge[0]} → {edge[1]}" for edge in cycle])
            QMessageBox.warning(self, "Deadlock Detected", f"Deadlock Detected!\nCycle: {cycle_str}")
        except nx.NetworkXNoCycle:
            QMessageBox.information(self, "No Deadlock", "No Deadlock Detected")
