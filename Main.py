'''
Created on Apr 1, 2015

@author: Vince Faller
'''
from PyQt5 import QtGui, QtWidgets ,QtCore
import pdb
import sys
import Logic
import time
import math
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
        self.btn_start.clicked.connect(self.start_brew)
        self.controller = Logic.Controls()
        
    def alarm(self, stage, error_msg):
        alarm = getattr(self, "alarm_"+stage)
        alarm_btn = getattr(self, "alarmbtn_"+stage)
        if alarm_btn.isChecked() == 0:
            alarm.setStyleSheet("background-color: rgb(255, 16, 48);")
            self.textBrowser.append(error_msg)
        
    def alarm_reset(self):
        source = self.sender()
        source.setStyleSheet("background-color: rgb(85, 255, 127);")
    
    def debug(self):
        stuff = eval(self.le_debug.text())
        self.textBrowser.append(str(stuff))
    
    def alarmbtn_toggle(self):
        source = self.sender()
        if source.isChecked()==1:
            source.setText("Alarm OFF")
        else:
            source.setText("Alarm ON")
    
    def run(self):
        self.running = True
        #start the while loop
        while self.running:
            QtWidgets.qApp.processEvents()
            self.update()
            self.controller.update()
            if self.controller.done:
                self.end_brew()
            time.sleep(0.05)
    
    def start_brew(self):
        self.textBrowser.append("Brew Starting")
        self.btn_start.setEnabled(False)
        self.btn_start.setText("Brewing \r\nin Progress")
        self.progressBar.setProperty("value", 0)
        self.sldr_boil_set.setEnabled(False)
        self.sldr_mash_set.setEnabled(False)
        self.sldr_sparge_set.setEnabled(False)
        self.sldr_strike_set.setEnabled(False)
        self.sldr_boil_time.setEnabled(False)
        self.sldr_mash_time.setEnabled(False)
        mash_time = self.lcd_mash_time.intValue()
        boil_time = self.lcd_boil_time.intValue()
        sparge_temp = self.lcd_sparge_set.intValue()
        mash_temp = self.lcd_mash_set.intValue()
        strike_temp = self.lcd_strike_set.intValue()
        boil_temp = self.lcd_boil_set.intValue()
        self.controller.loadrecipe(strike_temp, sparge_temp, mash_temp, mash_time, boil_temp, boil_time)
        self.controller.started = True        
        
    def end_brew(self):
        self.textBrowser.append("Brew Finished")
        self.btn_start.setEnabled(True)
        self.btn_start.setText("START")
        self.sldr_boil_set.setEnabled(True)
        self.sldr_mash_set.setEnabled(True)
        self.sldr_sparge_set.setEnabled(True)
        self.sldr_strike_set.setEnabled(True)
        self.sldr_boil_time.setEnabled(True)
        self.sldr_mash_time.setEnabled(True)
        self.running = False
        self.controller.started = False
        
        
    def update(self):
        controller = self.controller
        self.lcd_boil_meas.setProperty("value", controller.boil.temp)
        self.lcd_hlt_meas.setProperty("value", controller.hlt.temp)
        self.lcd_mash_meas.setProperty("value", controller.mash.temp)
        self.lcd_mash_timeleft.setProperty("intValue", math.floor(controller.mash.time))
        self.lcd_boil_timeleft.setProperty("intValue", math.floor(controller.boil.time))
        #time_left = controller.mash.time + controller.boil.time
        # = (self.controller.recipe.run_time - time_left)/self.controller.recipe.run_time
        #self.progressBar.setProperty("value", percentDone)
        if controller.change:
            self.textBrowser.append("Changing to step "+str(controller.currentStep))


        
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MW()
    form.show()
    form.run()
    app.exec_()