# item_dialog_window_ui.py
from PyQt5.QtWidgets import QDialog, QMessageBox, QSpinBox, QLineEdit, QPushButton
from modules.database import DatabaseManager

class ItemDialog(QDialog):
    """
    نافذة إضافة أو تعديل صنف في المخزن.
    """

    def __init__(self, db: DatabaseManager, item_record=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.item_record = item_record  # إذا كانت موجودة، سيتم تعديل الصنف
        self.setWindowTitle("Add/Edit Item")
        self.setFixedSize(300, 200)
        self.setup_ui()
        if self.item_record:
            self.load_item_data()

    def setup_ui(self):
        from PyQt5 import QtWidgets

        # اسم الصنف
        self.txtName = QtWidgets.QLineEdit(self)
        self.txtName.setGeometry(80, 20, 200, 25)
        self.txtName.setPlaceholderText("Item Name")

        # رقم القطعة
        self.txtPart = QtWidgets.QLineEdit(self)
        self.txtPart.setGeometry(80, 55, 200, 25)
        self.txtPart.setPlaceholderText("Part Number")

        # الكمية
        self.spinQuantity = QSpinBox(self)
        self.spinQuantity.setGeometry(80, 90, 200, 25)
        self.spinQuantity.setRange(1, 100000)

        # موقع الصنف
        self.txtLocation = QtWidgets.QLineEdit(self)
        self.txtLocation.setGeometry(80, 125, 200, 25)
        self.txtLocation.setPlaceholderText("Location")

        # أزرار
        self.btnOk = QPushButton("Save", self)
        self.btnOk.setGeometry(80, 160, 90, 30)
        self.btnOk.clicked.connect(self.save_item)

        self.btnCancel = QPushButton("Cancel", self)
        self.btnCancel.setGeometry(190, 160, 90, 30)
        self.btnCancel.clicked.connect(self.reject)

    def load_item_data(self):
        """
        تحميل بيانات الصنف إذا كانت موجودة للتعديل.
        """
        self.txtName.setText(self.item_record.get("name", ""))
        self.txtPart.setText(self.item_record.get("part_number", ""))
        self.spinQuantity.setValue(self.item_record.get("quantity", 1))
        self.txtLocation.setText(self.item_record.get("location", ""))

    def save_item(self):
        """
        التحقق من صحة البيانات وحفظ الصنف في قاعدة البيانات.
        """
        name = self.txtName.text().strip()
        part = self.txtPart.text().strip()
        quantity = self.spinQuantity.value()
        location = self.txtLocation.text().strip()

        if not name or not part:
            QMessageBox.warning(self, "Warning", "Item name and part number cannot be empty.")
            return

        try:
            if self.item_record:
                # تعديل الصنف
                self.db.update_item(
                    part_number=self.item_record["part_number"],
                    name=name,
                    new_part_number=part,
                    quantity=quantity,
                    location=location
                )
            else:
                # إضافة صنف جديد
                self.db.add_item(
                    name=name,
                    part_number=part,
                    quantity=quantity,
                    location=location
                )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save item.\n{str(e)}")
