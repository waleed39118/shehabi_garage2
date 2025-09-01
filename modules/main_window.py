# modules/main_window.py
import csv
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QFileDialog, QDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from ui.main_window_ui import Ui_MainWindow
from modules.utils import normalize_text, show_warning, show_error, show_info

# الحوارات
from modules.item_dialog_window import ItemDialog
from modules.outgoing_dialog_window import OutgoingDialog
from modules.statistics_dialog_window import StatisticsDialog
from modules.settings_dialog_window import SettingsDialog
from modules.manage_users_window import ManageUsersDialog

# الأرشيف (اختياري)
ArchiveDialog = None
Ui_ArchiveDialog = None
try:
    from modules.archive_dialog_window import ArchiveDialog
except Exception:
    pass
try:
    from ui.archive_dialog_window_ui import Ui_ArchiveDialog
except Exception:
    try:
        from modules.archive_dialog_window import Ui_ArchiveDialog
    except Exception:
        pass

def apply_app_theme(widget):
    """تطبيق ثيم عصري على الواجهة"""
    widget.setStyleSheet("""
        QWidget { background-color: #f5f7fb; }
        QTableWidget { background: white; border-radius: 10px; border: 1px solid #d0d7de; gridline-color: #d0d7de; }
        QHeaderView::section { background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #1E90FF, stop:1 #1877E6); color: white; font-weight: bold; padding: 6px; border: none; }
        QTableWidget::item { padding: 4px; }
        QTableWidget::item:selected { background: #1E90FF; color: white; }
        QPushButton { background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #1E90FF, stop:1 #0F6AD8); color: white; font-weight: 600; padding: 8px 14px; border-radius: 8px; }
        QPushButton:hover { background: #1877E6; }
        QPushButton:pressed { background: #0F6AD8; }
        QLineEdit { background: white; border: 2px solid #1E90FF; border-radius: 8px; padding: 8px; }
        QLineEdit:focus { border-color: #0F6AD8; background: #f0f6ff; }
    """)

