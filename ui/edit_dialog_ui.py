from PyQt5 import QtWidgets

class Ui_EditDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("EditDialog")
        Dialog.resize(300, 200)

        self.txtName = QtWidgets.QLineEdit(Dialog)
        self.txtName.setGeometry(80, 20, 200, 25)

        self.txtPart = QtWidgets.QLineEdit(Dialog)
        self.txtPart.setGeometry(80, 55, 200, 25)

        self.spinQuantity = QtWidgets.QSpinBox(Dialog)
        self.spinQuantity.setGeometry(80, 90, 200, 25)
        self.spinQuantity.setRange(0, 100000)

        self.txtLocation = QtWidgets.QLineEdit(Dialog)
        self.txtLocation.setGeometry(80, 125, 200, 25)

        self.btnOk = QtWidgets.QPushButton("Save", Dialog)
        self.btnOk.setGeometry(80, 160, 90, 30)

        self.btnCancel = QtWidgets.QPushButton("Cancel", Dialog)
        self.btnCancel.setGeometry(190, 160, 90, 30)