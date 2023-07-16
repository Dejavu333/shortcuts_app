import json
import threading
import keyboard
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # Set the window title and size it cant be resized
        self.setWindowTitle('botyware')
        self.resize(400, 400)
        self.setFixedSize(self.size())

        # Set the style sheet
        with open('style.qss', 'r') as styleSheet:
            self.setStyleSheet(styleSheet.read())
        # Create the main widget and set it as the central widget
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        # Create a grid layout and set it as the main layout
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.central_widget.setLayout(self.grid_layout)
        # Create the input fields and labels
        self.key_combo_label = QtWidgets.QLabel('Key Combination:', self.central_widget)
        self.key_combo_field = QtWidgets.QLineEdit(self.central_widget)
        self.text_label = QtWidgets.QLabel('Text:', self.central_widget)
        self.text_field = QtWidgets.QLineEdit(self.central_widget)
        self.save_button = QtWidgets.QPushButton('Save', self.central_widget)
        self.delete_button = QtWidgets.QPushButton('Delete', self.central_widget)
        self.key_combos_list = QtWidgets.QListWidget(self.central_widget)
        # Add the input fields and labels to the grid layout
        self.grid_layout.addWidget(self.key_combo_label, 0, 0)
        self.grid_layout.addWidget(self.key_combo_field, 0, 1)
        self.grid_layout.addWidget(self.text_label, 1, 0)
        self.grid_layout.addWidget(self.text_field, 1, 1)
        self.grid_layout.addWidget(self.save_button, 2, 0, 1, 2)
        self.grid_layout.addWidget(self.delete_button, 4, 0, 1, 2)
        self.grid_layout.addWidget(self.key_combos_list, 3, 0, 1, 2)

        # Connect the save button's clicked signal to a slot that saves the key combination and text
        self.save_button.clicked.connect(self.save_key_combo)
        # Connect the save button's clicked signal to a slot that starts the key listening loop
        self.save_button.clicked.connect(self.start_listening_on_new_thread)
        # Connect the save button's clicked signal to a slot that saves the key combinations to a file
        self.save_button.clicked.connect(self.save_key_combos_to_file)
        # Connect the delete button's clicked signal to a slot that deletes the selected item from the list
        self.delete_button.clicked.connect(self.delete_selected_item)

        # Create a thread and a boolean to store the key listening loop
        self.thread = None
        self.listening = False
        # Create a dictionary to store the key combinations and texts
        self.key_combos = {}
        self.load_key_combos_from_file()
        # Add the saved items to the QListWidget
        self.items = []
        for key_combo, text in self.key_combos.items():
            item = f'{key_combo}: {text}'
            self.key_combos_list.addItem(item)
            self.items.append(item)
        # Start the key listening loop
        self.start_listening_on_new_thread()

    def save_key_combo(self):
        # Get the key combination and text from the input fields
        key_combo = self.key_combo_field.text()
        text = self.text_field.text()

        # Add the key combination and text to the dictionary
        self.key_combos[key_combo] = text

        # Create a list item with the key combination and text and add it to the QListWidget
        item = f'{key_combo}: {text}'
        self.key_combos_list.addItem(item)
        self.items.append(item)

        # Clear the input fields
        self.key_combo_field.clear()
        self.text_field.clear()

    def delete_selected_item(self):
        # Get the selected item
        item = self.key_combos_list.selectedItems()[0]
        # Remove the item from the QListWidget
        self.key_combos_list.takeItem(self.key_combos_list.row(item))
        # Remove the item from the list
        self.items.remove(item.text())
        # Remove the key combination and text from the dictionary
        key_combo = item.text().split(':')[0]
        del self.key_combos[key_combo]
        # Save the key combinations to a file
        self.save_key_combos_to_file()

    def listen_for_key_combos(self, key_combos):
        # Start a loop that globally listens for key combinations
        while True:
            for key_combo in key_combos:
                if keyboard.is_pressed(key_combo):
                    keyboard.write(key_combos[key_combo])
           
    def start_listening_on_new_thread(self):
        # If the key listening loop is already running, stop it
        if self.listening:
            self.thread.join()
            self.listening = False
        # Start the key listening loop on a new thread
        self.listening = True
        self.thread = threading.Thread(target=self.listen_for_key_combos, args=(self.key_combos,))
        self.thread.start()

    def save_key_combos_to_file(self):
            with open('key_combos.json', 'w') as f:
                json.dump(self.key_combos, f)

    def load_key_combos_from_file(self):
        try:
            with open('key_combos.json', 'r') as f:
                self.key_combos = json.load(f)
        except FileNotFoundError:
            # If the file doesn't exist, just create an empty dictionary
            self.key_combos = {}

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
