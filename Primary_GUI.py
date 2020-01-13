# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:23:25 2019

@author: DZLR3
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import random
import sys
from os import listdir


class Primary_GUI(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # File locations
        self.condition_combo_dynamic_loc = \
            'current_state\\condition_combo_file_dynamic.txt'
        self.condition_combo_master_loc = \
            'config\\condition_combo_file_master.txt'
        self.ui_file_loc = 'ui\\Screen.ui'
        self.intro_text_file_loc = 'text\\Introduction.txt'
        self.disclaimer_text_file_loc = 'text\\Disclaimer.txt'
        self.instruct_text_file_loc = 'text\\Instructions.txt'
        self.debrief_text_file_loc = 'text\\Debrief.txt'
        self.config_text_file_loc = 'config\\config.txt'

        # Import the QT designer UI and name the window
        self.window = uic.loadUi(self.ui_file_loc, self)
        self.setWindowTitle('Ellsberg, Pullman and Colman Test')

        # Open the 'database' table, set relevant file loc
        self.csv_results_db = open('results\\csv_results_db.csv', 'a')

        # Import images & set front screen image
        self.pixmap_dict = {}
        self.set_image_dict()
        self.window.front_screen.setPixmap(self.pixmap_dict["Front_Screen"])

        # Adjust the combobox content to support the valid values
        self.set_gender_types()
        self.set_edu_types()

        # Set random urn condition (i.e. marble count), distribution
        # and position
        (self.random_urn_position,
         self.urn_condition,
         self.red_marbles_rand,
         self.blue_marbles_rand) = self.get_random_partic_cond()
        self.random_urn_draw_count = 0
        self.ff_urn_draw_count = 0
        self.results = []
        self.set_urn_random_dist()
        self.set_random_urn_info()

        # Get the config file and set the maximum trials (i.e. the most draws)
        # and the required trials (i.e. the minimum draws).  1 and 1 in the
        # default case, but support added for more diverse selection
        # experiments
        self.max_trials, self.req_trials = self.get_config()

        # Connect the buttons and tabs to the relevant functions
        self.window.back_btn.clicked.connect(self.back_button_clicked)
        self.window.next_btn.clicked.connect(self.next_button_clicked)
        self.window.save_btn.clicked.connect(self.save_button_clicked)
        self.window.tabs.currentChanged.connect(self.refresh_nav_buttons)
        self.window.tabs.currentChanged.connect(self.check_disclaimer_nav)

        # Import all the text from external sources (simplifies future changes)
        # adjust with the appropriate text and fill the text boxes
        # and set to read only to prevent user edits
        self.get_set_text()

        # Set the default visibility for the nav buttons and show the screen
        self.window.back_btn.hide()
        self.window.save_btn.hide()
        self.window.error_textbox.hide()
        self.window.show()

    def get_config(self):
        """
        Reads the config file and returns the max_trials and req_trials
        """
        config_file = open(self.config_text_file_loc, 'r').read()
        max_trials = int(config_file.split('\n')[0].split(' = ')[1])
        req_trials = int(config_file.split('\n')[1].split(' = ')[1])
        return (max_trials, req_trials)

    def set_image_dict(self):
        """
        Import and set the images for the urns into the pixmap_dict dictionary
        for importing into the gui.  Images must pngs and named according to
        the scheme colour/grey + _ + 5050/random + _ + condition(i.e. number of
        marbles).  e.g. colour_5050_100.png
        """
        files = listdir('images')
        for file in files:
            if file == 'Front_Screen.png':
                pixmap = QPixmap('images\\' + file)
                pixmap = pixmap.scaled(1001, 811,
                                       Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation)
                self.pixmap_dict['Front_Screen'] = pixmap
            elif file.endswith('.png'):
                dict_key = file[:-4].split('_')  # condition, random, colour
                dict_key[2] = int(dict_key[2])
                pixmap = QPixmap('images\\' + file)
                pixmap = pixmap.scaled(350, 525,
                                       Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation)
                self.pixmap_dict[tuple(dict_key)] = pixmap
            else:
                print('FYI - Non png file detected in image folder - ', file)

    def set_random_urn_info(self):
        """
        Sets the urn that is random (i.e. not 50/50) based on the
        random_urn_position varibale pulled from the file.
        NB - counterintuitively 1 denotes left NOT right
        """
        if self.random_urn_position == 1:  # 1 denotes random urn on left
            self.window.left_urn_textbox.setText("Random Urn (B)")
            self.window.urn_left_image.setPixmap(
                    self.pixmap_dict[("grey", "random", self.urn_condition)])
            self.window.right_urn_textbox.setText("50/50 Urn (A)")
            self.window.urn_right_image.setPixmap(
                    self.pixmap_dict[("colour", "5050", self.urn_condition)])
        else:
            self.window.left_urn_textbox.setText("50/50 Urn (A)")
            self.window.urn_left_image.setPixmap(
                    self.pixmap_dict[("colour", "5050", self.urn_condition)])
            self.window.right_urn_textbox.setText("Random Urn (B)")
            self.window.urn_right_image.setPixmap(
                    self.pixmap_dict[("grey", "random", self.urn_condition)])
        self.window.left_urn_textbox.setAlignment(Qt.AlignCenter)
        self.window.right_urn_textbox.setAlignment(Qt.AlignCenter)
        self.draw_marble_button.clicked.connect(
          self.draw_marble_button_clicked)

    def set_urn_random_dist(self):
        """
        Sets the random distribution of the urn, using the ratios in the
        original paper and the random.shuffle function to randomise the
        outcome (random seeds were not used owing to the need to make it
        random per participant, but could be used, and iterated to support
        improved reproducibility)
        """
        self.red_marbles_ff = int(self.urn_condition/2)
        self.blue_marbles_ff = int(self.urn_condition/2)
        self.all_marbles = self.urn_condition
        if self.blue_marbles_rand + self.red_marbles_rand != self.all_marbles:
            print('''Warning, distribution not correct, blue marble count plus
                  red marble count does not match the urn size''')
        random_dist = (['Blue'] * self.blue_marbles_rand +
                       ['Red'] * self.red_marbles_rand)
        ff_dist = (['Blue'] * self.blue_marbles_ff +
                   ['Red'] * self.red_marbles_ff)
        random.shuffle(random_dist)
        random.shuffle(ff_dist)
        self.random_urn_distribution = random_dist
        self.ff_urn_distribution = ff_dist

    def set_gender_types(self):
        """
        Sets the gender types for the combobox.  Presumed to be relatively
        static, but could be altered to support imports for more non-code
        adjustability
        """
        gender_list = ['', 'Prefer Not To Say', 'Female', 'Male', 'Other']
        for gender in gender_list:
            self.window.gender_combobox.addItem(gender)

    def set_edu_types(self):
        """
        Sets the education types for the combobox.  Presumed to be relatively
        static, but could be altered to support imports for more non-code
        adjustability
        """
        education_list = ['', 'High School', 'Bachelors', 'Masters', 'PhD',
                          'Other']
        for education in education_list:
            self.window.edu_combobox.addItem(education)

    def set_cond_all(self, condition_combo_file):
        """
        Reads either the master condition list or the list that is stored per
        trial and updates teh MyWizard class with the current conditions
        and the remaining future conditions in the condition_combo_lst, then
        shuffles them to randomise the remaining combos in the combination
        run
        """
        self.condition_combo_lst = []
        lines = condition_combo_file.readlines()
        for line in lines:
            combo = line.strip('\n').strip('(').strip(')').split(',')
            combo = (int(combo[0]),
                     int(combo[1]),
                     int(combo[2]),
                     int(combo[3]),)
            self.condition_combo_lst.append(combo)
        random.shuffle(self.condition_combo_lst)

    def get_random_partic_cond(self):
        """
        Gets the random conditions per particpant, with the combination of
        urn position and urn marble count resulting in 6 differnt participant
        conditions. First an attempt to import the prioir history is made
        if no prioir history is available a new randomised list is created
        with the condition tuples.  If history is available, then the top most
        condition tuple is read and returned as a tuple.  Iteration of the list
        only occurs after the particpant saves (see set_next_partic_cond())
        to prevent loss of a condition (and unbalance of the data) owing to
        a ui failure or partipant abandoini
        """
        condition_combo_file = open(self.condition_combo_dynamic_loc, 'r')
        if condition_combo_file.readline() == '':
            condition_combo_file.close()
            condition_combo_file = open(self.condition_combo_master_loc, 'r')
            self.set_cond_all(condition_combo_file)
            condition_combo_file.close()
            print('new combo list created from master - ',
                  self.condition_combo_lst)
        else:
            condition_combo_file.close()
            condition_combo_file = open(self.condition_combo_dynamic_loc, 'r')
            self.set_cond_all(condition_combo_file)
            condition_combo_file.close()
            print('old combo list read from drive - ',
                  self.condition_combo_lst)
        return(self.condition_combo_lst[0])

    def set_next_partic_cond(self):
        """
        Sets the condition combination file with all but the current condition
        supporting the randomised (but balanced) approach for participant
        conditions
        """
        condition_combo_file = open(self.condition_combo_dynamic_loc, 'w')
        for combo in self.condition_combo_lst[1:]:
            condition_combo_file.write(str(combo) + '\n')
            print('new combo entry created', combo)
        condition_combo_file.close()

    def back_button_clicked(self):
        """
        Dictates the actions for clicking the back button on a given screen
        using the screen_fxn_dict dictionary that houses the screen dispay
        functions
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
        functions
        """
        self.window.tabs.setCurrentIndex(self.window.tabs.currentIndex() + 1)
        self.window.next_btn.show()
        self.window.back_btn.show()
        if self.window.tabs.currentIndex() == 5:
            self.window.next_btn.hide()
            self.show_save_check()

    def check_disclaimer_nav(self):
        """
        Ensures navigation cannot happen past the  disclaimer screen unless
        consent has been provided via the consent_checkbox
        """
        if self.window.consent_checkbox.isChecked() is False:
            if self.window.tabs.currentIndex() > 1:
                self.window.tabs.setCurrentIndex(1)
                self.window.save_btn.hide()
                self.window.back_btn.show()
                self.window.next_btn.show()
                self.refresh_nav_buttons()
            else:
                self.refresh_nav_buttons()
        else:
            self.refresh_nav_buttons()

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
            self.show_debrief_check()
            self.window.next_btn.hide()
            self.window.back_btn.show()
        else:
            self.window.next_btn.show()
            self.window.back_btn.show()
            self.window.save_btn.hide()

    def check_task_complete(self):
        """
        Checks all activities, demographics etc have been submitted prior to
        allowing the participant to save and exit.  Should tasks not be
        complete an error message will be supplied to the user detailing
        the issue(s)
        """
        complete = True
        error_message = 'The following errors are preventing saving: '
        if len(self.window.username_textbox.text()) > 0:
            complete *= True
        else:
            complete *= False
            error_message += 'username is blank, '
        if self.window.consent_checkbox.isChecked():
            complete *= True
        else:
            complete *= False
            error_message += 'consent was not provided, '
        if self.window.age_spinbox.value() > 17:
            complete *= True
        else:
            complete *= False
            error_message += 'must be an adult (18+) to participate, '
        if str(self.window.edu_combobox.currentText()) != '':
            complete *= True
        else:
            complete *= False
            error_message += 'education level was not provided, '
            print(self.window.edu_combobox.currentText())
        if str(self.window.gender_combobox.currentText()) != '':
            complete *= True
        else:
            complete *= False
            error_message += 'gender was not provided, '
            print(self.window.gender_combobox.currentText())
        trial = self.ff_urn_draw_count + self.random_urn_draw_count
        trial_delta_req = trial - self.req_trials
        trial_delta_max = trial - self.max_trials
        print(self.req_trials, self.max_trials, trial)
        if trial == self.req_trials:
            complete *= True
        elif trial < self.req_trials:
            error_message += (str(abs(trial_delta_req)) +
                              'too few marble draws executed, ')
        elif trial > self.max_trials:
            error_message += (str(abs(trial_delta_max)) +
                              'too many marble draws executed (restart the app), ')        
        error_message = error_message[:-2] + '.'
        return (complete, error_message)

    def check_urn_selected(self):
        """
        Selects which urn (i.e. random of fifty fifty/ff), is selected
        when a users selects a radio button
        NB there is scope for confusion between urn selection (1 = random)
        and random urn position (1 = left).  Care should be taken when
        amending this function
        """
        if self.window.left_urn_a_radiobutton.isChecked():
            if self.random_urn_position == 0:
                urn_selected = 0  # fifty fifty
            else:
                urn_selected = 1  # random
        elif self.window.right_urn_b_radiobutton.isChecked():
            if self.random_urn_position == 1:
                urn_selected = 0  # fifty fifty
            else:
                urn_selected = 1  # random
        else:
            urn_selected = None
        return urn_selected

    def get_save_details(self):
        """
        Get the all the details from the experiment (incl. demographics and
        consent), and cast them into a csv ready string, then return the 
        content as a list
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
                                str(self.results[count][2]) + ', ' +  # urn chosen
                                str(self.results[count][3])))  # random urn pos
            count += 1
        return csv_content

    def get_marble_result(self):
        """
        Checks the marble returned from the given urn based upon the shuffled
        marble distribution for the fifty fifty (ff) and random urns
        """
        urn_selected = self.check_urn_selected()
        trial = self.ff_urn_draw_count + self.random_urn_draw_count

        # check if any urn has been selected
        if urn_selected is None:
            return "No urn selected..."

        # check that the maximum number of trials hasn't been exceeded
        if trial >= self.max_trials:
            return 'No more draws allowed, the experiment is over'

        # check the urn selected (1 is the ranodm urn) and draw the next marble
        # in sequence (or announce the urn is empty) and append to result list
        if urn_selected == 1:
            if self.random_urn_draw_count >= len(self.random_urn_distribution):
                marble_returned = 'The random urn selected is now empty'
            else:
                index = self.random_urn_draw_count
                marble_returned = self.random_urn_distribution[index]
                self.random_urn_draw_count += 1
                print('random urn selected')
        else:
            if self.ff_urn_draw_count >= len(self.ff_urn_distribution):
                marble_returned = 'The 50 50 urn selected is now empty'
            else:
                index = self.ff_urn_draw_count
                marble_returned = self.ff_urn_distribution[index]
                self.ff_urn_draw_count += 1
                print('5050 urn selected')
        self.results.append((trial, marble_returned,
                             urn_selected, self.random_urn_position))
        return marble_returned

    def draw_marble_button_clicked(self):
        """
        Updates the screen with the resultant marble when the draw marble
        button is clicked
        """
        marble_returned = self.get_marble_result()
        self.window.marble_result_textbox.setText(marble_returned)
        self.window.marble_result_textbox.setAlignment(Qt.AlignCenter)

    def show_save_check(self):
        """
        Check whether the save button should be shown, based upon the
        completion of all the relevant criteria (consent, demographics, test)
        """
        if self.window.consent_checkbox.isChecked():
            self.window.save_btn.show()
        else:
            self.window.save_btn.hide()

    def show_debrief_check(self):
        """
        Check whether the save button should be shown, based upon the
        completion of all the relevant criteria (consent, demographics, test)
        """
        trial = self.ff_urn_draw_count + self.random_urn_draw_count
        if trial >= self.req_trials:
            self.window.debrief_textbox.setText(self.debrief_text)
        else:
            pass

    def save_button_clicked(self):
        """
        Saves the demographics to csv, closes the csv, sets the remaining
        random conditions in the batch and exits the application
        """
        results = self.get_save_details()
        (validity, error_message) = self.check_task_complete()
        if validity:
            for result in results:
                self.csv_results_db.write(result)
                self.csv_results_db.write('\n')
            self.csv_results_db.close()
            self.set_next_partic_cond()
            sys.exit(QtWidgets.QApplication([]).exec_())
        else:
            self.window.error_textbox.show()
            self.window.error_textbox.setText(error_message)
            self.window.error_textbox.setReadOnly(True)

    def get_set_text(self):
        """
        Gets the text from the file locations and embeds it into the gui
        text boxs (made read only to prevent user edits)
        """
        self.intro_text = open(self.intro_text_file_loc, 'r').read()
        self.window.intro_textbox.setText(self.intro_text)
        self.window.intro_textbox.setReadOnly(True)
        self.disclaimer_text = open(self.disclaimer_text_file_loc, 'r').read()
        self.window.disclaimer_textbox.setText(self.disclaimer_text)
        self.window.disclaimer_textbox.setReadOnly(True)
        self.instruction_text = open(self.instruct_text_file_loc, 'r').read()
        self.instruction_text = self.instruction_text.replace(
                                  'red_marble_count_5050',
                                  str(self.red_marbles_ff))
        self.instruction_text = self.instruction_text.replace(
                                  'blue_marble_count_5050',
                                  str(self.blue_marbles_ff))
        self.instruction_text = self.instruction_text.replace(
                                  'total_marbles',
                                  str(self.all_marbles))
        self.window.instr_textbox.setText(self.instruction_text)
        self.window.instr_textbox.setReadOnly(True)
        self.debrief_text = open(self.debrief_text_file_loc, 'r').read()
        self.window.debrief_textbox.setText('Experiment not yet complete...')
        self.window.instr_textbox.setReadOnly(True)
