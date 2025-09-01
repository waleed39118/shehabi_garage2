from PyQt5 import QtWidgets, QtGui, QtCore

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1150, 750)
        MainWindow.setWindowTitle("Shihabi2 Inventory System")

        # ---------------- Central Widget ----------------
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralWidget)

        # -------- Layout رئيسي: بانل يسار + محتوى يمين --------
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # ---------------- بانل جانبي يسار للأزرار ----------------
        self.sidePanel = QtWidgets.QFrame(self.centralWidget)
        self.sidePanel.setFixedWidth(220)
        self.sidePanel.setStyleSheet("background-color: #F8F9FA;")
        self.sideLayout = QtWidgets.QVBoxLayout(self.sidePanel)
        self.sideLayout.setContentsMargins(15, 20, 15, 20)
        self.sideLayout.setSpacing(12)

        # قائمة الأزرار مع أيقونات
        buttons = [
            ("Add Item", "assets/icon_add.png"),
            ("Record Outgoing", "assets/icon_outgoing.png"),
            ("Edit Item", "assets/icon_edit.png"),
            ("Delete Item", "assets/icon_delete.png"),
            ("Refresh", "assets/icon_refresh.png"),
            ("Statistics", "assets/icon_stats.png"),
            ("Archive", "assets/icon_archive.png"),
            ("Users", "assets/icon_users.png"),
            ("Settings", "assets/icon_settings.png"),
            ("Print", "assets/icon_print.png"),
            ("Export", "assets/icon_export.png"),
        ]

        self.buttonObjects = {}
        for text, icon in buttons:
            btn = QtWidgets.QPushButton(text)
            btn.setIcon(QtGui.QIcon(icon))
            btn.setIconSize(QtCore.QSize(28, 28))
            btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1E90FF;
                    color: white;
                    font-weight: 600;
                    padding: 12px;
                    border-radius: 10px;
                    text-align: left;
                }
                QPushButton:hover { background-color: #4682B4; }
                QPushButton:pressed { background-color: #104E8B; }
            """)
            self.sideLayout.addWidget(btn)
            self.buttonObjects[text] = btn
        self.sideLayout.addStretch(1)
        self.mainLayout.addWidget(self.sidePanel)

        # ---------------- المنطقة الرئيسية (يمين) ----------------
        self.rightWidget = QtWidgets.QWidget(self.centralWidget)
        self.rightLayout = QtWidgets.QVBoxLayout(self.rightWidget)
        self.rightLayout.setContentsMargins(15, 15, 15, 15)
        self.rightLayout.setSpacing(15)
        self.mainLayout.addWidget(self.rightWidget)

        # ---------------- شريط علوي بخلفية متجاوبة ----------------
        self.topHeader = QtWidgets.QWidget(self.rightWidget)
        self.topHeader.setFixedHeight(180)
        self.rightLayout.addWidget(self.topHeader)

        # استخدام QStackedLayout لطبقة الخلفية والمحتوى
        self.topHeaderLayout = QtWidgets.QStackedLayout(self.topHeader)
        self.topHeaderLayout.setContentsMargins(0, 0, 0, 0)

        # خلفية الصورة
        self.bgLabel = QtWidgets.QLabel(self.topHeader)
        self.bgPixmap = QtGui.QPixmap("assets/garage_bg.jpg")
        self.bgLabel.setScaledContents(True)
        self.bgLabel.setPixmap(self.bgPixmap)
        self.topHeaderLayout.addWidget(self.bgLabel)

        # محتوى الشريط (العنوان فقط، بدون شعار)
        self.headerContent = QtWidgets.QWidget(self.topHeader)
        contentLayout = QtWidgets.QHBoxLayout(self.headerContent)
        contentLayout.setContentsMargins(20, 10, 20, 10)

        # العنوان
        self.titleLabel = QtWidgets.QLabel("Shihabi2 Inventory System")
        self.titleLabel.setStyleSheet("font-size: 24pt; font-weight: bold; color: white;")
        contentLayout.addWidget(self.titleLabel, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        contentLayout.addStretch()
        self.topHeaderLayout.addWidget(self.headerContent)
        self.topHeaderLayout.setCurrentWidget(self.headerContent)

        # ---------------- شريط البحث ----------------
        self.searchBox = QtWidgets.QLineEdit(self.rightWidget)
        self.searchBox.setPlaceholderText("🔍 Search by name, part number, location, or condition...")
        self.searchBox.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #1E90FF;
                border-radius: 10px;
                padding: 10px;
                font-size: 11pt;
            }
            QLineEdit:focus { border-color: #0F6AD8; background: #f0f6ff; }
        """)
        self.rightLayout.addWidget(self.searchBox)

        # ---------------- جدول المخزون ----------------
        self.tableInventory = QtWidgets.QTableWidget(self.rightWidget)
        self.tableInventory.setColumnCount(6)
        self.tableInventory.setHorizontalHeaderLabels(
            ["Name", "Part Number", "Quantity", "Location", "Condition", "Last Updated"]
        )
        self.tableInventory.horizontalHeader().setStretchLastSection(True)
        self.tableInventory.setAlternatingRowColors(True)
        self.tableInventory.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableInventory.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableInventory.setSelectionMode(QtWidgets.QTableWidget.SingleSelection)
        self.tableInventory.verticalHeader().setVisible(False)
        self.tableInventory.setStyleSheet("""
            QTableWidget { background: white; border-radius: 12px; gridline-color: #d0d7de; }
            QHeaderView::section {
                background-color: #1E90FF; color: white; font-weight: bold; padding: 6px; border: none;
            }
            QTableWidget::item:selected { background-color: #1E90FF; color: white; }
        """)
        self.rightLayout.addWidget(self.tableInventory)

        # ---------------- شريط الفوتر ----------------
        self.footerWidget = QtWidgets.QWidget(self.rightWidget)
        self.footerWidget.setStyleSheet("background-color: rgba(0,0,0,0.85);")
        footerLayout = QtWidgets.QVBoxLayout(self.footerWidget)
        footerLayout.setContentsMargins(0, 5, 0, 5)
        self.footerLabel = QtWidgets.QLabel("إعداد و برمجة: وليد جابر سالم", self.footerWidget)
        self.footerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.footerLabel.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 14px;")
        footerLayout.addWidget(self.footerLabel)
        self.rightLayout.addWidget(self.footerWidget)

        # ---------------- شريط الحالة ----------------
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusBar)

        # ---------------- ستايل عام ----------------
        MainWindow.setStyleSheet("""
            QWidget { background-color: #F4F7FB; font-family: 'Segoe UI'; font-size: 10pt; }
            QPushButton { pointer; }
        """)

    # ----------------- تحديث الخلفية تلقائيًا عند تغيير الحجم -----------------
    def resizeEvent(self, event):
        if hasattr(self, 'bgLabel') and self.bgPixmap:
            self.bgLabel.setPixmap(self.bgPixmap.scaled(
                self.topHeader.width(),
                self.topHeader.height(),
                QtCore.Qt.KeepAspectRatioByExpanding,
                QtCore.Qt.SmoothTransformation
            ))
        QtWidgets.QWidget.resizeEvent(self, event)
