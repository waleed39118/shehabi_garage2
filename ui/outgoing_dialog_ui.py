# outgoing_dialog_window_ui.py
"""
OutgoingDialog - نافذة تسجيل خروج صنف من المخزن
"""

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton, QMessageBox
from modules.database import DatabaseManager

class OutgoingDialog(QDialog):
    """
    نافذة تسجيل خروج صنف: رقم القطعة أو الباركود، الكمية، وحالة الصنف.
    """

    def __init__(self, db: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Record Outgoing Item")
        self.setFixedSize(350, 250)
        self.setup_ui()

    def setup_ui(self):
        # رقم القطعة أو الباركود
        self.lblPart = QLabel("Part Number or Barcode:", self)
        self.lblPart.setGeometry(20, 20, 150, 25)
        self.txtPart = QLineEdit(self)
        self.txtPart.setGeometry(180, 20, 150, 25)
        self.txtPart.setPlaceholderText("Enter part number or barcode")

        # الكمية
        self.lblQuantity = QLabel("Quantity:", self)
        self.lblQuantity.setGeometry(20, 60, 150, 25)
        self.spinQuantity = QSpinBox(self)
        self.spinQuantity.setGeometry(180, 60, 150, 25)
        self.spinQuantity.setRange(1, 100000)

        # حالة الصنف
        self.lblCondition = QLabel("Condition:", self)
        self.lblCondition.setGeometry(20, 100, 150, 25)
        self.comboCondition = QComboBox(self)
        self.comboCondition.setGeometry(180, 100, 150, 25)
        self.comboCondition.addItems(["New", "Used"])

        # أزرار
        self.btnOk = QPushButton("Record", self)
        self.btnOk.setGeometry(80, 160, 90, 30)
        self.btnOk.clicked.connect(self.record_outgoing)

        self.btnCancel = QPushButton("Cancel", self)
        self.btnCancel.setGeometry(180, 160, 90, 30)
        self.btnCancel.clicked.connect(self.reject)

    def record_outgoing(self):
        """
        التحقق من صحة البيانات وتسجيل خروج الصنف.
        """
        part = self.txtPart.text().strip()
        quantity = self.spinQuantity.value()
        condition = self.comboCondition.currentText()

        if not part:
            QMessageBox.warning(self, "Warning", "Please enter the part number or barcode.")
            return

        # التحقق من وجود الصنف في قاعدة البيانات
        item = self.db.get_item_by_part(part)
        if not item:
            QMessageBox.warning(self, "Warning", f"Item with part '{part}' not found.")
            return

        if quantity > item.get("quantity", 0):
            QMessageBox.warning(self, "Warning", "Quantity exceeds available stock.")
            return

        try:
            # تحديث الكمية بعد تسجيل الخروج
            new_quantity = item["quantity"] - quantity
            self.db.update_item(
                part_number=part,
                name=item["name"],
                new_part_number=part,
                quantity=new_quantity,
                location=item.get("location", ""),
                condition=condition  # تحديث حالة الصنف إذا كانت مطلوبة
            )
            QMessageBox.information(
                self,
                "Success",
                f"Outgoing recorded successfully.\nRemaining stock: {new_quantity}"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to record outgoing item.\n{str(e)}")

    def get_data(self):
        """
        إرجاع البيانات بعد إدخالها.
        """
        return {
            "part": self.txtPart.text().strip(),
            "quantity": self.spinQuantity.value(),
            "condition": self.comboCondition.currentText()
        }
