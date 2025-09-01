"""
statistics_dialog_window.py - نافذة إحصائيات الجرد
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class StatisticsDialog(QDialog):
    """
    نافذة عرض الإحصائيات الرئيسية للمخزن.
    """

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Inventory Statistics")
        self.setFixedSize(400, 400)
        self.setStyleSheet("""
            QLabel {
                font-size: 13px;
            }
            QTableWidget {
                border: 1px solid #ccc;
                gridline-color: #bbb;
                font-size: 13px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # 🌟 عنوان الإحصائيات
        self.title_label = QLabel("Inventory Statistics")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.title_label)

        # 🌟 جدول الإحصائيات
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["Statistic", "Value"])
        self.stats_table.horizontalHeader().setStretchLastSection(True)
        self.stats_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.stats_table)

        self.setLayout(layout)

        # تحميل وعرض الإحصائيات
        self.load_statistics()

    def load_statistics(self):
        """
        تحميل الإحصائيات من قاعدة البيانات وعرضها في الجدول.
        """
        items = self.db.get_inventory()

        total_items = len(items)
        total_quantity = sum(int(item[2]) for item in items)
        new_items = sum(1 for item in items if len(item) >=5 and item[4].lower() == "new")
        used_items = sum(1 for item in items if len(item) >=5 and item[4].lower() == "used")

        stats = [
            ("Total Items", total_items),
            ("Total Quantity", total_quantity),
            ("New Items", new_items),
            ("Used Items", used_items)
        ]

        self.stats_table.setRowCount(len(stats))
        for row, (stat, value) in enumerate(stats):
            self.stats_table.setItem(row, 0, QTableWidgetItem(str(stat)))
            self.stats_table.setItem(row, 1, QTableWidgetItem(str(value)))
