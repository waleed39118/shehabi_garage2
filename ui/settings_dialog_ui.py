# settings_dialog_window_ui.py
import json
from pathlib import Path
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

SETTINGS_PATH = Path(__file__).resolve().parent.parent / "settings.json"

class SettingsDialog(QDialog):
    """
    نافذة تعديل إعدادات المشروع مع التحقق الكامل من القيم.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Project Settings")
        self.setFixedSize(350, 250)
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # اسم الكراج
        layout.addWidget(QLabel("Garage Name:"))
        self.garage_name_edit = QLineEdit()
        layout.addWidget(self.garage_name_edit)

        # الحد الأقصى للصفوف
        layout.addWidget(QLabel("Max Rows in Inventory Table:"))
        self.max_rows_edit = QLineEdit()
        layout.addWidget(self.max_rows_edit)

        # خيارات عرض الموقع ووقت التحديث
        self.show_location_checkbox = QCheckBox("Show Location Column")
        self.show_last_updated_checkbox = QCheckBox("Show Last Updated Column")
        layout.addWidget(self.show_location_checkbox)
        layout.addWidget(self.show_last_updated_checkbox)

        # أزرار الحفظ والإلغاء
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_settings(self):
        """
        تحميل الإعدادات من ملف JSON أو تعيين القيم الافتراضية عند عدم وجود الملف.
        """
        default_data = {
            "garage_name": "Shihabi Garage",
            "max_rows": 100,
            "show_location": True,
            "show_last_updated": True
        }

        if SETTINGS_PATH.exists():
            try:
                with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    data = json.loads(content) if content else default_data
            except Exception:
                data = default_data
        else:
            data = default_data

        self.garage_name_edit.setText(data.get("garage_name", "Shihabi Garage"))
        self.max_rows_edit.setText(str(data.get("max_rows", 100)))
        self.show_location_checkbox.setChecked(data.get("show_location", True))
        self.show_last_updated_checkbox.setChecked(data.get("show_last_updated", True))

    def save_settings(self):
        """
        حفظ الإعدادات بعد التحقق من صحة البيانات.
        """
        garage_name = self.garage_name_edit.text().strip()
        max_rows_text = self.max_rows_edit.text().strip()

        if not garage_name:
            QMessageBox.warning(self, "Warning", "Garage name cannot be empty.")
            return

        try:
            max_rows = int(max_rows_text)
            if max_rows <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Warning", "Max rows must be a positive integer.")
            return

        data = {
            "garage_name": garage_name,
            "max_rows": max_rows,
            "show_location": self.show_location_checkbox.isChecked(),
            "show_last_updated": self.show_last_updated_checkbox.isChecked()
        }

        try:
            with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Saved", "Settings saved successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings.\n{str(e)}")
