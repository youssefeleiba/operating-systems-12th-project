import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import sys

# Define the Banker class
class Banker:
    def __init__(self, total_resources, available, allocation, max_need):
        self.total_resources = total_resources
        self.available = available
        self.allocation = allocation
        self.max_need = max_need
        self.processes = range(len(allocation))

    def request_resource(self, process_id, request):
        # Check if the request exceeds the maximum need
        if any(request[i] > self.max_need[process_id][i] for i in range(len(request))):
            return False

        # Check if the request can be satisfied with the available resources
        if any(request[i] > self.available[i] for i in range(len(request))):
            return False

        # Make a copy of the current state to simulate granting the request
        new_allocation = [self.allocation[i].copy() for i in self.processes]
        new_available = self.available.copy()

        for i in range(len(request)):
            new_allocation[process_id][i] += request[i]
            new_available[i] -= request[i]

        # Check if the resulting state is safe
        if not self._is_safe(new_available, new_allocation):
            return False

        # Grant the request
        self.available = new_available
        self.allocation = new_allocation
        return True

    def _is_safe(self, available, allocation):
        # Initialize the work and finish vectors
        work = available.copy()
        finish = [False] * len(self.processes)

        # Find a process that can be executed
        while True:
            found = False
            for i in self.processes:
                if not finish[i] and all(allocation[i][j] <= work[j] for j in range(len(work))):
                    found = True
                    finish[i] = True
                    work = [work[j] + allocation[i][j] for j in range(len(work))]
            if not found:
                break

        # Check if all processes have finished
        return all(finish)

# Define the BankerGUI class
class BankerGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Create the input fields and button
        self.process_id_input = QLineEdit()
        self.request_input = QLineEdit()
        self.submit_button = QPushButton('Submit Request')
        self.submit_button.clicked.connect(self.submit_request)

        # Create a layout for the input fields and button
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Process ID:'))
        layout.addWidget(self.process_id_input)
        layout.addWidget(QLabel('Resource Request:'))
        layout.addWidget(self.request_input)
        layout.addWidget(self.submit_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set the window properties
        self.setWindowTitle('Banker GUI')
        self.setGeometry(100, 100, 300, 150)
        self.show()

    def submit_request(self):
        # Get the input values
        process_id = int(self.process_id_input.text())
        request = list(map(int, self.request_input.text().split()))

        # Process the resource request
        if banker.request_resource(process_id-1, request):
            print("Resource request granted.")
        else:
            print("Resource request denied.")

if __name__ == '__main__':
    # Get input from the user
    num_resources = int(input("Enter the number of resource types: "))
    total_resources = np.zeros(num_resources)
    available = np.zeros(num_resources)
    allocation = np.zeros((0, num_resources))
    max_need = np.zeros((0, num_resources))

    # Get the total resources
    for i in range(num_resources):
        total_resources[i] = int(input(f"Enter the total number of resources of type {i+1}: "))

    # Get the available resources
    for i in range(num_resources):
        available[i] = int(input(f"Enter the number of available resources of type {i+1}: "))

    # Get the current allocation matrix
    while True:
        process_allocation = np.zeros(num_resources)
        for i in range(num_resources):
            process_allocation[i] = int(input(f"Enter the current allocation of process {len(allocation)+1} for resource type {i+1}: "))
        allocation = np.vstack((allocation, process_allocation))
        response = input("Would you like to enter another process? (y/n): ")
        if response.lower() == 'n':
            break

    # Get the maximum need matrix
    for i in range(len(allocation)):
        process_max_need = np.zeros(num_resources)
        for j in range(num_resources):
            process_max_need[j] = int(input(f"Enter the maximum need of process {i+1} for resource type {j+1}: "))
        max_need = np.vstack((max_need, process_max_need))

    # Create a banker object
    banker = Banker(total_resources, available, allocation, max_need)

    # Start the GUI
    app = QApplication(sys.argv)
    gui = BankerGUI()
    sys.exit(app.exec_())