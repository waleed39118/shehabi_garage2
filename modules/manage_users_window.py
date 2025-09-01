"""
manage_users_window.py - نافذة إدارة المستخدمين
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ManageUsersDialog(QDialog):
    """
    نافذة لإدارة المستخدمين: عرض، إضافة، تعديل وحذف مع دعم الصلاحيات.
    """

    def __init__(self, db, current_role, parent=None):
        super().__init__(parent)
        self.db = db
        self.current_role = current_role
        self.setWindowTitle("Manage Users")
        self.setMinimumSize(700, 400)
        self.setStyleSheet("""
            QTableWidget {
                font-size: 13px;
                background: rgba(255, 255, 255, 0.9);
                gridline-color: #bbb;
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

        # جدول المستخدمين
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Username", "Role", "Can Add", "Can Edit", "Can Delete", "Last Login"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # أزرار التحكم
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add User")
        self.add_btn.clicked.connect(self.add_user)
        self.edit_btn = QPushButton("Edit User")
        self.edit_btn.clicked.connect(self.edit_user)
        self.delete_btn = QPushButton("Delete User")
        self.delete_btn.clicked.connect(self.delete_user)
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_users)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.refresh_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.load_users()

    def load_users(self):
        """
        تحميل بيانات المستخدمين وعرضها في الجدول.
        """
        self.table.setRowCount(0)
        try:
            users = self.db.get_users()
            for row_index, user in enumerate(users):
                self.table.insertRow(row_index)
                self.table.setItem(row_index, 0, QTableWidgetItem(user["username"]))
                self.table.setItem(row_index, 1, QTableWidgetItem(user["role"]))
                self.table.setItem(row_index, 2, QTableWidgetItem(str(user.get("can_add", False))))
                self.table.setItem(row_index, 3, QTableWidgetItem(str(user.get("can_edit", False))))
                self.table.setItem(row_index, 4, QTableWidgetItem(str(user.get("can_delete", False))))
                self.table.setItem(row_index, 5, QTableWidgetItem(user.get("last_login", "")))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load users.\n{str(e)}")

    def add_user(self):
        """
        فتح نافذة لإضافة مستخدم جديد.
        """
        if self.current_role not in ("admin", "developer", "owner"):
            QMessageBox.warning(self, "Access Denied", "You do not have permission to add users.")
            return

        dialog = UserEditDialog(parent=self)
        if dialog.exec_():
            data = dialog.get_data()
            try:
                self.db.add_user(data)
                QMessageBox.information(self, "Success", "User added successfully.")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add user.\n{str(e)}")

    def edit_user(self):
        """
        فتح نافذة لتعديل مستخدم محدد.
        """
        if self.current_role not in ("admin", "developer", "owner"):
            QMessageBox.warning(self, "Access Denied", "You do not have permission to edit users.")
            return

        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Warning", "Please select a user to edit.")
            return

        username = self.table.item(row, 0).text()
        user_record = self.db.get_user_by_username(username)
        if not user_record:
            QMessageBox.warning(self, "Error", "Selected user does not exist.")
            return

        dialog = UserEditDialog(user_record, parent=self)
        if dialog.exec_():
            data = dialog.get_data()
            try:
                self.db.update_user(username, data)
                QMessageBox.information(self, "Success", "User updated successfully.")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update user.\n{str(e)}")

    def delete_user(self):
        """
        حذف المستخدم المحدد بعد التأكيد.
        """
        if self.current_role not in ("admin", "developer", "owner"):
            QMessageBox.warning(self, "Access Denied", "You do not have permission to delete users.")
            return

        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Warning", "Please select a user to delete.")
            return

        username = self.table.item(row, 0).text()
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete user '{username}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                self.db.delete_user(username)
                QMessageBox.information(self, "Deleted", "User deleted successfully.")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete user.\n{str(e)}")

# ملاحظة: UserEditDialog يجب أن يكون نافذة لإدخال بيانات المستخدم (اسم، كلمة مرور، الدور، صلاحيات)
