"""
edit_dialog_window.py - نافذة تعديل صنف موجود
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

class EditDialog(QDialog):
    """
    نافذة تعديل بيانات صنف موجود مع دعم الباركود وحالة الصنف.
    """

    def __init__(self, name, part, quantity, barcode, condition, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Item")
        self.setFixedSize(380, 360)
        self.setStyleSheet("""
            QLabel {
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                padding: 6px;
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

        # 🌟 اسم الصنف
        layout.addWidget(QLabel("Item Name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setText(name)
        layout.addWidget(self.name_edit)

        # 🌟 رقم القطعة
        layout.addWidget(QLabel("Part Number:"))
        self.part_edit = QLineEdit()
        self.part_edit.setText(part)
        layout.addWidget(self.part_edit)

        # 🌟 الكمية
        layout.addWidget(QLabel("Quantity:"))
        self.qty_edit = QLineEdit()
        self.qty_edit.setText(str(quantity))
        layout.addWidget(self.qty_edit)

        # 🌟 الباركود
        layout.addWidget(QLabel("Barcode:"))
        self.barcode_edit = QLineEdit()
        self.barcode_edit.setText(barcode)
        self.barcode_edit.setPlaceholderText("Scan or enter manually")
        layout.addWidget(self.barcode_edit)

        # 🌟 حالة الصنف
        layout.addWidget(QLabel("Condition:"))
        self.condition_combo = QComboBox()
        self.condition_combo.addItems(["New", "Used"])
        self.condition_combo.setCurrentText(condition)
        layout.addWidget(self.condition_combo)

        # 🌟 أزرار حفظ وإلغاء
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept_data)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def accept_data(self):
        """
        التحقق من صحة البيانات وإغلاق النافذة عند النجاح.
        """
        name = self.name_edit.text().strip()
        part = self.part_edit.text().strip()
        qty_text = self.qty_edit.text().strip()
        barcode = self.barcode_edit.text().strip()
        condition = self.condition_combo.currentText()

        if not name or not part or not qty_text:
            QMessageBox.warning(self, "Warning", "Please fill in all required fields.")
            return

        try:
            qty = int(qty_text)
            if qty < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Warning", "Quantity must be a positive number.")
            return

        self.data = {
            "name": name,
            "part": part,
            "quantity": qty,
            "barcode": barcode,
            "condition": condition
        }
        self.accept()

    def get_data(self):
        """
        إرجاع البيانات بعد التعديل.
        """
        return (
            self.data["name"],
            self.data["part"],
            self.data["quantity"],
            self.data["barcode"],
            self.data["condition"]
        )
