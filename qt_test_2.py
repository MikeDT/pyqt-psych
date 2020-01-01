# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:23:25 2019

@author: miketaylor
"""

from PyQt5 import QtWidgets, QtCore, uic
import random
import sys

class MyWizard(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Import the designer UI and name the window
        self.window = uic.loadUi('Screen.ui', self)
        self.setWindowTitle('Ellsberg, Pullman and Colman Test')

        # Open the 'database' tables
        self.csv_results_db = open('database\\csv_results_db.csv', 'a')

        # Import all the text from external sources (simplifies future changes)
        # and set the fill the text boxes (read only to prevent user edits)
        self.intro_text = open('text\\' + 'Introduction.txt', 'r').read()
        self.window.intro_textbox.setText(self.intro_text)
        self.window.intro_textbox.setReadOnly(True)
        self.disclaimer_text = open('text\\' + 'Disclaimer.txt', 'r').read()
        self.window.disclaimer_textbox.setText(self.disclaimer_text)
        self.window.disclaimer_textbox.setReadOnly(True)
        self.instruction_text = open('text\\' + 'Instructions.txt', 'r').read()
        self.window.instr_textbox.setText(self.instruction_text)
        self.window.instr_textbox.setReadOnly(True)

        # Adjust the combobox content to support the valid values
        gender_list = ['', 'Prefer Not To Say', 'Female', 'Male', 'Other']
        for gender in gender_list:
            self.window.gender_combobox.addItem(gender)
        education_list = ['', 'High School', 'Bachelors', 'Masters', 'PhD',
                          'Other']
        for education in education_list:
            self.window.edu_combobox.addItem(education)

        # Set random urn condition (i.e. marble count), distribution
        # and position
        self.urn_condition = random.choice([2, 10, 100])
        if self.urn_condition == 2:
            dist = ['Blue', 'Blue']
            random.shuffle(dist)
        elif self.urn_condition == 10:
            dist = ['Blue'] * 2 + ['Red'] * 8
            random.shuffle(dist)
        else:
            dist = ['Blue'] * 53 + ['Red'] * 47
            random.shuffle(dist)
        self.urn_distribution = dist
        self.random_urn_position = random.choice([0, 1])  # 1 right, 0 left

        # Connect the buttons and tabs to the relevant functions
        self.window.back_btn.clicked.connect(self.back_button_clicked)
        self.window.next_btn.clicked.connect(self.next_button_clicked)
        self.window.save_btn.clicked.connect(self.save_button_clicked)
        self.window.tabs.currentChanged.connect(self.refresh_nav_buttons)

        # Set the default conditions for the nav buttons and show the screen
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

    def is_task_complete(self,results):
        """
        Checks all activities, demographics etc have been submitted prior to
        allowing the participant to save and exit
        """
        return True
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
        urn_condition = str(self.urn_condition)
        urn_position = str(self.random_urn_position)  # 0 random urn on the right, 1 on the left
        urn_selected = str(0)  # 0 random urn, 1 50/50 urn ############################  think radio button XOR gate
        marble_received = str('Red')
        return (username + ', ' + consent + ', ' + age + ', ' +
                education + ', ' + gender + ', ' +
                urn_condition + ', ' + urn_position + ', ' +
                urn_selected + ', ' + marble_received)

    def show_save_check(self):
        """
        Check whether the save button should be shown, based upon the
        completion of all the relevant criteria (consent, demographics, test)
        """
        if self.window.consent_checkbox.isChecked():
            self.window.save_btn.show()
        else:
            self.window.save_btn.hide()

    def save_button_clicked(self):
        """
        Saves the demographics to csv, closes the csv and exits the application
        """
        results = self.get_details()
        if self.is_task_complete(results):
            self.csv_results_db.write(results)
            self.csv_results_db.write('\n')
            self.csv_results_db.close()
            sys.exit(app.exec_())

app = QtWidgets.QApplication([])
wizard = MyWizard()
wizard.setWindowTitle('MyWizard Example')
wizard.show()
app.exec_()

# To Do
# write intro text
# write debrief text
# write instructions text
# code urn