"""
user_edit_dialog.py - نافذة إضافة أو تعديل مستخدم
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt

class UserEditDialog(QDialog):
    """
    نافذة لإضافة أو تعديل مستخدم مع جميع الحقول والصلاحيات.
    """

    def __init__(self, user_record=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit User")
        self.setFixedSize(350, 300)
        self.user_record = user_record  # إذا كانت موجودة، نعدل المستخدم الحالي

        self.setStyleSheet("""
            QLabel {
                font-size: 13px;
            }
            QLineEdit, QComboBox, QCheckBox {
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

        # اسم المستخدم
        layout.addWidget(QLabel("Username:"))
        self.username_edit = QLineEdit()
        layout.addWidget(self.username_edit)

        # كلمة المرور
        layout.addWidget(QLabel("Password:"))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)

        # الدور
        layout.addWidget(QLabel("Role:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(["user", "admin", "developer", "owner"])
        layout.addWidget(self.role_combo)

        # الصلاحيات
        layout.addWidget(QLabel("Permissions:"))
        self.can_add_checkbox = QCheckBox("Can Add")
        self.can_edit_checkbox = QCheckBox("Can Edit")
        self.can_delete_checkbox = QCheckBox("Can Delete")
        layout.addWidget(self.can_add_checkbox)
        layout.addWidget(self.can_edit_checkbox)
        layout.addWidget(self.can_delete_checkbox)

        # أزرار الحفظ والإلغاء
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept_data)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # إذا كانت بيانات المستخدم موجودة، نملأ الحقول
        if user_record:
            self.username_edit.setText(user_record.get("username", ""))
            self.password_edit.setText("")  # لا نعرض كلمة المرور الحالية
            self.role_combo.setCurrentText(user_record.get("role", "user"))
            self.can_add_checkbox.setChecked(user_record.get("can_add", False))
            self.can_edit_checkbox.setChecked(user_record.get("can_edit", False))
            self.can_delete_checkbox.setChecked(user_record.get("can_delete", False))

    def accept_data(self):
        """
        التحقق من صحة البيانات وإرجاعها.
        """
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        role = self.role_combo.currentText()
        can_add = self.can_add_checkbox.isChecked()
        can_edit = self.can_edit_checkbox.isChecked()
        can_delete = self.can_delete_checkbox.isChecked()

        if not username:
            QMessageBox.warning(self, "Warning", "Username cannot be empty.")
            return
        if not self.user_record and not password:
            QMessageBox.warning(self, "Warning", "Password cannot be empty for new user.")
            return

        self.data = {
            "username": username,
            "password": password,
            "role": role,
            "can_add": can_add,
            "can_edit": can_edit,
            "can_delete": can_delete
        }
        self.accept()

    def get_data(self):
        """
        إرجاع البيانات بعد الحفظ.
        """
        return self.data
