# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDockWidget, QFrame,
    QGridLayout, QHeaderView, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTableWidget,
    QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QWidget)
import app_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(755, 590)
        icon = QIcon()
        icon.addFile(u":/icons/images/start.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.load_data_action = QAction(MainWindow)
        self.load_data_action.setObjectName(u"load_data_action")
        self.quit_action = QAction(MainWindow)
        self.quit_action.setObjectName(u"quit_action")
        self.download_remote_repo_action = QAction(MainWindow)
        self.download_remote_repo_action.setObjectName(u"download_remote_repo_action")
        self.about_action = QAction(MainWindow)
        self.about_action.setObjectName(u"about_action")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/success.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.about_action.setIcon(icon1)
        self.export_local_repo_as_txt_action = QAction(MainWindow)
        self.export_local_repo_as_txt_action.setObjectName(u"export_local_repo_as_txt_action")
        self.show_download_manager_action = QAction(MainWindow)
        self.show_download_manager_action.setObjectName(u"show_download_manager_action")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/download.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.show_download_manager_action.setIcon(icon2)
        self.actionArchivos_del_directorio = QAction(MainWindow)
        self.actionArchivos_del_directorio.setObjectName(u"actionArchivos_del_directorio")
        self.actionArchivos_del_directorio_2 = QAction(MainWindow)
        self.actionArchivos_del_directorio_2.setObjectName(u"actionArchivos_del_directorio_2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 755, 21))
        self.menuOpciones = QMenu(self.menubar)
        self.menuOpciones.setObjectName(u"menuOpciones")
        self.menuExportar_repositorio_local = QMenu(self.menuOpciones)
        self.menuExportar_repositorio_local.setObjectName(u"menuExportar_repositorio_local")
        self.menuRepositorio = QMenu(self.menuExportar_repositorio_local)
        self.menuRepositorio.setObjectName(u"menuRepositorio")
        self.menuEnlaces_2 = QMenu(self.menuExportar_repositorio_local)
        self.menuEnlaces_2.setObjectName(u"menuEnlaces_2")
        self.menuInfo = QMenu(self.menubar)
        self.menuInfo.setObjectName(u"menuInfo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidget.setFeatures(QDockWidget.DockWidgetClosable)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.gridLayout_2 = QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.treeWidget = QTreeWidget(self.dockWidgetContents)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1")
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setFrameShape(QFrame.NoFrame)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setHeaderHidden(True)

        self.gridLayout_2.addWidget(self.treeWidget, 0, 0, 1, 1)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidget)

        self.menubar.addAction(self.menuOpciones.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())
        self.menuOpciones.addAction(self.show_download_manager_action)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.menuExportar_repositorio_local.menuAction())
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.quit_action)
        self.menuExportar_repositorio_local.addAction(self.menuRepositorio.menuAction())
        self.menuExportar_repositorio_local.addAction(self.menuEnlaces_2.menuAction())
        self.menuRepositorio.addAction(self.export_local_repo_as_txt_action)
        self.menuEnlaces_2.addAction(self.actionArchivos_del_directorio_2)
        self.menuInfo.addAction(self.about_action)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Visuales UCLV Explorer", None))
        self.load_data_action.setText(QCoreApplication.translate("MainWindow", u"Cargar repositorio local", None))
        self.quit_action.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.download_remote_repo_action.setText(QCoreApplication.translate("MainWindow", u"Descargar repositorio remoto", None))
        self.about_action.setText(QCoreApplication.translate("MainWindow", u"Acerca de", None))
        self.export_local_repo_as_txt_action.setText(QCoreApplication.translate("MainWindow", u"TXT", None))
        self.show_download_manager_action.setText(QCoreApplication.translate("MainWindow", u"Gestionador de descargas", None))
        self.actionArchivos_del_directorio.setText(QCoreApplication.translate("MainWindow", u"Archivos del directorio", None))
        self.actionArchivos_del_directorio_2.setText(QCoreApplication.translate("MainWindow", u"Archivos del directorio", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Tama\u00f1o", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Fecha de modificaci\u00f3n", None))
        self.menuOpciones.setTitle(QCoreApplication.translate("MainWindow", u"Aplicaci\u00f3n", None))
        self.menuExportar_repositorio_local.setTitle(QCoreApplication.translate("MainWindow", u"Exportar", None))
        self.menuRepositorio.setTitle(QCoreApplication.translate("MainWindow", u"Repositorio", None))
        self.menuEnlaces_2.setTitle(QCoreApplication.translate("MainWindow", u"Enlaces", None))
        self.menuInfo.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
        self.dockWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Directorios", None))
    # retranslateUi
