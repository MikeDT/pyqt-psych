# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:23:25 2019

@author: miketaylor
"""

from PyQt5 import QtWidgets, QtCore

class MyWizard(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # vertical layout, wraps content layout and buttons layout
        # could be almost any layout actually
        self.disclaimer_text = open("Disclaimer.txt",'r').read()
        self.create_buttons()
        self.display_intro_screen()
        self.setWindowTitle('Ellsberg, Pullman and Colman Test')


    def screen_clear(self):
        # remove old content
        self.content_layout.removeWidget(self.content)
        self.content.deleteLater()
        
    def create_buttons(self):
        # back, forward buttons wrapped in horizontal layout
#        self.vertical_layout = QtWidgets.QVBoxLayout()
#        self.setLayout(self.vertical_layout)
#        self.content_layout = QtWidgets.QVBoxLayout()
#        self.button_layout = QtWidgets.QHBoxLayout()
        self.vertical_layout = QtWidgets.QVBoxLayout()
        #self.setLayout(self.vertical_layout)
        self.content_layout = QtWidgets.QVBoxLayout()
        self.demo_button_layout = QtWidgets.QVBoxLayout()
        self.nav_button_layout = QtWidgets.QHBoxLayout()
        self.nav_button_layout.setAlignment(QtCore.Qt.AlignBottom)
        
        self.nav_button_layout.addStretch()
        self.consent_check_box = QtWidgets.QCheckBox("I give consent")
        self.nav_button_layout.addWidget(self.consent_check_box)
        self.back_button = QtWidgets.QPushButton('Back')
        self.back_button.clicked.connect(self.back_button_clicked)
        self.nav_button_layout.addWidget(self.back_button)
        self.forward_button = QtWidgets.QPushButton('Next')
        self.forward_button.clicked.connect(self.forward_button_clicked)
        self.nav_button_layout.addWidget(self.forward_button)
        self.age_spinbox = QtWidgets.QSpinBox()
        self.demo_button_layout.addWidget(self.age_spinbox)
        self.gender_combobox = QtWidgets.QComboBox()
        self.gender_combobox.addItem("Female")
        self.gender_combobox.addItem("Male")
        self.gender_combobox.addItem("Other")
        self.gender_combobox.addItem("Prefer Not To Say")
        self.demo_button_layout.addWidget(self.gender_combobox)
        self.edu_combobox = QtWidgets.QComboBox()
        self.edu_combobox.addItem("High School")
        self.edu_combobox.addItem("Associate's")
        self.edu_combobox.addItem("Bachelor's")
        self.edu_combobox.addItem("Master's")
        self.edu_combobox.addItem("PhD")
        self.edu_combobox.addItem("Other")
        self.edu_combobox.addItem("Prefer Not To Say")
        self.demo_button_layout.addWidget(self.edu_combobox)
        self.vertical_layout.addLayout(self.demo_button_layout)
        self.vertical_layout.addLayout(self.nav_button_layout)
        self.consent_check_box.hide()
        
    def hide_buttons(self):
        """
        The back button is clicked.
        """
        self.consent_check_box.hide()
        self.gender_combobox.hide()
        self.age_spinbox.hide()
        self.edu_combobox.hide()
        
        
    def display_intro_screen(self):
        """
        The back button is clicked.
        """
        # content widget and layout
        self.content = QtWidgets.QTextEdit('Here are some introductory statements')
        self.content.setReadOnly(True) # customize with your content
        self.content_layout.addWidget(self.content)
        self.vertical_layout.addLayout(self.content_layout)
        self.back_button.hide()
        self.hide_buttons()
        self.current_screen = 'intro'

    def display_consent_screen(self):
        """
        The back button is clicked.
        """
        # content widget and layout
        self.content = QtWidgets.QTextEdit(self.disclaimer_text)
        self.content.setReadOnly(True) # customize with your content
        self.content_layout.addWidget(self.content)
        self.vertical_layout.addLayout(self.content_layout)
        self.back_button.show()
        self.consent_check_box.show()
        self.current_screen = 'consent'
        
    def display_demographic_screen(self):
        """
        The back button is clicked.
        """
        # content widget and layout
        self.content = QtWidgets.QLabel('Demographic Screen') # customize with your content        
        self.gender_combobox.show()
        self.age_spinbox.show()
        self.edu_combobox.show()
        self.content_layout.addWidget(self.content)
        self.vertical_layout.addLayout(self.content_layout)
        self.current_screen = 'demographic'

    def display_instructions_screen(self):
        """
        The back button is clicked.
        """
        # content widget and layout
        self.content = QtWidgets.QTextEdit('Here are some instructions')
        self.content.setReadOnly(True) # customize with your content
        self.content_layout.addWidget(self.content)
        self.vertical_layout.addLayout(self.content_layout)
        self.current_screen = 'instructions'

    def display_test_screen(self):
        """
        The back button is clicked.
        """
        # content widget and layout
        self.content = QtWidgets.QLabel('Test Screen') # customize with your content
        self.content_layout.addWidget(self.content)
        self.vertical_layout.addLayout(self.content_layout)
        self.current_screen = 'test'

    def back_button_clicked(self):
        """
        The back button is clicked.
        """
        self.screen_clear()
        self.hide_buttons()
        if self.current_screen == 'consent':
            self.display_intro_screen()    
        elif self.current_screen == 'demographic':
            self.display_consent_screen()
        elif self.current_screen == 'instructions':
            self.display_demographic_screen()
        elif self.current_screen == 'test':
            self.display_instructions_screen()
            
    def forward_button_clicked(self):
        """
        The forward button is clicked.
        """
        self.screen_clear()
        self.hide_buttons()
        if self.current_screen == 'intro':
            self.display_consent_screen()
        elif self.current_screen == 'consent':
            if self.consent_check_box.isChecked():
                self.display_demographic_screen()
            else:
                self.display_consent_screen()
        elif self.current_screen == 'demographic':
            self.display_instructions_screen()
        elif self.current_screen == 'instructions':
            self.display_test_screen()
        elif self.current_screen == 'test':
            self.display_test_screen()
            
            
# loads to info page
# then consent
        # then demographics
        # then task itself (prob needs a submit/reset button)
        # then debrief
        # will need a logger
        # create a history file to support pseudo random blah
        # qtab widget
        

app = QtWidgets.QApplication([])

wizard = MyWizard()
wizard.setWindowTitle('MyWizard Example')
wizard.setFixedSize(600, 800)
wizard.show()

app.exec_()


# To Do
# Shift forward/back buttons to bottom
# move disclaimer to text
# move intructions to text
# create the random images and the buttons
# create a logger

# 
