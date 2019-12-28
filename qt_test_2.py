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
        self.create_buttons()
        self.display_intro_screen()
        self.text = """What is the purpose of the study?
State the background and aim of the study. When will the study be completed?
Why have you been chosen?
You have been selected as you are a representative individual of society

Do you have to take part?
Taking part is entirely voluntary and refusal or withdrawal from the study at any time will involve no penalty 
or loss, now or in the future.

What do you need to do?
If you take part in the test you will be asked to make some selections based upon certain hypothetical,
computer based, decision scenarios.

Will the test cause any adverse effects?
The test is not expected to cause any emotional or physical distress and is entirely computer based with
only visual feedback.

What are the possible benefits of taking part?
No monetary benefits will be provided for completion of this task. Its only purpose is the recreation of
a well-known experiment in support of a Masters student’s core module coursework.

How will your data be protected?
All data will be identified only by a code, with personal details kept in a password protected file on a
secure and encrypted computer hard drive with access only by the immediate research team. We also operate
a fully GDPR compliant data storage, retention and deletion policy.

How will your data be used?
Results will be presented at conferences and written up in journals.  Results are normally presented in
terms of groups of individuals. If any individual data is presented, the data will be fully and untraceably
anonymous, without any means of identifying the individuals involved.  Depending on the nature of your proposed
project, you may need to include a statement indicating that the data collected during the course of the
project might be used for additional or subsequent research.

Who is the research being performed and sponsored by?
This research is being performed by UCL and is sponsored by ACME Corporation.

Are there any ethical considerations?
No - the project has also been reviewed by UCL’s Psychology Research Ethics Committee.
Should further contact be required, please do not hesitate to contact UCL’s Psychology department.

I confirm that I have read and understand the Participant Information Sheet
	I have had the opportunity to ask questions and had them answered
	I understand that all personal information will remain confidential and that all efforts will be made to ensure
 	I cannot be identified (except as might be required by law)
	I agree that data gathered in this study may be stored anonymously and securely, and may be used for future
 	research
	I understand that my participation is voluntary and that I am free to withdraw at any time without giving a
	reason
	I agree to take part in this study

A paper copy of this consent form is also available upon request"""



    def screen_clear(self):
        # remove old content
        self.content_layout.removeWidget(self.content)
        self.content.deleteLater()
        
    def create_buttons(self):
        # back, forward buttons wrapped in horizontal layout
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.vertical_layout)
        self.content_layout = QtWidgets.QVBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch()
        self.consent_check_box = QtWidgets.QCheckBox("I give consent")
        self.button_layout.addWidget(self.consent_check_box)
        self.back_button = QtWidgets.QPushButton('Back')
        self.back_button.clicked.connect(self.back_button_clicked)
        self.button_layout.addWidget(self.back_button)
        self.forward_button = QtWidgets.QPushButton('Next')
        self.forward_button.clicked.connect(self.forward_button_clicked)
        self.button_layout.addWidget(self.forward_button)
        self.age_spinbox = QtWidgets.QSpinBox()
        self.button_layout.addWidget(self.age_spinbox)
        self.gender_combobox = QtWidgets.QComboBox()
        self.gender_combobox.addItem("Female")
        self.gender_combobox.addItem("Male")
        self.gender_combobox.addItem("Other")
        self.gender_combobox.addItem("Prefer Not To Say")
        self.button_layout.addWidget(self.gender_combobox)
        self.edu_combobox = QtWidgets.QComboBox()
        self.edu_combobox.addItem("High School")
        self.edu_combobox.addItem("Associate's")
        self.edu_combobox.addItem("Bachelor's")
        self.edu_combobox.addItem("Master's")
        self.edu_combobox.addItem("PhD")
        self.edu_combobox.addItem("Other")
        self.edu_combobox.addItem("Prefer Not To Say")
        self.button_layout.addWidget(self.edu_combobox)
        self.vertical_layout.addLayout(self.button_layout)
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
        self.content = QtWidgets.QLabel('Intro Screen') # customize with your content
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
        self.content = QtWidgets.QLabel(self.text) # customize with your content
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
        self.content = QtWidgets.QLabel('Instruction Screen') # customize with your content
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
