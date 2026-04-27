import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QPushButton
from PyQt6.QtCore import Qt
from scripts.mouse_logic import ModelDWireless

class GloriousLink(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mouse = ModelDWireless()
        self.setWindowTitle("Glorious Linux Link")
        self.setFixedSize(300, 200)
        
        # Garuda-style Dark Theme
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QLabel { color: #e0e0e0; font-size: 16px; font-weight: bold; }
            QPushButton { 
                background-color: #2a2a2a; color: white; 
                border-radius: 5px; padding: 10px; border: 1px solid #444;
            }
            QPushButton:hover { background-color: #3a3a3a; border: 1px solid #00ffcc; }
        """)

        layout = QVBoxLayout()
        
        self.label = QLabel("Battery: --%")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        self.status_label = QLabel("Mode: Wired (Status Locked)")
        self.status_label.setStyleSheet("font-size: 10px; color: #888;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.refresh_btn = QPushButton("Refresh Status")
        self.refresh_btn.clicked.connect(self.update_battery)
        layout.addWidget(self.refresh_btn)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_battery(self):
        if self.mouse.connect():
            val = self.mouse.get_battery()
            # If the mouse sends zeros (like yours does wired), we show N/A
            if val == 0 or val == "0":
                self.label.setText("Battery: N/A (Wired)")
            else:
                self.label.setText(f"Battery: {val}%")
            self.mouse.disconnect()
        else:
            self.label.setText("Mouse Not Found")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GloriousLink()
    window.show()
    sys.exit(app.exec())
    
