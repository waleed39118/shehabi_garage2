"""
نافذة تسجيل الدخول - نسخة محدثة
- تعتمد على واجهة UI في: ui/login_window_ui.py
- تعديلات:
  1) إضافة أيقونات لأزرار الدخول والإلغاء.
  2) الحفاظ على حفظ بيانات المستخدم وخاصية قفل حساب المبرمج.
"""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from ui.login_window_ui import Ui_LoginWindow
from modules.utils import show_error, show_warning, show_info


class LoginWindow(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.user = None
        self._developer_locked = False

        # تهيئة الواجهة
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        # إضافة أيقونات للأزرار
        self.ui.loginButton.setIcon(QIcon("assets/icon_login.png"))
        self.ui.cancelButton.setIcon(QIcon("assets/icon_cancel.png"))

        # ربط الأزرار
        self.ui.loginButton.clicked.connect(self.handle_login)
        self.ui.cancelButton.clicked.connect(self.reject)

        # دعم الضغط على Enter في الحقول
        self.ui.username.returnPressed.connect(self.handle_login)
        self.ui.password.returnPressed.connect(self.handle_login)

    def handle_login(self):
        """التحقق من بيانات الدخول وتنفيذ إجراءات ما بعد النجاح/الفشل."""
        username = self.ui.username.text().strip()
        password = self.ui.password.text().strip()

        if not username or not password:
            show_warning(self, "تنبيه", "يرجى إدخال اسم المستخدم وكلمة المرور.")
            return

        try:
            user_record = self.db.authenticate_user(username, password)
            if not user_record:
                show_error(self, "خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة.")
                return

            self.user = user_record
            self._developer_locked = (user_record.get("role") == "developer")

            show_info(self, "نجاح", f"مرحباً {username}")
            self.accept()
        except Exception as e:
            show_error(self, "خطأ", f"حدث خطأ أثناء تسجيل الدخول:\n{str(e)}")

    def get_user(self):
        """إرجاع بيانات المستخدم بعد تسجيل الدخول."""
        return self.user

    def is_developer_locked(self):
        """إرجاع حالة قفل حساب المبرمج."""
        return self._developer_locked