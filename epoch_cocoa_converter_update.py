import sys
# Try PySide6 first, then PyQt6, then PyQt5
try:
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
    from PySide6.QtCore import Qt
except ImportError:
    try:
        from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
        from PyQt6.QtCore import Qt
    except ImportError:
        from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
        from PyQt5.QtCore import Qt

from datetime import datetime, timedelta, timezone

# Reference epoch for Cocoa (January 1, 2001 UTC)
COCOA_EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Epoch ‒ DateTime ‒ Cocoa Converter")
        self.setup_ui()
        # Initialize clock display once on startup
        self.update_clock()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Header: centered clock and refresh button at top-right
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Clock display (stacked vertically, left-aligned text)
        time_layout = QVBoxLayout()
        self.local_label = QLabel()
        self.local_label.setAlignment(Qt.AlignLeft)
        self.local_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.utc_label = QLabel()
        self.utc_label.setAlignment(Qt.AlignLeft)
        self.utc_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.epoch_label = QLabel()
        self.epoch_label.setAlignment(Qt.AlignLeft)
        self.epoch_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.cocoa_label = QLabel()
        self.cocoa_label.setAlignment(Qt.AlignLeft)
        self.cocoa_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        time_layout.addWidget(self.local_label)
        time_layout.addWidget(self.utc_label)
        time_layout.addWidget(self.epoch_label)
        time_layout.addWidget(self.cocoa_label)

        # Refresh button
        refresh_btn = QPushButton("Refresh Clock")
        refresh_btn.clicked.connect(self.update_clock)
        refresh_btn.setFixedWidth(120)

        # Assemble header: stretch, time, stretch, button
        header_layout.addStretch()
        header_layout.addLayout(time_layout)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        main_layout.addLayout(header_layout)

        # Input section: labels, edits, buttons in grid for alignment
        input_grid = QGridLayout()
        # make the edit column wider for proper display
        input_grid.setColumnStretch(1, 3)

        # Epoch row
        input_grid.addWidget(QLabel("Epoch (seconds since Unix epoch, UTC):"), 0, 0)
        self.epoch_edit = QLineEdit()
        input_grid.addWidget(self.epoch_edit, 0, 1)
        self.epoch_btn = QPushButton("Update Epoch")
        self.epoch_btn.clicked.connect(self.update_from_epoch)
        input_grid.addWidget(self.epoch_btn, 0, 2)

        # DateTime row
        input_grid.addWidget(QLabel("DateTime (YYYY-MM-DD HH:MM:SS, UTC):"), 1, 0)
        self.dt_edit = QLineEdit()
        input_grid.addWidget(self.dt_edit, 1, 1)
        self.dt_btn = QPushButton("Update DateTime")
        self.dt_btn.clicked.connect(self.update_from_datetime)
        input_grid.addWidget(self.dt_btn, 1, 2)

        # Cocoa row
        input_grid.addWidget(QLabel("Cocoa (seconds since 2001-01-01 UTC):"), 2, 0)
        self.cocoa_edit = QLineEdit()
        input_grid.addWidget(self.cocoa_edit, 2, 1)
        self.cocoa_btn = QPushButton("Update Cocoa")
        self.cocoa_btn.clicked.connect(self.update_from_cocoa)
        input_grid.addWidget(self.cocoa_btn, 2, 2)

        main_layout.addLayout(input_grid)

    def update_clock(self):
        # Show current times once, no live updating
        now_local = datetime.now()
        now_utc = datetime.now(timezone.utc)
        epoch = int(now_utc.timestamp())
        cocoa = int((now_utc - COCOA_EPOCH).total_seconds())
        self.local_label.setText(f"Local Time: {now_local.strftime('%Y-%m-%d %H:%M:%S')}")
        self.utc_label.setText(f"UTC Time:   {now_utc.strftime('%Y-%m-%d %H:%M:%S')}")
        self.epoch_label.setText(f"Epoch (UTC): {epoch}")
        self.cocoa_label.setText(f"Cocoa (UTC): {cocoa}")

    def update_from_epoch(self):
        text = self.epoch_edit.text().strip()
        try:
            ts = float(text)
            dt = datetime.fromtimestamp(ts, timezone.utc)
            self.dt_edit.setText(dt.strftime("%Y-%m-%d %H:%M:%S"))
            cocoa = int((dt - COCOA_EPOCH).total_seconds())
            self.cocoa_edit.setText(str(cocoa))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid Epoch value: {e}")

    def update_from_datetime(self):
        text = self.dt_edit.text().strip()
        try:
            dt = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
            dt = dt.replace(tzinfo=timezone.utc)
            ts = int(dt.timestamp())
            self.epoch_edit.setText(str(ts))
            cocoa = int((dt - COCOA_EPOCH).total_seconds())
            self.cocoa_edit.setText(str(cocoa))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid DateTime value: {e}")

    def update_from_cocoa(self):
        text = self.cocoa_edit.text().strip()
        try:
            secs = float(text)
            dt = COCOA_EPOCH + timedelta(seconds=secs)
            self.dt_edit.setText(dt.strftime("%Y-%m-%d %H:%M:%S"))
            ts = int(dt.timestamp())
            self.epoch_edit.setText(str(ts))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid Cocoa value: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec())
