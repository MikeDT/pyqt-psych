# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:23:25 2019

@author: miketaylor
"""

from PyQt5 import QtWidgets, QtCore, uic
import sys

class MyWizard(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Ellsberg, Pullman and Colman Test')
        self.window = uic.loadUi('Screen.ui', self)
        # Import all the text from external sources (simplifies future changes)
        self.disclaimer_text = open('text\\' + 'Disclaimer.txt', 'r').read()
        self.intro_text = open('text\\' + 'Introduction.txt', 'r').read()
        self.instruction_text = open('text\\' + 'Instructions.txt', 'r').read()

        # The possible screens
        self.screens = ['Intro', 'Consent', 'Demographic',
                        'Instruction', 'Test', 'Debrief']

        self.csv_db = open('database\\csv_db.csv', 'a')
        self.window.back_btn.clicked.connect(self.back_button_clicked)
        self.window.next_btn.clicked.connect(self.next_button_clicked)
        self.window.save_btn.clicked.connect(self.save_button_clicked)
        self.window.tabs.currentChanged.connect(self.refresh_nav_buttons)

        self.window.gender_combobox.addItem("Female")
        self.window.gender_combobox.addItem("Male")
        self.window.gender_combobox.addItem("Other")
        self.window.gender_combobox.addItem("Prefer Not To Say")
        self.window.edu_combobox.addItem("High School")
        self.window.edu_combobox.addItem("Associate's")
        self.window.edu_combobox.addItem("Bachelor's")
        self.window.edu_combobox.addItem("Master's")
        self.window.edu_combobox.addItem("PhD")
        self.window.edu_combobox.addItem("Other")
        self.window.edu_combobox.addItem("Prefer Not To Say")
        self.window.intro_textbox.setText(self.intro_text)
        self.window.intro_textbox.setReadOnly(True)
        self.window.disclaimer_textbox.setText(self.disclaimer_text)
        self.window.disclaimer_textbox.setReadOnly(True)
        self.window.instr_textbox.setText(self.instruction_text)
        self.window.instr_textbox.setReadOnly(True)
        self.window.back_btn.hide()
        self.window.save_btn.hide()
        self.window.show()

    def back_button_clicked(self):
        """
        Dictates the actions for clicking the back button on a given screen
        using the screen_fxn_dict dictionary that houses the screen dispay
        functions, selected by the screen + button tuple that interacts with
        the screen_nav_graph dictionary.
        """
        self.window.tabs.setCurrentIndex(self.window.tabs.currentIndex() - 1)
        self.window.next_btn.show()
        self.window.back_btn.show()
        self.window.save_btn.hide()
        if self.window.tabs.currentIndex() == 0:
            self.window.back_btn.hide()

    def is_task_complete(self):
        """
        Checks all activities, demographics etc have been submitted prior to
        allowing the participant to save and exit
        """
        pass
        #  return error for what is not yet submitted

    def get_details(self):
        """
        Get the all the details from the experiment (incl. demographics and
        consent), and cast them into a csv ready string
        """
        username = str(self.window.username_textbox.text())
        consent = str(self.window.consent_checkbox.isChecked())
        age = str(self.window.age_spinbox.value())
        education = str(self.window.edu_combobox.currentText())
        gender = str(self.window.gender_combobox.currentText())
        urn1_result = str(self.window.urn1_radiobutton.isChecked())
        urn2_result = str(self.window.urn2_radiobutton.isChecked()) #not strictly necessary, but belt and braces
        urn_condition = str(None)
        return (username + ', ' + consent + ', ' + age + ', ' +
                education + ', ' + gender + ', ' + urn1_result + ', ' +
                urn2_result + ', ' + urn_condition)

    def show_save_check(self):
        """
        Check whether the save button should be shown, based upon the
        completion of all the relevant criteria (consent, demographics, test)
        """
        if self.window.consent_checkbox.isChecked():
            self.window.save_btn.show()
        else:
            self.window.save_btn.hide()

    def next_button_clicked(self):
        """
        Dictates the actions for clicking the next button on a given screen
        using the screen_fxn_dict dictionary that houses the screen dispay
        functions, selected by the screen + button tuple that interacts with
        the screen_nav_graph dictionary.
        """
        self.window.tabs.setCurrentIndex(self.window.tabs.currentIndex() + 1)
        self.window.next_btn.show()
        self.window.back_btn.show()
        if self.window.tabs.currentIndex() == 5:
            self.window.next_btn.hide()
            self.show_save_check()

    def save_button_clicked(self):
        """
        Saves the demographics to csv, closes the csv and exits the application
        """
        self.csv_db.write((self.get_details()))
        self.csv_db.write('\n')
        self.csv_db.close()
        sys.exit(app.exec_())

    def refresh_nav_buttons(self):
        """
        Refreshs the navigation buttons upon tab clicks to ensure only the
        relevant buttons are shown
        """
        if self.window.tabs.currentIndex() == 0:
            self.window.save_btn.hide()
            self.window.back_btn.hide()
        elif self.window.tabs.currentIndex() == 5:
            self.show_save_check()
            self.window.next_btn.hide()
            self.window.back_btn.show()
        else:
            self.window.next_btn.show()
            self.window.back_btn.show()


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
wizard.show()
app.exec_()

# To Do
# Shift forward/back buttons to bottom
# move disclaimer to text
# move intructions to text
# create the random images and the buttons
# create a logger
