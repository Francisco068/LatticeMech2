# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LatticeMech3D.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class SimpleViewer(QtWidgets.QOpenGLWidget):
    mouse_press_cb = QtCore.pyqtSignal(QtGui.QMouseEvent)

    def __init__(self,parent=None):
        self.parent = parent
        QtWidgets.QOpenGLWidget.__init__(self, parent)
        self.setMouseTracking(True)

    def mousePressEvent( self, evt ):
        self.mouse_press_cb.emit( evt )

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1139, 833)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.horizontalLayout.addWidget(self.treeWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.openGLWidget = SimpleViewer(self.centralwidget) 
        # QtWidgets.QOpenGLWidget(self.centralwidget)
        self.openGLWidget.setMinimumSize(QtCore.QSize(0, 600))
        self.openGLWidget.setObjectName("openGLWidget")
        self.verticalLayout.addWidget(self.openGLWidget)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 60))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 150))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1139, 21))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuCalculate = QtWidgets.QMenu(self.menubar)
        self.menuCalculate.setObjectName("menuCalculate")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionsave = QtWidgets.QAction(MainWindow)
        self.actionsave.setObjectName("actionsave")
        self.actionsave_picture = QtWidgets.QAction(MainWindow)
        self.actionsave_picture.setObjectName("actionsave_picture")
        self.actionsave_txt = QtWidgets.QAction(MainWindow)
        self.actionsave_txt.setObjectName("actionsave_txt")
        self.actionsave_json = QtWidgets.QAction(MainWindow)
        self.actionsave_json.setObjectName("actionsave_json")
        self.actionexit = QtWidgets.QAction(MainWindow)
        self.actionexit.setObjectName("actionexit")
        self.actionadd_node = QtWidgets.QAction(MainWindow)
        self.actionadd_node.setObjectName("actionadd_node")
        self.actionadd_beam = QtWidgets.QAction(MainWindow)
        self.actionadd_beam.setObjectName("actionadd_beam")
        self.actionremove_element = QtWidgets.QAction(MainWindow)
        self.actionremove_element.setObjectName("actionremove_element")
        self.menufile.addAction(self.actionOpen)
        self.menufile.addAction(self.actionsave)
        self.menufile.addAction(self.actionsave_picture)
        self.menufile.addAction(self.actionsave_txt)
        self.menufile.addAction(self.actionsave_json)
        self.menufile.addAction(self.actionexit)
        self.menuEdit.addAction(self.actionadd_node)
        self.menuEdit.addAction(self.actionadd_beam)
        self.menuEdit.addAction(self.actionremove_element)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuCalculate.menuAction())

        self.retranslateUi(MainWindow)
        self.tableWidget.cellChanged['int','int'].connect(self.cellChangedAction)
        self.treeWidget.itemClicked['QTreeWidgetItem*','int'].connect(self.itemCliquedAction)
        self.openGLWidget.mouse_press_cb.connect(self.mouse_press)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def cellChangedAction(self,signal1, signal2):
        self.textBrowser.append("essai %i, %i " % (signal1, signal2))

    def itemCliquedAction(self,Item):
        self.textBrowser.append("item %s" % (Item.data(0,0)))

    def mouse_press(self, evt ):
        self.textBrowser.append('Mouse press {}: [{},{}]'.format(evt.button(),evt.x(),evt.y()) )
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Lattice"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Material"))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "Aluminum:7000,0.3"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "Nodes"))
        self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "N1:0.0,0.5"))
        self.treeWidget.topLevelItem(2).setText(0, _translate("MainWindow", "Beams"))
        self.treeWidget.topLevelItem(2).child(0).setText(0, _translate("MainWindow", "B1:1,1,0,1,0.5"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "N1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "X"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Y"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuCalculate.setTitle(_translate("MainWindow", "Calculate"))
        self.actionOpen.setText(_translate("MainWindow", "Open xml"))
        self.actionsave.setText(_translate("MainWindow", "save xml"))
        self.actionsave_picture.setText(_translate("MainWindow", "save picture"))
        self.actionsave_txt.setText(_translate("MainWindow", "save txt"))
        self.actionsave_json.setText(_translate("MainWindow", "save json"))
        self.actionexit.setText(_translate("MainWindow", "exit"))
        self.actionadd_node.setText(_translate("MainWindow", "add node"))
        self.actionadd_beam.setText(_translate("MainWindow", "add beam"))
        self.actionremove_element.setText(_translate("MainWindow", "remove element"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

