"""
archive_dialog_window.py - نافذة عرض الأرشيف
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt

class ArchiveDialog(QDialog):
    """
    نافذة الأرشيف: عرض جميع العناصر التي تم حذفها أو تصديرها.
    """

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Archive")
        self.setFixedSize(700, 500)
        self.setStyleSheet("""
            QTableWidget {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #ccc;
                gridline-color: #bbb;
                font-size: 13px;
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

        # 🌟 جدول الأرشيف
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # 🌟 أزرار
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_archive)
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # تحميل البيانات عند الفتح
        self.load_archive()

    def load_archive(self):
        """
        تحميل بيانات الأرشيف من قاعدة البيانات وعرضها في الجدول.
        """
        try:
            items = self.db.get_archived_items()
            headers = ["Name", "Part Number", "Quantity", "Barcode", "Condition", "Deleted At"]
            self.table.setRowCount(0)
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)

            for row, item in enumerate(items):
                self.table.insertRow(row)
                for col, value in enumerate(item):
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))

            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load archive.\n{str(e)}")
