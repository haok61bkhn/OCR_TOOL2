import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QFileDialog,QInputDialog , QShortcut
from PyQt5.QtGui import QIcon, QPixmap ,QKeySequence
import glob
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("tool.ui", self)
        self.next.setShortcut("D")
        self.prev.setShortcut("A")
        # self.ok.setShortcut("Space")
        self.open.setShortcut("Ctrl+O")
        shortcut = QShortcut(QKeySequence("W"), self.id_2)
        shortcut.activated.connect(self.slot)
        shortcut = QShortcut(QKeySequence("Ctrl+S"), self.id_2)
        shortcut.activated.connect(self.disslot)
        # shortcut = QShortcut(QKeySequence("Del"))
        # shortcut.activated.connect(self.disslot)
        self.open.triggered.connect(self.showdialog)
        self.next.clicked.connect(self.event_next)
        self.prev.clicked.connect(self.event_prev)
        self.ok.clicked.connect(self.event_ok)


        self.list_img=[]
        self.id=0
        self.check=False
        # QtCore.QMetaObject.connectSlotsByName()
    def show_image(self,path):
        try:
            label = open(path.split(".")[0]+".txt").read().split("\n")
        except:
            label =""
        self.id_2.setText(label[0])
        self.name_2.setText(label[1])
        self.date_2.setText(label[2])
        self.ad1_2.setText(label[3])
        self.ad2_2.setText(label[4])
        self.path.setText(path.split("/")[-1])
        pixmap = QPixmap(path)
        self.img.setPixmap(pixmap)
        self.img.setScaledContents(True)

        self.check=True
    def slot(self):
        self.label.setFocus()
    def disslot(self):
        self.label.clearFocus()
        self.event_ok()

    def showdialog(self):
        self.check=False
        folderPath = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select folder')
        self.list_img=glob.glob(folderPath+"/*.jpg")+glob.glob(folderPath+"/*.png")+glob.glob(folderPath+"/*.jpeg")
        self.id=0
        if(len(self.list_img)>0):
            self.show_image(self.list_img[0])
        
    def event_ok(self):
        if(self.check):
            lb=self.id_2.toPlainText()+"\n"+self.name_2.toPlainText()+"\n"+self.date_2.toPlainText()+"\n"+self.ad1_2.toPlainText()+"\n"+self.ad2_2.toPlainText()
            path=self.list_img[self.id]
            label = open(path.split(".")[0]+".txt","w+")
            label.write(lb)
            label.close()

    def event_next(self):
        if(self.id <len(self.list_img)-1):
            self.id +=1
            self.show_image(self.list_img[self.id])
    def event_prev(self):
        if(self.id>0):
            self.id -=1
            self.show_image(self.list_img[self.id])

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()

window.show()
app.exec_()
