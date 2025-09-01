"""
utils.py - أدوات مساعدة عامة للمشروع
"""

import re
from PyQt5.QtWidgets import QMessageBox


def show_info(parent, title, message):
    """
    عرض رسالة معلومات.
    """
    QMessageBox.information(parent, title, message)


def show_warning(parent, title, message):
    """
    عرض رسالة تحذير.
    """
    QMessageBox.warning(parent, title, message)


def show_error(parent, title, message):
    """
    عرض رسالة خطأ.
    """
    QMessageBox.critical(parent, title, message)


def validate_integer(value, min_val=None, max_val=None):
    """
    التحقق من أن القيمة عدد صحيح صالح ضمن الحدود.
    """
    try:
        num = int(value)
        if min_val is not None and num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        return True
    except ValueError:
        return False


def validate_float(value, min_val=None, max_val=None):
    """
    التحقق من أن القيمة عدد عشري صالح ضمن الحدود.
    """
    try:
        num = float(value)
        if min_val is not None and num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        return True
    except ValueError:
        return False


def validate_text(value, allow_empty=False, pattern=None):
    """
    التحقق من أن النص صالح.
    - allow_empty: هل مسموح أن يكون فارغ؟
    - pattern: تعبير منتظم (Regex) للتحقق من النمط (مثل الباركود).
    """
    if not value and not allow_empty:
        return False
    if pattern:
        return bool(re.match(pattern, value))
    return True


def validate_barcode(value):
    """
    التحقق من صحة الباركود (أرقام فقط، من 6 إلى 20 رقم).
    """
    return bool(re.match(r"^[0-9]{6,20}$", value.strip()))


def normalize_text(value):
    """
    تنسيق النصوص: إزالة الفراغات الزائدة + جعل أول حرف كبير.
    """
    return value.strip().capitalize()


def format_number(value):
    """
    تنسيق الرقم بشكل مرتب (يفصل الألوف).
    """
    try:
        return f"{int(value):,}"
    except ValueError:
        return value


def safe_get(data, index, default=""):
    """
    استرجاع قيمة من قائمة أو Tuple بشكل آمن.
    """
    try:
        return data[index]
    except (IndexError, TypeError):
        return default
