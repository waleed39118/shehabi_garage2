from PyQt5 import QtWidgets

class Ui_ArchiveDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("ArchiveDialog")
        Dialog.resize(600, 400)

        self.tableArchive = QtWidgets.QTableWidget(Dialog)
        self.tableArchive.setGeometry(20, 20, 560, 360)