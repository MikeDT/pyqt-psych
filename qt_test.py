# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 12:49:47 2019

@author: miketaylor
"""

from PyQt5 import uic 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication([]) 

window = uic.loadUi("demographics.ui")
 
#Your code here!

window.show() 

app.exec_()
