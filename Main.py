'''
Created on Apr 1, 2015

@author: Vince Faller
'''
from PyQt5 import QtGui, QtWidgets ,QtCore
import pdb
import sys
from UI import MainWindow

class MW(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    """The Main Window where everything happens"""
    def __init__(self, parent=None):
        """Initializes shit (Don't use partial as most of the variables
        aren't created yet)"""
        super(MW, self).__init__(parent)
        self.setupUi(self)
        self.le_debug.returnPressed.connect(self.debug)
        self.alarm_hlt.clicked.connect(self.alarm_reset)
        self.alarm_mash.clicked.connect(self.alarm_reset)
        self.alarm_boil.clicked.connect(self.alarm_reset)
        self.alarmbtn_hlt.toggled.connect(self.alarmbtn_toggle)
        self.alarmbtn_mash.toggled.connect(self.alarmbtn_toggle)
        self.alarmbtn_boil.toggled.connect(self.alarmbtn_toggle)
        
    def alarm(self, btn):
        btn.setStyleSheet("background-color: rgb(255, 16, 48);")
        
    def alarm_reset(self):
        source = self.sender()
        source.setStyleSheet("background-color: rgb(85, 255, 127);")
    
    def debug(self):
        eval(self.le_debug.text())
    
    def alarmbtn_toggle(self):
        source = self.sender()
        if source.isChecked()==1:
            source.setText("Alarm OFF")
        else:
            source.setText("Alarm ON")
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MW()
    form.show()
    app.exec_()