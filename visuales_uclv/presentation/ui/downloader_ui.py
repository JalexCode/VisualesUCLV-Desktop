# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'downloader_ui.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QToolBar, QWidget)
import app_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModal)
        MainWindow.resize(865, 635)
        icon = QIcon()
        icon.addFile(u":/icons/images/download.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.actionIniciar_todas = QAction(MainWindow)
        self.actionIniciar_todas.setObjectName(u"actionIniciar_todas")
        self.actionPausar_todas = QAction(MainWindow)
        self.actionPausar_todas.setObjectName(u"actionPausar_todas")
        self.salir_action = QAction(MainWindow)
        self.salir_action.setObjectName(u"salir_action")
        self.actionAyuda = QAction(MainWindow)
        self.actionAyuda.setObjectName(u"actionAyuda")
        self.actionAcerca_de = QAction(MainWindow)
        self.actionAcerca_de.setObjectName(u"actionAcerca_de")
        icon1 = QIcon()
        icon1.addFile(u"../Documents/Mis Proyectos/FreeS3 Downloader v2/recursos/about.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAcerca_de.setIcon(icon1)
        self.cargar_datos_perfil = QAction(MainWindow)
        self.cargar_datos_perfil.setObjectName(u"cargar_datos_perfil")
        icon2 = QIcon()
        icon2.addFile(u"../Documents/Mis Proyectos/FreeS3 Downloader v2/recursos/default_user.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cargar_datos_perfil.setIcon(icon2)
        self.actionEliminar_links_vencidos = QAction(MainWindow)
        self.actionEliminar_links_vencidos.setObjectName(u"actionEliminar_links_vencidos")
        icon3 = QIcon()
        icon3.addFile(u"../Documents/Mis Proyectos/FreeS3 Downloader v2/recursos/Emoji Symbols-70.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionEliminar_links_vencidos.setIcon(icon3)
        self.actionActivar = QAction(MainWindow)
        self.actionActivar.setObjectName(u"actionActivar")
        self.actionDesactivar = QAction(MainWindow)
        self.actionDesactivar.setObjectName(u"actionDesactivar")
        self.save_list = QAction(MainWindow)
        self.save_list.setObjectName(u"save_list")
        icon4 = QIcon()
        icon4.addFile(u"../Documents/Mis Proyectos/FreeS3 Downloader v2/recursos/Emoji Objects-29.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_list.setIcon(icon4)
        self.load_list = QAction(MainWindow)
        self.load_list.setObjectName(u"load_list")
        icon5 = QIcon()
        icon5.addFile(u"../Documents/Mis Proyectos/FreeS3 Downloader v2/recursos/Emoji Objects-107.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.load_list.setIcon(icon5)
        self.actionBarra_de_t_tulo = QAction(MainWindow)
        self.actionBarra_de_t_tulo.setObjectName(u"actionBarra_de_t_tulo")
        self.actionBarra_de_t_tulo.setCheckable(True)
        self.actionBarra_de_t_tulo.setChecked(True)
        self.actionDatos_del_perfil = QAction(MainWindow)
        self.actionDatos_del_perfil.setObjectName(u"actionDatos_del_perfil")
        self.actionDatos_del_perfil.setCheckable(True)
        self.actionDatos_del_perfil.setChecked(True)
        self.actionModo_Pura_Descarga = QAction(MainWindow)
        self.actionModo_Pura_Descarga.setObjectName(u"actionModo_Pura_Descarga")
        self.actionExportar = QAction(MainWindow)
        self.actionExportar.setObjectName(u"actionExportar")
        icon6 = QIcon()
        icon6.addFile(u"../Documents/Mis Proyectos/FreeS3 Downloader v2/recursos/icon_export_n@2x.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionExportar.setIcon(icon6)
        self.vaciar_informe = QAction(MainWindow)
        self.vaciar_informe.setObjectName(u"vaciar_informe")
        icon7 = QIcon()
        icon7.addFile(u"../Documents/Mis Proyectos/FreeS3 Downloader v2/recursos/Emoji Symbols-134.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.vaciar_informe.setIcon(icon7)
        self.actionPor_nombre = QAction(MainWindow)
        self.actionPor_nombre.setObjectName(u"actionPor_nombre")
        self.ordenar_por_nombre = QAction(MainWindow)
        self.ordenar_por_nombre.setObjectName(u"ordenar_por_nombre")
        icon8 = QIcon()
        icon8.addFile(u"../Documents/Mis Proyectos/FreeS3 Downloader v2/recursos/sort_ascending.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ordenar_por_nombre.setIcon(icon8)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_17 = QGridLayout(self.centralwidget)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_5 = QGridLayout(self.tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.widget_7 = QWidget(self.tab)
        self.widget_7.setObjectName(u"widget_7")
        self.contenedor = QGridLayout(self.widget_7)
        self.contenedor.setObjectName(u"contenedor")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.total_size_queue_label = QLabel(self.widget_7)
        self.total_size_queue_label.setObjectName(u"total_size_queue_label")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.total_size_queue_label.setFont(font1)

        self.gridLayout_4.addWidget(self.total_size_queue_label, 0, 0, 1, 1)

        self.line_6 = QFrame(self.widget_7)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.VLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.line_6, 0, 3, 1, 1)

        self.line_7 = QFrame(self.widget_7)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.VLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.line_7, 0, 1, 1, 1)

        self.download_time_label = QLabel(self.widget_7)
        self.download_time_label.setObjectName(u"download_time_label")
        self.download_time_label.setFont(font1)

        self.gridLayout_4.addWidget(self.download_time_label, 0, 2, 1, 1, Qt.AlignHCenter)

        self.free_space = QLabel(self.widget_7)
        self.free_space.setObjectName(u"free_space")
        self.free_space.setFont(font1)

        self.gridLayout_4.addWidget(self.free_space, 0, 4, 1, 1, Qt.AlignRight)


        self.gridLayout_3.addLayout(self.gridLayout_4, 0, 0, 1, 1)


        self.contenedor.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.tableWidget = QTableWidget(self.widget_7)
        if (self.tableWidget.columnCount() < 8):
            self.tableWidget.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setFrameShape(QFrame.Box)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.contenedor.addWidget(self.tableWidget, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.widget_7, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, icon, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_8 = QGridLayout(self.tab_4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.history_table = QTableWidget(self.tab_4)
        if (self.history_table.columnCount() < 3):
            self.history_table.setColumnCount(3)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(2, __qtablewidgetitem10)
        self.history_table.setObjectName(u"history_table")
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setShowGrid(False)
        self.history_table.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_8.addWidget(self.history_table, 0, 0, 1, 1)

        icon9 = QIcon()
        icon9.addFile(u":/icons/images/history.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabWidget.addTab(self.tab_4, icon9, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_29 = QGridLayout(self.tab_3)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.errors_table = QTableWidget(self.tab_3)
        if (self.errors_table.columnCount() < 3):
            self.errors_table.setColumnCount(3)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.errors_table.setHorizontalHeaderItem(0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.errors_table.setHorizontalHeaderItem(1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.errors_table.setHorizontalHeaderItem(2, __qtablewidgetitem13)
        self.errors_table.setObjectName(u"errors_table")
        self.errors_table.setFrameShape(QFrame.Box)
        self.errors_table.setFrameShadow(QFrame.Sunken)
        self.errors_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.errors_table.setAlternatingRowColors(True)
        self.errors_table.setShowGrid(False)
        self.errors_table.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_29.addWidget(self.errors_table, 0, 0, 1, 1)

        icon10 = QIcon()
        icon10.addFile(u":/icons/images/report.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabWidget.addTab(self.tab_3, icon10, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_2 = QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_7 = QGridLayout(self.groupBox_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.alert_when_finish_checkb = QGroupBox(self.groupBox_2)
        self.alert_when_finish_checkb.setObjectName(u"alert_when_finish_checkb")
        self.alert_when_finish_checkb.setCheckable(True)
        self.gridLayout_6 = QGridLayout(self.alert_when_finish_checkb)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.change_song_button = QPushButton(self.alert_when_finish_checkb)
        self.change_song_button.setObjectName(u"change_song_button")

        self.gridLayout_6.addWidget(self.change_song_button, 0, 1, 1, 1)

        self.sound_path_input = QLineEdit(self.alert_when_finish_checkb)
        self.sound_path_input.setObjectName(u"sound_path_input")
        self.sound_path_input.setReadOnly(True)

        self.gridLayout_6.addWidget(self.sound_path_input, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.alert_when_finish_checkb, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_31 = QGridLayout(self.groupBox_3)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.widget = QWidget(self.groupBox_3)
        self.widget.setObjectName(u"widget")
        self.widget.setEnabled(True)
        self.gridLayout_14 = QGridLayout(self.widget)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_14.addWidget(self.label_3, 0, 0, 1, 1)

        self.max_threads_threads = QSpinBox(self.widget)
        self.max_threads_threads.setObjectName(u"max_threads_threads")
        self.max_threads_threads.setMinimum(1)
        self.max_threads_threads.setMaximum(100)
        self.max_threads_threads.setValue(5)

        self.gridLayout_14.addWidget(self.max_threads_threads, 0, 1, 1, 1)


        self.gridLayout_31.addWidget(self.widget, 1, 0, 1, 1)

        self.widget_2 = QWidget(self.groupBox_3)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_18 = QGridLayout(self.widget_2)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.label_6 = QLabel(self.widget_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_18.addWidget(self.label_6, 0, 0, 1, 1)

        self.if_file_already_exists_combo = QComboBox(self.widget_2)
        self.if_file_already_exists_combo.addItem("")
        self.if_file_already_exists_combo.addItem("")
        self.if_file_already_exists_combo.addItem("")
        self.if_file_already_exists_combo.setObjectName(u"if_file_already_exists_combo")

        self.gridLayout_18.addWidget(self.if_file_already_exists_combo, 0, 1, 1, 1)


        self.gridLayout_31.addWidget(self.widget_2, 2, 0, 1, 1)

        self.widget_3 = QWidget(self.groupBox_3)
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout_22 = QGridLayout(self.widget_3)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.label_8 = QLabel(self.widget_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_22.addWidget(self.label_8, 0, 0, 1, 1)

        self.when_downloads_stops_combo = QComboBox(self.widget_3)
        self.when_downloads_stops_combo.addItem("")
        self.when_downloads_stops_combo.addItem("")
        self.when_downloads_stops_combo.addItem("")
        self.when_downloads_stops_combo.setObjectName(u"when_downloads_stops_combo")

        self.gridLayout_22.addWidget(self.when_downloads_stops_combo, 0, 1, 1, 1)


        self.gridLayout_31.addWidget(self.widget_3, 2, 1, 1, 1)

        self.widget_4 = QWidget(self.groupBox_3)
        self.widget_4.setObjectName(u"widget_4")
        self.gridLayout_15 = QGridLayout(self.widget_4)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.label_5 = QLabel(self.widget_4)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_15.addWidget(self.label_5, 0, 0, 1, 1)

        self.attemps_limit_spin = QSpinBox(self.widget_4)
        self.attemps_limit_spin.setObjectName(u"attemps_limit_spin")
        self.attemps_limit_spin.setMinimum(2)
        self.attemps_limit_spin.setMaximum(100)
        self.attemps_limit_spin.setValue(5)

        self.gridLayout_15.addWidget(self.attemps_limit_spin, 0, 1, 1, 1)


        self.gridLayout_31.addWidget(self.widget_4, 1, 1, 1, 1)

        self.widget_5 = QWidget(self.groupBox_3)
        self.widget_5.setObjectName(u"widget_5")
        self.gridLayout = QGridLayout(self.widget_5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(self.widget_5)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)

        self.change_destiny_button = QPushButton(self.widget_5)
        self.change_destiny_button.setObjectName(u"change_destiny_button")

        self.gridLayout.addWidget(self.change_destiny_button, 0, 3, 1, 1)

        self.destiny_folder_input = QLineEdit(self.widget_5)
        self.destiny_folder_input.setObjectName(u"destiny_folder_input")
        self.destiny_folder_input.setReadOnly(True)

        self.gridLayout.addWidget(self.destiny_folder_input, 0, 2, 1, 1)


        self.gridLayout_31.addWidget(self.widget_5, 0, 0, 1, 2)


        self.gridLayout_2.addWidget(self.groupBox_3, 0, 0, 1, 1)

        icon11 = QIcon()
        icon11.addFile(u":/icons/images/settings.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabWidget.addTab(self.tab_2, icon11, "")

        self.gridLayout_17.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 865, 21))
        self.menuInforme = QMenu(self.menubar)
        self.menuInforme.setObjectName(u"menuInforme")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuInforme.menuAction())
        self.menuInforme.addAction(self.vaciar_informe)
        self.menuInforme.addAction(self.actionExportar)

        self.retranslateUi(MainWindow)
        self.salir_action.triggered.connect(MainWindow.close)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Visuales UCLV Download Manager", None))
        self.actionIniciar_todas.setText(QCoreApplication.translate("MainWindow", u"Iniciar todas", None))
        self.actionPausar_todas.setText(QCoreApplication.translate("MainWindow", u"Pausar todas", None))
        self.salir_action.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.actionAyuda.setText(QCoreApplication.translate("MainWindow", u"Ayuda", None))
        self.actionAcerca_de.setText(QCoreApplication.translate("MainWindow", u"Acerca de", None))
        self.cargar_datos_perfil.setText(QCoreApplication.translate("MainWindow", u"Cargar datos", None))
#if QT_CONFIG(shortcut)
        self.cargar_datos_perfil.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionEliminar_links_vencidos.setText(QCoreApplication.translate("MainWindow", u"Eliminar links vencidos", None))
        self.actionActivar.setText(QCoreApplication.translate("MainWindow", u"Activar", None))
        self.actionDesactivar.setText(QCoreApplication.translate("MainWindow", u"Desactivar", None))
        self.save_list.setText(QCoreApplication.translate("MainWindow", u"Guardar lista de descarga", None))
#if QT_CONFIG(shortcut)
        self.save_list.setShortcut(QCoreApplication.translate("MainWindow", u"F2", None))
#endif // QT_CONFIG(shortcut)
        self.load_list.setText(QCoreApplication.translate("MainWindow", u"Cargar lista de descarga", None))
#if QT_CONFIG(shortcut)
        self.load_list.setShortcut(QCoreApplication.translate("MainWindow", u"F3", None))
#endif // QT_CONFIG(shortcut)
        self.actionBarra_de_t_tulo.setText(QCoreApplication.translate("MainWindow", u"Barra de t\u00edtulo", None))
        self.actionDatos_del_perfil.setText(QCoreApplication.translate("MainWindow", u"Datos del perfil", None))
        self.actionModo_Pura_Descarga.setText(QCoreApplication.translate("MainWindow", u"Modo Pura Descarga", None))
        self.actionExportar.setText(QCoreApplication.translate("MainWindow", u"Exportar", None))
        self.vaciar_informe.setText(QCoreApplication.translate("MainWindow", u"Vaciar la Lista", None))
        self.actionPor_nombre.setText(QCoreApplication.translate("MainWindow", u"Por nombre", None))
        self.ordenar_por_nombre.setText(QCoreApplication.translate("MainWindow", u"Ordenar elementos por nombre", None))
#if QT_CONFIG(tooltip)
        self.total_size_queue_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Tama\u00f1o total de la descarga</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.total_size_queue_label.setText(QCoreApplication.translate("MainWindow", u"Tama\u00f1o total: 0.0 Mb", None))
#if QT_CONFIG(tooltip)
        self.download_time_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Tiempo transcurrido de descarga</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.download_time_label.setText(QCoreApplication.translate("MainWindow", u"Tiempo transcurrido: -", None))
#if QT_CONFIG(tooltip)
        self.free_space.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Espacio disponible en el disco donde se encuentra la carpeta de las Descargas</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.free_space.setText(QCoreApplication.translate("MainWindow", u"Espacio disponible: -", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Estado", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Progreso", None))
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Velocidad", None))
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Tama\u00f1o", None))
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Tiempo restante", None))
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Agregada", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Descargas", None))
        ___qtablewidgetitem7 = self.history_table.horizontalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        ___qtablewidgetitem8 = self.history_table.horizontalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Tiempo de descarga", None))
        ___qtablewidgetitem9 = self.history_table.horizontalHeaderItem(2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Destino", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Historial", None))
        ___qtablewidgetitem10 = self.errors_table.horizontalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Fecha-Hora", None))
        ___qtablewidgetitem11 = self.errors_table.horizontalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Archivo", None))
        ___qtablewidgetitem12 = self.errors_table.horizontalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Descripci\u00f3n", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Informe de errores", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Tras descargar", None))
        self.alert_when_finish_checkb.setTitle(QCoreApplication.translate("MainWindow", u"Alertar que finaliz\u00f3 la descarga con un sonido", None))
        self.change_song_button.setText(QCoreApplication.translate("MainWindow", u"Cambiar", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Descargas", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Cantidad de hilos:", None))
#if QT_CONFIG(tooltip)
        self.max_threads_threads.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Cantidad de descargas que se realizar\u00e1n a la vez</p><p>Por defecto: 10</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Si el archivo existe:", None))
        self.if_file_already_exists_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"Sobreescribir", None))
        self.if_file_already_exists_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"Omitir", None))
        self.if_file_already_exists_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"Renombrar", None))

#if QT_CONFIG(tooltip)
        self.if_file_already_exists_combo.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Acci\u00f3n a llevar a cabo si el archivo a descargar ya existe en el directorio especificado</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Al detener las descargas:", None))
        self.when_downloads_stops_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"Preguntar qu\u00e9 hacer", None))
        self.when_downloads_stops_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"Eliminar los archivos incompletos", None))
        self.when_downloads_stops_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"No hacer nada", None))

#if QT_CONFIG(tooltip)
        self.when_downloads_stops_combo.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Acci\u00f3n a llevar a cabo con los archivos descargados a medias al detener las descargas</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Cantidad de intentos:", None))
#if QT_CONFIG(tooltip)
        self.attemps_limit_spin.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Cantidad de intentos para lograr un descarga exitosa</p><p>Por defecto: 10</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Carpeta de descargas:", None))
        self.change_destiny_button.setText(QCoreApplication.translate("MainWindow", u"Cambiar", None))
#if QT_CONFIG(tooltip)
        self.destiny_folder_input.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Directorio en el que se guardar\u00e1 el contenido descargado</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.destiny_folder_input.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Opciones", None))
        self.menuInforme.setTitle(QCoreApplication.translate("MainWindow", u"Informe", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi
