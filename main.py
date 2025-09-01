"""
main.py - نقطة تشغيل مشروع shihabi2

يقوم بتهيئة التطبيق، عرض نافذة تسجيل الدخول، ثم تحميل الواجهة الرئيسية بناءً على صلاحيات المستخدم.
تم التحديث لدمج تصميم واجهة تسجيل الدخول الجديد (LoginWindow) مع الحفاظ على منطق إنشاء الحسابات الافتراضية.
"""

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

# استيراد مدير قاعدة البيانات
from modules.database import DatabaseManager

# استيراد النوافذ
from modules.login_window import LoginWindow  # النسخة الجديدة من نافذة تسجيل الدخول
from modules.main_window import MainWindow


def create_default_accounts(db: DatabaseManager):
    """
    إنشاء الحسابات الافتراضية عند أول تشغيل:
    - حساب المبرمج (developer) خاص بك أنت فقط.
    - حساب صاحب الكراج (owner).
    """
    try:
        db.create_user(
            username="saif103",  # حساب المبرمج
            password="Rnj103",   # كلمة مرور قوية وخاصة بك
            role="developer",
            can_add=True,
            can_edit=True,
            can_delete=True
        )
    except Exception:
        # الحساب موجود مسبقًا أو تم منعه بسبب وجود مطوّر آخر
        pass

    try:
        db.create_user(
            username="garage_owner",  # صاحب الكراج
            password="owner123",
            role="owner",
            can_add=True,
            can_edit=True,
            can_delete=True
        )
    except Exception:
        # الحساب موجود مسبقًا
        pass


def launch_app():
    """
    تشغيل التطبيق: تسجيل الدخول ثم تحميل الواجهة الرئيسية.
    """
    app = QApplication(sys.argv)
    db = DatabaseManager()

    # إنشاء الحسابات الافتراضية إذا لم تكن موجودة
    create_default_accounts(db)

    # عرض نافذة تسجيل الدخول الجديدة
    login_dialog = LoginWindow(db)
    if login_dialog.exec_() == login_dialog.Accepted:
        user = login_dialog.get_user()
        if user:
            # تمرير بيانات المستخدم إلى MainWindow
            window = MainWindow(user, db)
            window.show()
            sys.exit(app.exec_())
        else:
            QMessageBox.critical(None, "خطأ", "تعذر تحميل بيانات المستخدم.")
    else:
        QMessageBox.information(None, "إغلاق", "تم إلغاء تسجيل الدخول.")
        sys.exit()


if __name__ == "__main__":
    launch_app()