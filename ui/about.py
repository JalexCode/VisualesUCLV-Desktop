# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(623, 231)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.app_name = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.app_name.setFont(font)
        self.app_name.setObjectName("app_name")
        self.gridLayout_2.addWidget(self.app_name, 0, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.tab)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.colaborators = QtWidgets.QPlainTextEdit(self.widget_2)
        self.colaborators.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.colaborators.setReadOnly(True)
        self.colaborators.setObjectName("colaborators")
        self.gridLayout_3.addWidget(self.colaborators, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.developer = QtWidgets.QLabel(self.widget_2)
        self.developer.setObjectName("developer")
        self.gridLayout_3.addWidget(self.developer, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.widget = QtWidgets.QWidget(self.tab_3)
        self.widget.setObjectName("widget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setOpenExternalLinks(True)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setOpenExternalLinks(True)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 4, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setOpenExternalLinks(True)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 2, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.widget)
        self.label_12.setObjectName("label_12")
        self.gridLayout_5.addWidget(self.label_12, 4, 0, 1, 1)
        self.gridLayout_9.addWidget(self.widget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.about = QtWidgets.QPlainTextEdit(self.tab_2)
        self.about.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.about.setReadOnly(True)
        self.about.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.about.setObjectName("about")
        self.gridLayout_4.addWidget(self.about, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(200, 200))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/images/start.ico"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Acerca de"))
        self.app_name.setText(_translate("Dialog", "APP NAME"))
        self.label_4.setText(_translate("Dialog", "Colaboradores"))
        self.label_3.setText(_translate("Dialog", "Desarrollador"))
        self.developer.setText(_translate("Dialog", "Javier Alejandro González Casellas"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Créditos"))
        self.label_9.setText(_translate("Dialog", "<html><head/><body><p><a href=\"https://facebook.com/javyalejandro99\"><span style=\" text-decoration: underline; color:#0000ff;\">https://facebook.com/javyalejandro99</span></a></p></body></html>"))
        self.label_13.setText(_translate("Dialog", "<html><head/><body><p><a href=\"https://t.me/jalexcode\"><span style=\" text-decoration: underline; color:#0000ff;\">https://t.me/jalexcode</span></a></p></body></html>"))
        self.label_11.setText(_translate("Dialog", "<html><head/><body><p><a href=\"https://twitter.com/javyalejandro99\"><span style=\" text-decoration: underline; color:#0000ff;\">https://twitter.com/javyalejandro99</span></a></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "Proyecto en GitHub:"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p><a href=\"https://github.com/JalexCode/VisualesUCLV-Desktop\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/JalexCode/VisualesUCLV-Desktop</span></a></p></body></html>"))
        self.label_8.setText(_translate("Dialog", "Facebook"))
        self.label_10.setText(_translate("Dialog", "Twitter"))
        self.label_12.setText(_translate("Dialog", "Telegram"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Enlaces"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Acerca de"))
import ui.app_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
