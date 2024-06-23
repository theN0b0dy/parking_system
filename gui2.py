import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem, QGridLayout, QMainWindow, QScrollArea, QTabWidget, QMessageBox, QAction, QMenu, QInputDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage 
import cv2
import database
from datetime import datetime

from ANPR_ir import ANRPIR

# class SmartParkingApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.plate_rec = ANRPIR()
#         # initialazing database
#         self.db = database.ParkDatabase()
#         self.detected_plates = []
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle('Smart Parking System')
#         self.setGeometry(100, 100, 1400, 600)  # Larger window size

#         self.header_label = QLabel('Smart Parking System', self)
#         self.header_label.setStyleSheet('font-size: 20px; font-weight: bold;')

#         self.image_label = QLabel(self)
#         self.image_label.setAlignment(Qt.AlignCenter)
#         self.image_label.setFixedSize(900, 600)  # Larger size for image display

#         self.btn_choose_file = QPushButton('Choose File')
#         self.btn_webcam = QPushButton('Enable Webcam')
#         self.btn_slots = QPushButton('Parking Slots')
        
#         self.btn_choose_file.clicked.connect(self.chooseFile)
#         self.btn_webcam.clicked.connect(self.enableWebcam)
#         self.btn_slots.clicked.connect(self.showParkingSlots)
        
#         # Table widget for displaying number plates 
#         self.table_widget = QTableWidget(self)
#         self.table_widget.setColumnCount(4)
#         self.table_widget.setHorizontalHeaderLabels(['Number Plate', 'Slot', 'time', 'floor'])
#         self.table_widget.setRowCount(100)
#         self.table_item_count = 0

#         # Layout setup: Vertical layout for main window
#         main_layout = QHBoxLayout(self)

#         # Left side layout (image display)
#         left_layout = QVBoxLayout()
#         left_layout.addWidget(self.header_label, alignment=Qt.AlignCenter)
#         left_layout.addWidget(self.image_label)
#         left_layout.addWidget(self.btn_choose_file)
#         left_layout.addWidget(self.btn_slots)
#         left_layout.addWidget(self.btn_webcam)
#         left_layout.addStretch(1)  # Add stretchable space at the bottom
#         main_layout.addLayout(left_layout)

#         # Right side layout (table widget)
#         right_layout = QVBoxLayout()
#         right_layout.addWidget(self.table_widget)
#         main_layout.addLayout(right_layout)

#         self.setLayout(main_layout)

#         self.cap = None
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.updateFrame)

#     def chooseFile(self):
#         options = QFileDialog.Options()
#         fileName, _ = QFileDialog.getOpenFileName(self, 'Choose Image', '', 'Image files (*.jpg *.png *.jpeg)', options=options)
#         if fileName:
#             self.plate_rec.read_image(fileName)
#             plateNumbers, imgs = self.plate_rec.process_img()
#             rgb_image = imgs
#             # not found 
#             if len(plateNumbers) == 0:
#                 QMessageBox.information(self, 'Error', 'Car plate not found', QMessageBox.Ok)
#                 return
#             for pn in plateNumbers:
#                 if self.validateDetectedNumberPlate(pn):
#                     time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                     self.detected_plates.append(pn)
#                     self.addPlateNumberToTable(pn, str(1), time, str(1))
#             h, w, ch = rgb_image.shape
#             bytes_per_line = ch * w

#             # Convert to QImage
#             qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
#             # Convert QImage to QPixmap
#             pixmap = QPixmap.fromImage(qt_image)
            
#             # Display QPixmap in QLabel
#             self.image_label.setPixmap(pixmap)
#             self.image_label.setScaledContents(True)
    
#     def enableWebcam(self):
#         if self.cap is None or not self.cap.isOpened():
#             self.cap = cv2.VideoCapture(0)  # Open default camera (usually index 0)

#             if self.cap.isOpened():
#                 self.timer.start(100)  # Update frame every 30 milliseconds (you can adjust this)
#             else:
#                 print("Error: Could not open webcam.")

#         else:
#             self.cap.release()
#             self.timer.stop()

