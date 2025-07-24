#!/usr/bin/env python3
import sys
from datetime import datetime, timezone

# Try PySide6 → PyQt6 → PyQt5
try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
        QGridLayout, QVBoxLayout, QHBoxLayout
    )
    from PySide6.QtCore import Qt
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
            QGridLayout, QVBoxLayout, QHBoxLayout
        )
        from PyQt6.QtCore import Qt
    except ImportError:
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
            QGridLayout, QVBoxLayout, QHBoxLayout
        )
        from PyQt5.QtCore import Qt


COCOA_EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc).timestamp()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Epoch ↔ Cocoa ↔ UTC ↔ Local Converter")
        self.resize(400, 200)  # smaller by default

        # Central widget & main layout
        central = QWidget()
        main_v = QVBoxLayout(central)
        main_v.setContentsMargins(20, 20, 20, 20)
        main_v.setSpacing(15)

        # — Live clock block —
        clock_block = QWidget()
        clock_v = QVBoxLayout(clock_block)
        clock_v.setAlignment(Qt.AlignHCenter)

        # Clock labels (left-aligned & selectable)
        self.lbl_cocoa_now = QLabel()
        self.lbl_epoch_now = QLabel()
        self.lbl_utc_now   = QLabel()
        self.lbl_local_now = QLabel()
        for lbl in (
            self.lbl_cocoa_now,
            self.lbl_epoch_now,
            self.lbl_utc_now,
            self.lbl_local_now
        ):
            lbl.setAlignment(Qt.AlignLeft)
            lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            clock_v.addWidget(lbl)

        # Refresh button (centered under clock)
        btn_refresh = QPushButton("Refresh Clock")
        btn_refresh.clicked.connect(self.update_clock)
        refresh_h = QHBoxLayout()
        refresh_h.setAlignment(Qt.AlignHCenter)
        refresh_h.addWidget(btn_refresh)
        clock_v.addLayout(refresh_h)

        main_v.addWidget(clock_block)

        # — Conversion grid —
        grid = QGridLayout()
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 3)  # make the input/output column wider

        # Row definitions: (label text, handler)
        rows = [
            ("Cocoa (UTC)",    self.on_cocoa_update),
            ("Epoch (UTC)",    self.on_epoch_update),
            ("UTC DateTime",   self.on_utc_update),
            ("Local DateTime", self.on_local_update),
        ]
        self.inputs = {}
        for i, (label_text, handler) in enumerate(rows):
            lbl = QLabel(label_text + ":")
            lbl.setAlignment(Qt.AlignLeft)  # left-align labels
            edit = QLineEdit()
            btn  = QPushButton("Update")
            btn.clicked.connect(handler)
            grid.addWidget(lbl, i, 0)
            grid.addWidget(edit, i, 1)
            grid.addWidget(btn,  i, 2)
            self.inputs[label_text] = edit

        main_v.addLayout(grid)

        # Set central widget and initial clock
        self.setCentralWidget(central)
        self.update_clock()

    def update_clock(self):
        now_utc   = datetime.now(timezone.utc)
        now_local = datetime.now()  # naive local time

        # Populate labels
        self.lbl_cocoa_now.setText(
            f"Cocoa Now (UTC): {now_utc.timestamp() - COCOA_EPOCH:.0f}"
        )
        self.lbl_epoch_now.setText(
            f"Epoch Now (UTC): {now_utc.timestamp():.0f}"
        )
        self.lbl_utc_now.setText(
            f"UTC Now: {now_utc.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.lbl_local_now.setText(
            f"Local Now: {now_local.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def on_cocoa_update(self):
        text = self.inputs["Cocoa (UTC)"].text().strip()
        try:
            cocoa = float(text)
            dt_utc = datetime.fromtimestamp(cocoa + COCOA_EPOCH, timezone.utc)
            self.inputs["Epoch (UTC)"].setText(f"{dt_utc.timestamp():.0f}")
            self.inputs["UTC DateTime"].setText(
                dt_utc.strftime('%Y-%m-%d %H:%M:%S')
            )
            self.inputs["Local DateTime"].setText(
                dt_utc.astimezone().strftime('%Y-%m-%d %H:%M:%S')
            )
        except Exception:
            pass

    def on_epoch_update(self):
        text = self.inputs["Epoch (UTC)"].text().strip()
        try:
            epoch = float(text)
            dt_utc = datetime.fromtimestamp(epoch, timezone.utc)
            self.inputs["Cocoa (UTC)"].setText(f"{dt_utc.timestamp() - COCOA_EPOCH:.0f}")
            self.inputs["UTC DateTime"].setText(
                dt_utc.strftime('%Y-%m-%d %H:%M:%S')
            )
            self.inputs["Local DateTime"].setText(
                dt_utc.astimezone().strftime('%Y-%m-%d %H:%M:%S')
            )
        except Exception:
            pass

    def on_utc_update(self):
        text = self.inputs["UTC DateTime"].text().strip()
        try:
            dt = datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
            dt = dt.replace(tzinfo=timezone.utc)
            self.inputs["Epoch (UTC)"].setText(f"{dt.timestamp():.0f}")
            self.inputs["Cocoa (UTC)"].setText(f"{dt.timestamp() - COCOA_EPOCH:.0f}")
            self.inputs["Local DateTime"].setText(
                dt.astimezone().strftime('%Y-%m-%d %H:%M:%S')
            )
        except Exception:
            pass

    def on_local_update(self):
        text = self.inputs["Local DateTime"].text().strip()
        try:
            dt_local = datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
            dt_utc = dt_local.astimezone(timezone.utc)
            self.inputs["Epoch (UTC)"].setText(f"{dt_utc.timestamp():.0f}")
            self.inputs["Cocoa (UTC)"].setText(f"{dt_utc.timestamp() - COCOA_EPOCH:.0f}")
            self.inputs["UTC DateTime"].setText(
                dt_utc.strftime('%Y-%m-%d %H:%M:%S')
            )
        except Exception:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
