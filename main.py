# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 18:05:19 2020

@author: DZLR3
"""

from PyQt5 import QtWidgets
from Primary_GUI import Primary_GUI

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    wizard = Primary_GUI()
    wizard.setWindowTitle('Ellsberg, Pullman and Colman Test')
    wizard.show()
    app.exec_()