#     def updateFrame(self):
#         ret, frame = self.cap.read()
#         if ret:
#             self.plate_rec.read_frame(frame)
#             plateNumbers, imgs = self.plate_rec.process_img()
#             if len(imgs) != 0:
#                 frame = imgs
#                 if len(plateNumbers) != 0:
#                     for pn in plateNumbers:
#                         if self.validateDetectedNumberPlate(pn):
#                             time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                             self.addPlateNumberToTable(pn, str(1), time, str(1))
#                             self.detected_plates.append(pn)
                
#             rgb_image = frame
#             h, w, ch = rgb_image.shape
#             bytes_per_line = ch * w

#             qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
#             pixmap = QPixmap.fromImage(qt_image)
#             self.image_label.setPixmap(pixmap)
#             self.image_label.setScaledContents(True)

#     def closeEvent(self, event):
#         # Release webcam and stop timer on application close
#         if self.cap and sel.cap.isOpened():
#             self.cap.release()
#         self.timer.stop()
#         event.accept()
    
#     def addPlateNumberToTable(self, plate_number, slot, time, floor):
#         plate_item = QTableWidgetItem(plate_number)
#         slot_item = QTableWidgetItem(slot)
#         time_item = QTableWidgetItem(time)
#         floor_item = QTableWidgetItem(floor)
#         self.table_widget.setItem(self.table_item_count, 0, plate_item)
#         self.table_widget.setItem(self.table_item_count, 1, slot_item)
#         self.table_widget.setItem(self.table_item_count, 2, time_item)
#         self.table_widget.setItem(self.table_item_count, 3, floor_item)
#         self.table_item_count += 1
    
#     def validateDetectedNumberPlate(self, number_plate):
#         if len(number_plate) < 8:
#             return False
        
#         for pn in self.detected_plates:
#             if number_plate == pn:
#                 return False
        
#         return True
    
#     def showParkingSlots(self):
#         self.parking_window = ParkingSlotsWindow()
#         self.parking_window.show()


import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem, QGridLayout, QMainWindow, QScrollArea, QTabWidget, QMessageBox, QAction, QMenu, QInputDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
import cv2
import database
from datetime import datetime

from ANPR_ir import ANRPIR



class SmartParkingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.plate_rec = ANRPIR()
        # Initializing database
        self.detected_plates = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Smart Parking System')
        self.setGeometry(100, 100, 1400, 600)

        self.header_label = QLabel('Smart Parking System', self)
        self.header_label.setStyleSheet('font-size: 20px; font-weight: bold;')

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(900, 600)

        self.btn_choose_file = QPushButton('Choose File')
        self.btn_webcam = QPushButton('Enable Webcam')
        self.btn_slots = QPushButton('Parking Slots')

        self.btn_choose_file.clicked.connect(self.chooseFile)
        self.btn_webcam.clicked.connect(self.enableWebcam)
        self.btn_slots.clicked.connect(self.showParkingSlots)

        # Table widget for displaying number plates
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['Number Plate', 'Slot', 'Time', 'Floor'])
        self.table_widget.setRowCount(100)
        self.table_item_count = 0

        # Layout setup: Vertical layout for main window
        main_layout = QHBoxLayout(self)

        # Left side layout (image display)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.header_label, alignment=Qt.AlignCenter)
        left_layout.addWidget(self.image_label)
        left_layout.addWidget(self.btn_choose_file)
        left_layout.addWidget(self.btn_slots)
        left_layout.addWidget(self.btn_webcam)
        left_layout.addStretch(1)
        main_layout.addLayout(left_layout)

        # Right side layout (table widget)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.table_widget)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)

    def chooseFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'Choose Image', '', 'Image files (*.jpg *.png *.jpeg)', options=options)
        if fileName:
            self.plate_rec.read_image(fileName)
            plateNumbers, imgs = self.plate_rec.process_img()
            rgb_image = imgs

            if len(plateNumbers) == 0:
                QMessageBox.information(self, 'Error', 'Car plate not found', QMessageBox.Ok)
                return

            for pn in plateNumbers:
                if self.validateDetectedNumberPlate(pn):
                    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.detected_plates.append(pn)
                    self.addPlateNumberToTable(pn, '1', time, '1')
                    self.db.add_entry(pn, '1', time, '1')

            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

            # Update parking slot map after adding the car
            self.addPlateNumberToTable(plateNumbers[0], '1', time, '1')

    def enableWebcam(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.timer.start(100)
            else:
                print("Error: Could not open webcam.")
        else:
            self.cap.release()
            self.timer.stop()

    def updateFrame(self):
        ret, frame = self.cap.read()
        if ret:
            self.plate_rec.read_frame(frame)
            plateNumbers, imgs = self.plate_rec.process_img()
            if len(imgs) != 0:
                frame = imgs
                if len(plateNumbers) != 0:
                    for pn in plateNumbers:
                        if self.validateDetectedNumberPlate(pn):
                            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            self.addPlateNumberToTable(pn, '1', time, '1')
                            self.db.add_entry(pn, '1', time, '1')
                            self.detected_plates.append(pn)

            rgb_image = frame
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

            # Update parking slot map after adding the car
            if len(plateNumbers) > 0:
                self.addPlateNumberToTable(plateNumbers[0], '1', time, '1')

    def closeEvent(self, event):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.timer.stop()
        self.db.close()
        event.accept()

    def addPlateNumberToTable(self, plate_number, slot, time, floor):
        # Find the first available slot and assign it to the car
        for floor_file, map_data in self.parking_window.maps_data.items():
            for i, row in enumerate(map_data):
                for j, cell in enumerate(row):
                    if cell == 'E':  # E for Empty slot
                        map_data[i][j] = 'P'  # P for Parked
                        self.parking_window.slot_buttons[i][j].setText('P')
                        self.parking_window.slot_buttons[i][j].setStyleSheet('background-color: #ffa500; color: white; border: 1px solid black;')
                        self.table_widget.setItem(self.table_item_count, 0, QTableWidgetItem(plate_number))
                        self.table_widget.setItem(self.table_item_count, 1, QTableWidgetItem(str(j)))  # Slot number
                        self.table_widget.setItem(self.table_item_count, 2, QTableWidgetItem(time))
                        self.table_widget.setItem(self.table_item_count, 3, QTableWidgetItem(floor_file))
                        self.table_item_count += 1
                        self.db.add_entry(plate_number, str(j), time, floor_file)
                        return
        QMessageBox.information(self, 'Parking Full', 'All parking slots are occupied.', QMessageBox.Ok)


    def validateDetectedNumberPlate(self, number_plate):
        if len(number_plate) < 8:
            return False
        for pn in self.detected_plates:
            if number_plate == pn:
                return False
        return True

    def showParkingSlots(self):
        self.parking_window = ParkingSlotsWindow()
        self.parking_window.show()

class ParkingSlotsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Parking Slots')
        self.setGeometry(150, 150, 800, 600)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Directory where map files are located
        self.map_files_dir = './maps/'

        # Get list of files in the directory
        self.map_files = [f for f in os.listdir(self.map_files_dir) if f.startswith('parking_map_floor') and f.endswith('.txt')]

        if not self.map_files:
            self.tab_widget.addTab(QWidget(), 'No Floors Found')
        else:
            self.loadFloors()

    def loadFloors(self):
        self.tabs = []
        self.maps_data = {}  # To hold map data for each floor
        self.plate_numbers = {}  # To hold number plates for each slot
        for floor_file in self.map_files:
            floor_widget = QWidget()
            grid_layout = QGridLayout()
            grid_layout.setSpacing(10)  # Add spacing between buttons

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_content.setLayout(grid_layout)
            scroll_area.setWidget(scroll_content)

            layout = QVBoxLayout(floor_widget)
            layout.addWidget(scroll_area)
            tab_name = str(floor_file).strip("parking_map_").strip(".txt")
            map_data, plates_data = self.createParkingSlotsFromMap(os.path.join(self.map_files_dir, floor_file), grid_layout)
            self.maps_data[floor_file] = map_data  # Store map data for the floor
            self.plate_numbers[floor_file] = plates_data  # Store plate numbers for each slot

            self.tab_widget.addTab(floor_widget, tab_name)
            self.tabs.append(floor_widget)

            # Add save button for each floor
            save_button = QPushButton('Save Map')
            save_button.clicked.connect(lambda _, file=floor_file: self.saveMap(file))
            layout.addWidget(save_button)

    def createParkingSlotsFromMap(self, map_file, grid_layout):
        # Read the map from the file and create parking slots
        with open(map_file, 'r') as file:
            map_data = [line.rstrip().split(' ') for line in file.readlines()]

        plate_numbers = [['' for _ in row] for row in map_data]

        self.slot_buttons = []
        for i, row in enumerate(map_data):
            row_buttons = []
            for j, cell in enumerate(row):
                slot_button = QPushButton(cell)
                slot_button.setFixedSize(80, 80)
                slot_button.setContextMenuPolicy(Qt.CustomContextMenu)
                slot_button.customContextMenuRequested.connect(lambda pos, button=slot_button, i=i, j=j, map_data=map_data, plates_data=plate_numbers: self.showContextMenu(pos, button, i, j, map_data, plates_data))
                slot_button.clicked.connect(lambda _, button=slot_button, i=i, j=j, map_data=map_data: self.toggleSlot(button, i, j, map_data))
                self.setButtonStyle(slot_button, cell)
                row_buttons.append(slot_button)
                grid_layout.addWidget(slot_button, i, j)
            self.slot_buttons.append(row_buttons)

        return map_data, plate_numbers

    def setButtonStyle(self, button, cell):
        if cell == 'E':
            button.setStyleSheet('background-color: #5cb85c; color: white; border: 1px solid black;')
        elif cell == 'P':
            button.setStyleSheet('background-color: #ffa500; color: white; border: 1px solid black;')
        elif cell == 'R':
            button.setStyleSheet('background-color: #d9534f; color: white; border: 1px solid black;')
        elif cell == 'I':
            button.setStyleSheet('background-color: #0275d8; color: white; border: 1px solid black;')
        elif cell == 'O':
            button.setStyleSheet('background-color: #f0ad4e; color: white; border: 1px solid black;')
        else:
            button.setStyleSheet('background-color: none; border: 1px solid black;')

    def showContextMenu(self, pos, button, i, j, map_data, plates_data):
        context_menu = QMenu(button)

        if map_data[i][j] == 'P':
            number_plate_action = QAction(f"Number Plate: {plates_data[i][j]}", self)
            context_menu.addAction(number_plate_action)
            change_plate_action = QAction("Change Number Plate", self)
            change_plate_action.triggered.connect(lambda: self.changeNumberPlate(i, j, plates_data))
            context_menu.addAction(change_plate_action)

        elif map_data[i][j] == 'E':
            change_to_parked_action = QAction("Change to Parked", self)
            change_to_parked_action.triggered.connect(lambda: self.toggleSlot(button, i, j, map_data))
            context_menu.addAction(change_to_parked_action)

        context_menu.exec_(button.mapToGlobal(pos))

    def changeNumberPlate(self, i, j, plates_data):
        text, ok = QInputDialog.getText(self, 'Change Number Plate', 'Enter new number plate:')
        if ok and text:
            plates_data[i][j] = text

    def toggleSlot(self, button, i, j, map_data):
        current_text = map_data[i][j]
        if current_text == 'E':
            map_data[i][j] = 'P'
            button.setText('P')
            button.setStyleSheet('background-color: #ffa500; color: white; border: 1px solid black;')
        elif current_text == 'P':
            map_data[i][j] = 'R'
            button.setText('R')
            button.setStyleSheet('background-color: #d9534f; color: white; border: 1px solid black;')
        elif current_text == 'R':
            map_data[i][j] = 'I'
            button.setText('I')
            button.setStyleSheet('background-color: #0275d8; color: white; border: 1px solid black;')
        elif current_text == 'I':
            map_data[i][j] = 'O'
            button.setText('O')
            button.setStyleSheet('background-color: #f0ad4e; color: white; border: 1px solid black;')
        elif current_text == 'O':
            map_data[i][j] = ''
            button.setText('')
            button.setStyleSheet('background-color: none; border: 1px solid black;')
        else:
            map_data[i][j] = 'E'
            button.setText('E')
            button.setStyleSheet('background-color: #5cb85c; color: white; border: 1px solid black;')

    def saveMap(self, floor_file):
        # Save map data to file
        try:
            with open(os.path.join(self.map_files_dir, floor_file), 'w') as file:
                for row in self.maps_data[floor_file]:
                    file.write(' '.join(row) + '\n')
                QMessageBox.information(self, 'Save Successful', 'Map saved successfully.', QMessageBox.Ok)
        except IOError:
            QMessageBox.critical(self, 'Save Error', 'Error saving map file.', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SmartParkingApp()
    ex.show()
    sys.exit(app.exec_())

