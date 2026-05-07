# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QPlainTextEdit, QSizePolicy, QTabWidget,
    QWidget)
import app_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(623, 231)
        Dialog.setModal(True)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.app_name = QLabel(self.tab)
        self.app_name.setObjectName(u"app_name")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.app_name.setFont(font)

        self.gridLayout_2.addWidget(self.app_name, 0, 0, 1, 1)

        self.widget_2 = QWidget(self.tab)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.colaborators = QPlainTextEdit(self.widget_2)
        self.colaborators.setObjectName(u"colaborators")
        self.colaborators.setFrameShape(QFrame.NoFrame)
        self.colaborators.setReadOnly(True)

        self.gridLayout_3.addWidget(self.colaborators, 4, 0, 1, 1)

        self.label_4 = QLabel(self.widget_2)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setBold(True)
        self.label_4.setFont(font1)

        self.gridLayout_3.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.developer = QLabel(self.widget_2)
        self.developer.setObjectName(u"developer")

        self.gridLayout_3.addWidget(self.developer, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_9 = QGridLayout(self.tab_3)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.widget = QWidget(self.tab_3)
        self.widget.setObjectName(u"widget")
        self.gridLayout_5 = QGridLayout(self.widget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setOpenExternalLinks(True)

        self.gridLayout_5.addWidget(self.label_9, 1, 1, 1, 1)

        self.label_13 = QLabel(self.widget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setOpenExternalLinks(True)

        self.gridLayout_5.addWidget(self.label_13, 4, 1, 1, 1)

        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setOpenExternalLinks(True)

        self.gridLayout_5.addWidget(self.label_11, 2, 1, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setOpenExternalLinks(True)

        self.gridLayout_5.addWidget(self.label_5, 0, 1, 1, 1)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_5.addWidget(self.label_8, 1, 0, 1, 1)

        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_5.addWidget(self.label_10, 2, 0, 1, 1)

        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_5.addWidget(self.label_12, 4, 0, 1, 1)


        self.gridLayout_9.addWidget(self.widget, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_4 = QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.about = QPlainTextEdit(self.tab_2)
        self.about.setObjectName(u"about")
        self.about.setFrameShape(QFrame.NoFrame)
        self.about.setReadOnly(True)
        self.about.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout_4.addWidget(self.about, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(200, 200))
        self.label.setPixmap(QPixmap(u":/icons/images/start.ico"))
        self.label.setScaledContents(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Acerca de", None))
        self.app_name.setText(QCoreApplication.translate("Dialog", u"APP NAME", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Colaboradores", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Desarrollador", None))
        self.developer.setText(QCoreApplication.translate("Dialog", u"Javier Alejandro Gonz\u00e1lez Casellas", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Cr\u00e9ditos", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><a href=\"https://facebook.com/javyalejandro99\"><span style=\" text-decoration: underline; color:#0000ff;\">https://facebook.com/javyalejandro99</span></a></p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><a href=\"https://t.me/jalexcode\"><span style=\" text-decoration: underline; color:#0000ff;\">https://t.me/jalexcode</span></a></p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><a href=\"https://twitter.com/javyalejandro99\"><span style=\" text-decoration: underline; color:#0000ff;\">https://twitter.com/javyalejandro99</span></a></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Proyecto en GitHub:", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><a href=\"https://github.com/JalexCode/VisualesUCLV-Desktop\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/JalexCode/VisualesUCLV-Desktop</span></a></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Facebook", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Twitter", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Telegram", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"Enlaces", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Acerca de", None))
        self.label.setText("")
    # retranslateUi
