"""
outgoing_dialog_window.py - نافذة تسجيل خروج صنف من الجرد
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

class OutgoingDialog(QDialog):
    """
    نافذة تسجيل خروج صنف: رقم القطعة أو الباركود، الكمية، وحالة الصنف.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Outgoing Item")
        self.setFixedSize(350, 300)
        self.setStyleSheet("""
            QLabel {
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #2e86de;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #1e5fad;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # رقم القطعة أو الباركود
        layout.addWidget(QLabel("Part Number or Barcode:"))
        self.part_edit = QLineEdit()
        layout.addWidget(self.part_edit)

        # الكمية
        layout.addWidget(QLabel("Quantity:"))
        self.qty_edit = QLineEdit()
        layout.addWidget(self.qty_edit)

        # حالة الصنف
        layout.addWidget(QLabel("Condition:"))
        self.condition_combo = QComboBox()
        self.condition_combo.addItems(["New", "Used"])
        layout.addWidget(self.condition_combo)

        # أزرار
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept_data)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def accept_data(self):
        """
        التحقق من صحة البيانات قبل قبولها.
        """
        part = self.part_edit.text().strip()
        qty_text = self.qty_edit.text().strip()
        condition = self.condition_combo.currentText()

        if not part or not qty_text:
            QMessageBox.warning(self, "Warning", "Please fill in all required fields.")
            return

        try:
            qty = int(qty_text)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Quantity must be a number.")
            return

        self.data = {
            "part": part,
            "quantity": qty,
            "condition": condition
        }
        self.accept()

    def get_data(self):
        """
        إرجاع البيانات بعد إغلاق النافذة.
        """
        return (
            self.data["part"],
            self.data["quantity"],
            self.data["condition"]
        )
