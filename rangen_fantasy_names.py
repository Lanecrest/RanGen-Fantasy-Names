from rangen_words import rangen_word
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QStyleFactory, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QSlider, QLineEdit, QMessageBox, QCheckBox, QRadioButton, QButtonGroup, QFileDialog
from PyQt5.QtGui import QFont, QFontMetrics, QPalette, QPixmap, QPainter, QColor, QPen
import csv

class RanGenFantasyNames(QWidget):
    # initialize the app and call some starting functions
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RanGen Fantasy Names 3.1.1')
        self.max_syllables_range = 6
        self.init_ui()
        self.reset_values()
        self.generate_names()

    # function to reset the values to default
    def reset_values(self):
        self.var_beg_cons_prob = 0.8
        self.var_beg_cluster_prob = 0.2
        self.var_vowel_prob = 0.75
        self.var_end_cons_prob = 0.6
        self.var_end_cluster_prob = 0.15
        self.var_name_splitter = True
        self.var_splitter_char = ' '
        self.var_max_syllables = 4
        
        self.beg_cons_slider.setValue(int(self.var_beg_cons_prob * 100))
        self.beg_cluster_slider.setValue(int(self.var_beg_cluster_prob * 100))
        self.vowel_slider.setValue(int(self.var_vowel_prob * 100))
        self.end_cons_slider.setValue(int(self.var_end_cons_prob * 100))
        self.end_cluster_slider.setValue(int(self.var_end_cluster_prob * 100))
        self.name_splitter_check_box.setChecked(self.var_name_splitter)
        self.splitter_char_radio1.setChecked(True)
        self.max_syllables_radio['4'].setChecked(True)

    # function to generate names for the name text boxes that are not selected with a corresponding check box id (being checked off 'saves' the name from re-rolling)
    def generate_names(self):
        for i in range(10):
            box_id = f'{i+1}'
            if not self.name_check_box[box_id].isChecked():
                name = rangen_word(
                    beg_cons_prob=self.var_beg_cons_prob,
                    beg_cluster_prob=self.var_beg_cluster_prob,
                    vowel_prob=self.var_vowel_prob,
                    end_cons_prob=self.var_end_cons_prob,
                    end_cluster_prob=self.var_end_cluster_prob,
                    word_splitter=self.var_name_splitter,
                    splitter_char=self.var_splitter_char,
                    max_syllables=self.var_max_syllables
                )
                self.name_text_box[box_id].setText(name.title())  
        
    # function to copy to clipboard as text
    def copy_to_clipboard(self):
        # checks if a name box has a corresponding check box checked
        checked_name_boxes = [self.name_text_box[f'{i+1}'].text() for i in range(10) if self.name_check_box[f'{i+1}'].isChecked()]
        if not checked_name_boxes:  # check to do nothing if nothing is checked
            return
        text = '\n'.join(checked_name_boxes)
        QApplication.clipboard().setText(text)
        
    # function to copy to clipboard as an image
    def copy_to_clipart(self):
        # checks if a name box has a corresponded check box checked and 
        checked_name_boxes = [self.name_text_box[f'{i+1}'].text() for i in range(10) if self.name_check_box[f'{i+1}'].isChecked()]
        if not checked_name_boxes:
            return
        clipart_font = QFont('Consolas', 12, QFont.Bold)
        height = 20
        for name_text_box in checked_name_boxes:
            height += QFontMetrics(clipart_font).height()
        pixmap = QPixmap(220, height)
        pixmap.fill(QColor('#704214'))  # should match QPalette.Base as defined for the GUI
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor('#ffefe0'))   # should match QPalette.Text as defined for the GUI
        painter.setFont(clipart_font)
        painter.setPen(pen)
        # draw text for each checked line
        y = 20
        for name_text_box in checked_name_boxes:
            painter.drawText(5, y, name_text_box)
            y += QFontMetrics(clipart_font).height()
        painter.end()
        QApplication.clipboard().setPixmap(pixmap)
        
    # function to export names to a file
    def export_names(self):
        checked_name_boxes = [self.name_text_box[f'{i+1}'].text() for i in range(10) if self.name_check_box[f'{i+1}'].isChecked()]
        if not checked_name_boxes:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, 'Export to CSV', 'RanGen Fantasy Names', 'CSV Files (*.csv)')
        if not file_path:
            return
        with open(file_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for name in checked_name_boxes:
                writer.writerow([name])
        QMessageBox.information(self, 'Export', 'Selected names have been exported to ' + file_path)

    # function to toggle check boxes
    def toggle_checkboxes(self):
        toggle_button_text = self.toggle_button.text()
        for i in range(1, 11):
            if toggle_button_text == 'Select All':
                self.name_check_box[f'{i}'].setChecked(True)
                self.toggle_button.setText('Deselect All')
            elif toggle_button_text == 'Deselect All':
                self.name_check_box[f'{i}'].setChecked(False)
                self.toggle_button.setText('Select All')

    # function for about message box dialog
    def about_message(self):
        message_box = QMessageBox()
        message_box.setWindowTitle('About')
        message_box.setText(
            '<p>RanGen Fantasy Names procedurally generates names by joining up to four randomly generated syllables that are constructed following "consonant-vowel-consonant" conventions. If you would like to see more about the project, check out the <a href="https://github.com/Lanecrest/RanGen-Fantasy-Names">GitHub</a> page.</p>'
            '<p>Use the check boxes to select specific names you would like to work with. Selected names will also be ignored when rolling. You can copy selected names to your clipboard either as text or as an image. You can also export the selected names to a CSV file which will be appended after any existing entries.</p>'
            '<p>Use the settings at the bottom of the interface to adjust values. You can toggle whether long names will be split somewhere randomly and choose the symbol that splits them. You can also adjust the frequency of consonants, clusters, vowels, diphthongs, etc. These values will effect every syllable a name contains, which is another setting you can adjust to determine the maximum number of syllables a name can have.</p>'
            '<p align="center">RanGen Fantasy Names ©2023 <a href="https://www.lanecrest.com/">Lanecrest Tech</a></p>'
            )
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()
     
    # function to toggle whether long names will have a split in them
    def set_var_name_splitter(self, state):
        self.var_name_splitter = state == Qt.Checked
        
    # function to set what character splits the names
    def set_var_splitter_char(self, button):
        if button == self.splitter_char_radio1:
            self.var_splitter_char = ' '
        elif button == self.splitter_char_radio2:
            self.var_splitter_char = '\''
        elif button == self.splitter_char_radio3:
            self.var_splitter_char = '-'
            
    # functions to set the syllable generation values
    def set_var_beg_cons_prob(self, value):
            self.var_beg_cons_prob = value / 100

    def set_var_beg_cluster_prob(self, value):
            self.var_beg_cluster_prob = value / 100

    def set_var_vowel_prob(self, value):
            self.var_vowel_prob = value / 100

    def set_var_end_cons_prob(self, value):
            self.var_end_cons_prob = value / 100

    def set_var_end_cluster_prob(self, value):
            self.var_end_cluster_prob = value / 100
            
    def set_var_max_syllables(self, button):
        for i in range(self.max_syllables_range):
            radio_id = f'{i+1}' 
            if button == self.max_syllables_radio[radio_id]:
                self.var_max_syllables = radio_id

    # function to define the GUI and its widgets
    def init_ui(self):
        # create buttons for app menus
        self.generate_button = QPushButton('Roll')
        self.generate_button.setToolTip('Generate names for unchecked fields')
        self.generate_button.clicked.connect(self.generate_names) 

        self.toggle_button = QPushButton('Select All')
        self.toggle_button.setToolTip('Select or deselect all check boxes')
        self.toggle_button.clicked.connect(self.toggle_checkboxes)

        self.reset_button = QPushButton('Reset Values')
        self.reset_button.setToolTip('Resets values to defaults')
        self.reset_button.clicked.connect(self.reset_values)

        self.about_button = QPushButton('About')
        self.about_button.setToolTip('About the application')
        self.about_button.clicked.connect(self.about_message)

        self.quit_button = QPushButton('Quit')
        self.quit_button.setToolTip('Exit application')
        self.quit_button.clicked.connect(QApplication.instance().quit)

        self.clipboard_button = QPushButton('Copy as Text')
        self.clipboard_button.setToolTip('Copy selected names as text to clipboard')
        self.clipboard_button.clicked.connect(self.copy_to_clipboard)
        
        self.clipart_button = QPushButton('Copy as Image')
        self.clipart_button.setToolTip('Copy selected names as an image to clipboard')
        self.clipart_button.clicked.connect(self.copy_to_clipart)
        
        self.export_button = QPushButton('Export to CSV')
        self.export_button.setToolTip('Export selected names to a CSV file')
        self.export_button.clicked.connect(self.export_names)

        # create a grid for the menu buttons
        button_layout = QGridLayout()
        button_layout.addWidget(self.generate_button, 0, 0)
        button_layout.addWidget(self.about_button, 0, 1)
        button_layout.addWidget(self.reset_button, 0, 2)
        button_layout.addWidget(self.quit_button, 0, 3)

        button_layout.addWidget(self.toggle_button, 1, 0)
        button_layout.addWidget(self.clipboard_button, 1, 1)
        button_layout.addWidget(self.clipart_button, 1, 2)
        button_layout.addWidget(self.export_button, 1, 3)

 
        # create a grid for the name check and text boxes and style settings
        check_text_layout = QGridLayout()
        name_font = QFont('Consolas', 12, QFont.Bold)
        self.name_text_box = {}
        self.name_check_box = {}
        # create check and text boxes for the number of names that can be generated at a time and place them in the grid
        for i in range(10):
            box_id = f'{i+1}'          
            self.name_check_box[box_id] = QCheckBox()
            self.name_check_box[box_id].setChecked(False)
            check_text_layout.addWidget(self.name_check_box[box_id], i, 0)
            
            self.name_text_box[box_id] = QLineEdit()
            self.name_text_box[box_id].setFont(name_font)
            self.name_text_box[box_id].setReadOnly(True)
            check_text_layout.addWidget(self.name_text_box[box_id],i, 1)
            
        # create user variable setting inputs for the GUI
        settings_font = QFont()
        settings_font.setPointSize(7)

        # radio buttons to choose the maximum number of syllables that can generate
        user_settings_syllables = QHBoxLayout()
        self.max_syllables_label = QLabel('Maximum syllables to generate: ')
        self.max_syllables_label.setFont(settings_font)
        user_settings_syllables.addWidget(self.max_syllables_label)
        self.max_syllables_radio = {}
        self.max_syllables_radio_group = QButtonGroup()
        for i in range(self.max_syllables_range):
            radio_id = f'{i+1}'          
            self.max_syllables_radio[radio_id] = QRadioButton(radio_id)
            self.max_syllables_radio_group.addButton(self.max_syllables_radio[radio_id])
            user_settings_syllables.addWidget(self.max_syllables_radio[radio_id])
        for radio_button in self.max_syllables_radio_group.buttons():
            radio_button.setFont(settings_font)
        self.max_syllables_radio_group.buttonClicked.connect(self.set_var_max_syllables)

        # check box and radio buttons to toggle name split and splitter char
        self.name_splitter_check_box = QCheckBox('Split long names with:', self)
        self.name_splitter_check_box.setFont(settings_font)
        self.name_splitter_check_box.setChecked(True)
        self.name_splitter_check_box.stateChanged.connect(self.set_var_name_splitter)        

        self.splitter_char_radio_group = QButtonGroup()
        self.splitter_char_radio1 = QRadioButton('Space')
        self.splitter_char_radio_group.addButton(self.splitter_char_radio1)
        self.splitter_char_radio2 = QRadioButton('Apostrophe')
        self.splitter_char_radio_group.addButton(self.splitter_char_radio2)
        self.splitter_char_radio3 = QRadioButton('Dash')
        self.splitter_char_radio_group.addButton(self.splitter_char_radio3)
        for radio_button in self.splitter_char_radio_group.buttons():
            radio_button.setFont(settings_font)
        self.splitter_char_radio_group.buttonClicked.connect(self.set_var_splitter_char)

        user_settings_splitter = QHBoxLayout()        
        user_settings_splitter.addWidget(self.name_splitter_check_box)
        user_settings_splitter.addWidget(self.splitter_char_radio1)
        user_settings_splitter.addWidget(self.splitter_char_radio2)
        user_settings_splitter.addWidget(self.splitter_char_radio3)

        # sliders for the syllable generation values
        self.beg_cons_label = QLabel('Beginning Consonant more likely than Cluster/Nothing: ')
        self.beg_cons_label.setFont(settings_font)
        self.beg_cons_slider = QSlider(Qt.Horizontal)
        self.beg_cons_slider.setMinimum(1)
        self.beg_cons_slider.setMaximum(100)
        self.beg_cons_slider.valueChanged.connect(self.set_var_beg_cons_prob)

        self.beg_cluster_label = QLabel('Beginning Cluster more likely than Nothing: ')
        self.beg_cluster_label.setFont(settings_font)
        self.beg_cluster_slider = QSlider(Qt.Horizontal)
        self.beg_cluster_slider.setMinimum(1)
        self.beg_cluster_slider.setMaximum(100)
        self.beg_cluster_slider.valueChanged.connect(self.set_var_beg_cluster_prob)

        self.vowel_label = QLabel('Vowel more likely than Diphthong: ')
        self.vowel_label.setFont(settings_font)
        self.vowel_slider = QSlider(Qt.Horizontal)
        self.vowel_slider.setMinimum(1)
        self.vowel_slider.setMaximum(100)
        self.vowel_slider.valueChanged.connect(self.set_var_vowel_prob)

        self.end_cons_label = QLabel('Ending Consonant more likely than Cluster/Nothing: ')
        self.end_cons_label.setFont(settings_font)
        self.end_cons_slider = QSlider(Qt.Horizontal)
        self.end_cons_slider.setMinimum(1)
        self.end_cons_slider.setMaximum(100)
        self.end_cons_slider.valueChanged.connect(self.set_var_end_cons_prob)

        self.end_cluster_label = QLabel('Ending Cluster more likely than Nothing: ')
        self.end_cluster_label.setFont(settings_font)
        self.end_cluster_slider = QSlider(Qt.Horizontal)
        self.end_cluster_slider.setMinimum(1)
        self.end_cluster_slider.setMaximum(100)
        self.end_cluster_slider.valueChanged.connect(self.set_var_end_cluster_prob)
        
        user_settings_probs = QVBoxLayout()
        user_settings_probs.addWidget(self.beg_cons_label)
        user_settings_probs.addWidget(self.beg_cons_slider)       
        user_settings_probs.addWidget(self.beg_cluster_label)
        user_settings_probs.addWidget(self.beg_cluster_slider)       
        user_settings_probs.addWidget(self.vowel_label)
        user_settings_probs.addWidget(self.vowel_slider)
        user_settings_probs.addWidget(self.end_cons_label)
        user_settings_probs.addWidget(self.end_cons_slider)       
        user_settings_probs.addWidget(self.end_cluster_label)
        user_settings_probs.addWidget(self.end_cluster_slider)
        
        # finalize the window display as a vertical box and set the window title
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(check_text_layout)
        main_layout.addLayout(user_settings_syllables)
        main_layout.addLayout(user_settings_splitter)
        main_layout.addLayout(user_settings_probs)
        self.setLayout(main_layout)
        
# load the app using name=main
if __name__ == '__main__':
    # set the palette colors for the GUI
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#d5a05a'))    # window background color
    palette.setColor(QPalette.WindowText, QColor('#000000'))    # window font color
    palette.setColor(QPalette.Base, QColor('#704214'))  # text edit background color
    palette.setColor(QPalette.Text, QColor('#ffefe0'))  # text edit font color
    palette.setColor(QPalette.Button, QColor('#704214'))    # button background color
    palette.setColor(QPalette.ButtonText, QColor('#ffefe0'))    # button font color
    palette.setColor(QPalette.AlternateBase, QColor('#b8803c')) # table and dropdown background color
    palette.setColor(QPalette.ToolTipBase, QColor('#b8803c'))   # tooltip background color
    palette.setColor(QPalette.ToolTipText, QColor('#ffefe0'))   # tooltip font color
    palette.setColor(QPalette.BrightText, QColor('#ffefe0'))    # highlighted font color
    
    # set some other settings and run
    app = QApplication([])
    app.setStyle(QStyleFactory.create('Fusion'))
    app.setPalette(palette)
    rangen_fantasy_names = RanGenFantasyNames()
    rangen_fantasy_names.show()
    frame = rangen_fantasy_names.frameGeometry()
    frame.moveCenter(QDesktopWidget().availableGeometry().center())
    rangen_fantasy_names.move(frame.topLeft())
    app.exec_()