# statistics_dialog_window_ui.py
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class StatisticsDialog(QDialog):
    """
    نافذة عرض الإحصائيات الرئيسية للمخزن.
    """

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Inventory Statistics")
        self.setFixedSize(400, 300)
        self.setup_ui()
        self.load_statistics()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # عنوان الإحصائيات
        self.title_label = QLabel("Inventory Statistics")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.title_label)

        # جدول الإحصائيات
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["Statistic", "Value"])
        self.stats_table.horizontalHeader().setStretchLastSection(True)
        self.stats_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.stats_table)

        self.setLayout(layout)

    def load_statistics(self):
        """
        تحميل الإحصائيات من قاعدة البيانات وعرضها في الجدول.
        """
        try:
            items = self.db.get_inventory()  # قائمة عناصر المخزن
        except Exception as e:
            self.stats_table.setRowCount(0)
            return

        # حساب الإحصائيات
        total_items = len(items)
        total_quantity = 0
        new_items = 0
        used_items = 0

        for item in items:
            # التأكد من وجود الأعمدة اللازمة
            quantity = 0
            condition = ""
            if len(item) >= 3:
                try:
                    quantity = int(item[2])
                except (ValueError, TypeError):
                    quantity = 0
            if len(item) >= 5:
                condition = str(item[4]).lower()

            total_quantity += quantity
            if condition == "new":
                new_items += 1
            elif condition == "used":
                used_items += 1

        stats = [
            ("Total Items", total_items),
            ("Total Quantity", total_quantity),
            ("New Items", new_items),
            ("Used Items", used_items)
        ]

        # عرض الإحصائيات في الجدول
        self.stats_table.setRowCount(len(stats))
        for row_index, (stat_name, value) in enumerate(stats):
            self.stats_table.setItem(row_index, 0, QTableWidgetItem(str(stat_name)))
            self.stats_table.setItem(row_index, 1, QTableWidgetItem(str(value)))