class MainWindow(QMainWindow):
    def __init__(self, user, db):
        super().__init__()
        self.db = db
        self.user = user
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # شعار overlay
        self.logoOverlay = QLabel(self)
        pixmap = QtGui.QPixmap("assets/shehabi_logo.jpg").scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logoOverlay.setPixmap(pixmap)
        self.logoOverlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.logoOverlay.setStyleSheet("background: transparent;")
        self.logoOverlay.show()
        self._position_overlay_logo()

        # ربط الأزرار
        self.ui.buttonObjects["Add Item"].clicked.connect(self.add_item)
        self.ui.buttonObjects["Record Outgoing"].clicked.connect(self.record_outgoing)
        self.ui.buttonObjects["Edit Item"].clicked.connect(self.edit_item)
        self.ui.buttonObjects["Delete Item"].clicked.connect(self.delete_item)
        self.ui.buttonObjects["Refresh"].clicked.connect(self.load_inventory)
        self.ui.buttonObjects["Statistics"].clicked.connect(self.show_statistics)
        self.ui.buttonObjects["Archive"].clicked.connect(self.show_archive)
        self.ui.buttonObjects["Users"].clicked.connect(self.manage_users)
        self.ui.buttonObjects["Settings"].clicked.connect(self.open_settings)
        self.ui.buttonObjects["Print"].clicked.connect(self.print_inventory)
        self.ui.buttonObjects["Export"].clicked.connect(self.export_inventory)
        self.ui.searchBox.textChanged.connect(self.filter_inventory)

        # تحميل البيانات
        self.load_inventory()

        # تطبيق الثيم
        apply_app_theme(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._position_overlay_logo()

    def _position_overlay_logo(self):
        margin = 12
        if not self.logoOverlay.pixmap():
            return
        w = self.logoOverlay.pixmap().width()
        x = self.width() - w - margin - (self.frameGeometry().width() - self.geometry().width())
        self.logoOverlay.move(max(margin, x), margin)

    # ---------------------- بيانات المخزون ----------------------
    def load_inventory(self):
        table = self.ui.tableInventory
        table.setRowCount(0)
        try:
            items = self.db.get_inventory()
            for row_index, item in enumerate(items):
                table.insertRow(row_index)
                if isinstance(item, dict):
                    name = str(item.get("name", ""))
                    part = str(item.get("part_number", ""))
                    qty = item.get("quantity", 0)
                    location = str(item.get("location", ""))
                    cond = str(item.get("condition", ""))
                    updated = str(item.get("last_updated", ""))
                else:
                    name = str(item[0]) if len(item) > 0 else ""
                    part = str(item[1]) if len(item) > 1 else ""
                    qty = item[2] if len(item) > 2 else 0
                    location = str(item[3]) if len(item) > 3 else ""
                    cond = str(item[4]) if len(item) > 4 else ""
                    updated = str(item[5]) if len(item) > 5 else ""

                table.setItem(row_index, 0, QTableWidgetItem(name))
                table.setItem(row_index, 1, QTableWidgetItem(part))
                table.setItem(row_index, 2, QTableWidgetItem(str(qty)))
                table.setItem(row_index, 3, QTableWidgetItem(location))
                table.setItem(row_index, 4, QTableWidgetItem(cond))
                table.setItem(row_index, 5, QTableWidgetItem(updated))
        except Exception as e:
            show_error(self, "Error", f"Failed to load inventory.\n{str(e)}")

    def filter_inventory(self, text: str):
        text = (text or "").strip().lower()
        table = self.ui.tableInventory
        for row in range(table.rowCount()):
            match = False
            for col in range(table.columnCount()):
                cell = table.item(row, col)
                if cell and text in cell.text().lower():
                    match = True
                    break
            table.setRowHidden(row, not match)

    # ---------------------- CRUD ----------------------
    def add_item(self):
        if not self.user.get("can_add", False):
            show_warning(self, "Access Denied", "You do not have permission to add items.")
            return
        dialog = ItemDialog(self)
        apply_app_theme(dialog)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                if "name" in data: data["name"] = normalize_text(str(data["name"]))
                if "part_number" in data: data["part_number"] = data["part_number"].strip()
                if "location" in data: data["location"] = data["location"].strip()
                self.db.add_inventory_item(data)
                show_info(self, "Success", "Item added successfully.")
                self.load_inventory()
            except Exception as e:
                show_error(self, "Error", f"Failed to add item.\n{str(e)}")

    def edit_item(self):
        if not self.user.get("can_edit", False):
            show_warning(self, "Access Denied", "You do not have permission to edit items.")
            return
        table = self.ui.tableInventory
        row = table.currentRow()
        if row == -1:
            show_warning(self, "Warning", "Please select an item to edit.")
            return
        part_item = table.item(row, 1)
        if not part_item:
            show_error(self, "Error", "Selected row is missing a part number.")
            return
        part_number = part_item.text()
        item_record = self.db.get_item_by_part(part_number)
        if not item_record:
            show_error(self, "Error", "Selected item not found.")
            return
        dialog = ItemDialog(self, item_record)
        apply_app_theme(dialog)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                if "name" in data: data["name"] = normalize_text(str(data["name"]))
                if "part_number" in data: data["part_number"] = data["part_number"].strip()
                if "location" in data: data["location"] = data["location"].strip()
                self.db.update_inventory_item(part_number, data)
                show_info(self, "Success", "Item updated successfully.")
                self.load_inventory()
            except Exception as e:
                show_error(self, "Error", f"Failed to update item.\n{str(e)}")

    def delete_item(self):
        if not self.user.get("can_delete", False):
            show_warning(self, "Access Denied", "You do not have permission to delete items.")
            return
        table = self.ui.tableInventory
        row = table.currentRow()
        if row == -1:
            show_warning(self, "Warning", "Please select an item to delete.")
            return
        part_item = table.item(row, 1)
        if not part_item:
            show_error(self, "Error", "Selected row is missing a part number.")
            return
        part_number = part_item.text()
        confirm = QMessageBox.question(self, "Confirm Deletion",
            f"Are you sure you want to delete item '{part_number}'?",
            QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                self.db.delete_inventory_item(part_number)
                show_info(self, "Deleted", "Item deleted successfully.")
                self.load_inventory()
            except Exception as e:
                show_error(self, "Error", f"Failed to delete item.\n{str(e)}")

    # ---------------------- عمليات أخرى ----------------------
    def record_outgoing(self):
        if not self.user.get("can_edit", False):
            show_warning(self, "Access Denied", "You do not have permission to record outgoing items.")
            return
        dialog = OutgoingDialog(self)
        apply_app_theme(dialog)
        if dialog.exec_() == QDialog.Accepted:
            try:
                part, qty, condition = dialog.get_data()
                self.db.record_outgoing_item(part, qty, condition)
                show_info(self, "Success", "Outgoing recorded successfully.")
                self.load_inventory()
            except Exception as e:
                show_error(self, "Error", f"Failed to record outgoing.\n{str(e)}")

    def show_statistics(self):
        dialog = StatisticsDialog(self.db, self)
        apply_app_theme(dialog)
        dialog.exec_()

    def show_archive(self):
        try:
            if ArchiveDialog is not None:
                dialog = ArchiveDialog(self.db, self)
                apply_app_theme(dialog)
                dialog.exec_()
            elif Ui_ArchiveDialog is not None:
                dlg = QDialog(self)
                ui = Ui_ArchiveDialog()
                ui.setupUi(dlg)
                apply_app_theme(dlg)
                dlg.exec_()
            else:
                QMessageBox.information(self, "Info", "Archive feature is not available.")
        except Exception as e:
            show_error(self, "Error", f"Failed to open archive.\n{str(e)}")

    def manage_users(self):
        role = self.user.get("role", "user")
        if role not in ("developer", "admin", "owner"):
            show_warning(self, "Access Denied", "You do not have permission to manage users.")
            return
        dialog = ManageUsersDialog(self.db, role, self)
        apply_app_theme(dialog)
        dialog.exec_()

    def open_settings(self):
        dialog = SettingsDialog(self)
        apply_app_theme(dialog)
        dialog.exec_()

    def print_inventory(self):
        show_info(self, "Print", "Printing functionality is not implemented yet.")

    def export_inventory(self):
        try:
            path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
            if not path: return
            table = self.ui.tableInventory
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                headers = [table.horizontalHeaderItem(i).text() if table.horizontalHeaderItem(i) else "" for i in range(table.columnCount())]
                writer.writerow(headers)
                for row in range(table.rowCount()):
                    row_data = [table.item(row, col).text() if table.item(row, col) else "" for col in range(table.columnCount())]
                    writer.writerow(row_data)
            show_info(self, "Export", "Inventory exported successfully.")
        except Exception as e:
            show_error(self, "Error", f"Failed to export inventory.\n{str(e)}")
