# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:23:25 2019

@author: miketaylor
"""

from PyQt5 import QtWidgets, uic
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
            random_dist = ['Blue', 'Blue']
            random.shuffle(random_dist)
            ff_dist = ['Blue', 'Red']
            random.shuffle(ff_dist)
        elif self.urn_condition == 10:
            random_dist = ['Blue'] * 2 + ['Red'] * 8
            random.shuffle(random_dist)
            ff_dist = ['Blue'] * 5 + ['Red'] * 5
            random.shuffle(ff_dist)
        else:
            random_dist = ['Blue'] * 53 + ['Red'] * 47
            random.shuffle(random_dist)
            ff_dist = ['Blue'] * 50 + ['Red'] * 50
            random.shuffle(ff_dist)
        self.random_urn_distribution = random_dist
        self.ff_urn_distribution = ff_dist
        self.random_urn_draw_count = 0
        self.ff_urn_draw_count = 0
        self.results = []
    
        self.random_urn_position = random.choice([0, 1])  # 0 left/a, 1 right/b
        if self.random_urn_position == 0:
            self.window.left_urn_textbox.setText("Random Urn")
            self.window.right_urn_textbox.setText("50/50 Urn")
        else:
            self.window.left_urn_textbox.setText("50/50 Urn")
            self.window.right_urn_textbox.setText("Random Urn")
        self.draw_marble_button.clicked.connect(self.draw_marble_button_clicked)
            
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

    def is_task_complete(self, results):
        """
        Checks all activities, demographics etc have been submitted prior to
        allowing the participant to save and exit
        """
        return True
        #  return error for what is not yet submitted

    def urn_selected_check(self):
        if self.window.left_urn_a_radiobutton.isChecked():
            if self.random_urn_position == 0:
                urn_selected = 0
            else:
                urn_selected = 1
        elif self.window.right_urn_b_radiobutton.isChecked():
            if self.random_urn_position == 1:
                urn_selected = 0
            else:
                urn_selected = 1
        else:
            urn_selected = None
        return urn_selected

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
        csv_content = []
        count = 0
        for result in self.results:
            csv_content.append((username + ', ' + consent + ', ' + age + ', ' +
                                education + ', ' + gender + ', ' +
                                urn_condition + ', ' +
                                str(self.results[count][0]) + ', ' +  # run
                                str(self.results[count][1]) + ', ' +  # marble
                                str(self.results[count][2]) + ', ' +  # urn selected
                                str(self.results[count][3])))  # random urn pos
            count += 1
        return csv_content

    def marble_result(self):
        """
        blurb
        """
        urn_selected = self.urn_selected_check()
        if urn_selected is None:
            return "No urn selected..."
        else:
            if (urn_selected == 0 & self.random_urn_position == 0):
                marble_returned = self.random_urn_distribution[self.random_urn_draw_count]
                self.random_urn_draw_count += 1    
            elif (urn_selected == 1 & self.random_urn_position == 1):
                marble_returned = self.random_urn_distribution[self.random_urn_draw_count]
                self.random_urn_draw_count += 1
            else:
                marble_returned = self.ff_urn_distribution[self.ff_urn_draw_count]
                self.ff_urn_draw_count += 1
            run = self.ff_urn_draw_count + self.random_urn_draw_count
            self.results.append((run, marble_returned,
                                 urn_selected, self.random_urn_position))
            return marble_returned

    def draw_marble_button_clicked(self):
        marble_returned = self.marble_result()
        self.window.marble_result_textbox.setText(marble_returned)
        

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
            for result in results:
                self.csv_results_db.write(result)
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
# make random selection sequence (i.e. each of the six conditions, rather than the existing random each time)