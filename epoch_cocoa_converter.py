import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from datetime import datetime, timedelta, timezone

# Reference epoch for Cocoa (January 1, 2001 UTC)
COCOA_EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Epoch / Cocoa Time Converter")
        self.setup_ui()
        self.setup_timer()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Current time display (UTC epoch & cocoa)
        time_layout = QVBoxLayout()
        self.epoch_label = QLabel()
        self.cocoa_label = QLabel()
        self.local_label = QLabel()
        self.utc_label = QLabel()
        time_layout.addWidget(self.epoch_label)
        time_layout.addWidget(self.cocoa_label)
        time_layout.addWidget(self.local_label)
        time_layout.addWidget(self.utc_label)
        layout.addLayout(time_layout)

        # Mode selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Conversion:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Epoch -> DateTime",
            "Cocoa -> DateTime",
            "DateTime -> Epoch",
            "DateTime -> Cocoa"
        ])
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)

        # Input
        input_layout = QHBoxLayout()
        input_label = QLabel("Input:")
        self.input_edit = QLineEdit()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_edit)
        layout.addLayout(input_layout)

        # Buttons: Convert and Swap
        button_layout = QHBoxLayout()
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert)
        self.swap_button = QPushButton("Swap")
        self.swap_button.clicked.connect(self.swap_values)
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.swap_button)
        layout.addLayout(button_layout)

        # Output
        output_layout = QHBoxLayout()
        output_label = QLabel("Output:")
        self.output_edit = QLineEdit()
        self.output_edit.setReadOnly(True)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_edit)
        layout.addLayout(output_layout)

    def setup_timer(self):
        # Update clock every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)
        self.update_clock()

    def update_clock(self):
        now_local = datetime.now()
        now_utc = datetime.now(timezone.utc)
        epoch = int(now_utc.timestamp())
        cocoa = int((now_utc - COCOA_EPOCH).total_seconds())
        self.epoch_label.setText(f"Current Epoch (UTC): {epoch}")
        self.cocoa_label.setText(f"Current Cocoa (UTC): {cocoa}")
        self.local_label.setText(
            f"Local Time:            {now_local.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.utc_label.setText(
            f"UTC Time:              {now_utc.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def convert(self):
        mode = self.mode_combo.currentText()
        text = self.input_edit.text().strip()
        try:
            if mode == "Epoch -> DateTime":
                ts = float(text)
                dt = datetime.fromtimestamp(ts, timezone.utc)
                result = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
            elif mode == "Cocoa -> DateTime":
                secs = float(text)
                dt = COCOA_EPOCH + timedelta(seconds=secs)
                result = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
            elif mode == "DateTime -> Epoch":
                # Parse input as UTC
                dt = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
                dt = dt.replace(tzinfo=timezone.utc)
                result = str(int(dt.timestamp()))
            elif mode == "DateTime -> Cocoa":
                dt = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
                dt = dt.replace(tzinfo=timezone.utc)
                delta = dt - COCOA_EPOCH
                result = str(int(delta.total_seconds()))
            else:
                raise ValueError("Unknown mode")
            self.output_edit.setText(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Conversion failed: {e}")

    def swap_values(self):
        # Swap the texts in input and output fields
        in_text = self.input_edit.text()
        out_text = self.output_edit.text()
        self.input_edit.setText(out_text)
        self.output_edit.setText(in_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec())
