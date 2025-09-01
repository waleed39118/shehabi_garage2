from PyQt5 import QtWidgets, QtGui, QtCore

class Ui_LoginWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("LoginWindow")
        Dialog.resize(520, 460)
        Dialog.setWindowTitle("تسجيل الدخول")

        # التخطيط الرئيسي: عمودي (محتوى + فوتر)
        self.mainLayout = QtWidgets.QVBoxLayout(Dialog)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # ---------------- قسم المحتوى مع الخلفية ----------------
        self.contentWidget = QtWidgets.QWidget(Dialog)
        self.contentWidget.setStyleSheet("""
            QWidget {
                background-image: url('assets/logo_login.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
            }
        """)
        self.contentLayout = QtWidgets.QVBoxLayout(self.contentWidget)
        self.contentLayout.setContentsMargins(20, 20, 20, 20)
        self.contentLayout.setSpacing(12)

        # شعار فوق الحقول
        self.logoLabel = QtWidgets.QLabel(self.contentWidget)
        self.logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        logo_pixmap = QtGui.QPixmap("assets/shehabi_logo.jpg").scaled(
            180, 180, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        self.logoLabel.setPixmap(logo_pixmap)
        self.contentLayout.addWidget(self.logoLabel)

        # حقول الإدخال
        self.username = QtWidgets.QLineEdit(self.contentWidget)
        self.username.setPlaceholderText("اسم المستخدم")
        self.username.setClearButtonEnabled(True)

        self.password = QtWidgets.QLineEdit(self.contentWidget)
        self.password.setPlaceholderText("كلمة المرور")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setClearButtonEnabled(True)

        fields_css = """
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 2px solid #1E90FF;
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.9);
            }
            QLineEdit:focus {
                border-color: #0F6AD8;
                background: rgba(255, 255, 255, 1.0);
            }
        """
        self.username.setStyleSheet(fields_css)
        self.password.setStyleSheet(fields_css)

        self.contentLayout.addWidget(self.username)
        self.contentLayout.addWidget(self.password)

        # صف الأزرار (دخول + إلغاء)
        self.buttonsRow = QtWidgets.QHBoxLayout()
        self.buttonsRow.addStretch(1)

        self.loginButton = QtWidgets.QPushButton("دخول", self.contentWidget)
        self.loginButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loginButton.setMinimumHeight(40)
        self.loginButton.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                font-weight: bold;
                font-size: 15px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #1877E6; }
            QPushButton:pressed { background-color: #0F6AD8; }
        """)
        self.buttonsRow.addWidget(self.loginButton)

        self.cancelButton = QtWidgets.QPushButton("إلغاء", self.contentWidget)
        self.cancelButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelButton.setMinimumHeight(40)
        self.cancelButton.setStyleSheet("""
            QPushButton {
                background-color: #B22222;
                color: white;
                font-weight: bold;
                font-size: 15px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #8B0000; }
            QPushButton:pressed { background-color: #A52A2A; }
        """)
        self.buttonsRow.addWidget(self.cancelButton)

        self.contentLayout.addLayout(self.buttonsRow)

        # إضافة المحتوى إلى التخطيط الرئيسي
        self.mainLayout.addWidget(self.contentWidget, stretch=1)

        # ---------------- قسم الفوتر ----------------
        self.footerWidget = QtWidgets.QWidget(Dialog)
        self.footerWidget.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.7);
            }
        """)
        self.footerLayout = QtWidgets.QVBoxLayout(self.footerWidget)
        self.footerLayout.setContentsMargins(0, 5, 0, 5)

        self.footerLabel = QtWidgets.QLabel("إعداد و تصميم المبرمج / وليد جابر سالم", self.footerWidget)
        self.footerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.footerLabel.setStyleSheet("""
            QLabel {
                color: #FFD700;
                font-weight: 700;
                font-size: 15px;
            }
        """)
        self.footerLayout.addWidget(self.footerLabel)

        self.mainLayout.addWidget(self.footerWidget, stretch=0)