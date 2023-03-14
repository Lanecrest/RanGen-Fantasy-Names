import random, csv
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QMessageBox, QCheckBox, QRadioButton, QButtonGroup, QStyleFactory, QFileDialog
from PyQt5.QtGui import QFont, QFontMetrics, QPalette, QPixmap, QPainter, QColor, QPen, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

class RanGenFantasyNames(QWidget):
    # initialize the app and set some variables
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RanGen Fantasy Names 2.3')
        self.init_ui()
        
        # create default settings for the variables
        self.var_name_splitter = False
        self.var_splitter_char = "'"
        
        # define the letters
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        self.diphthongs = ['ae', 'ai', 'au', 'ay', 'ea', 'ee', 'ei', 'eo', 'eu', 'ey', 'ia', 'ie', 'io', 'oa', 'oi', 'oo', 'ou', 'oy']
        self.consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
        self.beginning_clusters = ['bl', 'br', 'ch', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'gw', 'kl', 'ph', 'pl', 'pr', 'qu', 'rh', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'th', 'tr', 'tw', 'wh', 'wr', 'zh', 'scr', 'shr', 'sph', 'spl', 'spr', 'squ', 'str', 'thr']
        self.ending_clusters = ['ch', 'ck', 'ft', 'ld', 'lt', 'nd', 'ng', 'nk', 'nt', 'ph', 'pt', 'rd', 'rk', 'sh', 'sk', 'sp', 'st', 'th', 'dd', 'ff', 'gg', 'll', 'mm', 'pp', 'rr', 'ss', 'tt', 'zz', 'rth', 'tch']

    # function to toggle check boxes
    def toggle_checkboxes(self):
        checked = all([self.name_check_box[f"{i}"].isChecked() for i in range(1, 11)])
        for i in range(1, 11):
            self.name_check_box[f"{i}"].setChecked(not checked)
        if checked:
            self.toggle_button.setText("Select All")
        else:
            self.toggle_button.setText("Deselect All")
        
    # function to copy to clipboard as text
    def copy_to_clipboard(self):
        # checks if a name box has a corresponding check box checked
        checked_name_boxes = [self.name_text_box[f"{i+1}"].text() for i in range(10) if self.name_check_box[f"{i+1}"].isChecked()]
        if not checked_name_boxes:  # check to do nothing if nothing is checked
            return
        text = '\n'.join(checked_name_boxes)
        QApplication.clipboard().setText(text)
        
    # function to copy to clipboard as an image
    def copy_to_clipart(self):
        # checks if a name box has a corresponded check box checked and 
        checked_name_boxes = [self.name_text_box[f"{i+1}"].text() for i in range(10) if self.name_check_box[f"{i+1}"].isChecked()]
        if not checked_name_boxes:
            return
        font = QFont("Consolas", 12, QFont.Bold)
        height = 20
        for name_text_box in checked_name_boxes:
            height += QFontMetrics(font).height()
        pixmap = QPixmap(220, height)
        pixmap.fill(QColor('#704214'))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor('#ffefe0'))
        painter.setFont(font)
        painter.setPen(pen)
        # draw text for each checked line
        y = 20
        for name_text_box in checked_name_boxes:
            painter.drawText(5, y, name_text_box)
            y += QFontMetrics(font).height()
        painter.end()
        QApplication.clipboard().setPixmap(pixmap)
        
    # function to export names to a file
    def export_names(self):
        checked_name_boxes = [self.name_text_box[f"{i+1}"].text() for i in range(10) if self.name_check_box[f"{i+1}"].isChecked()]
        if not checked_name_boxes:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "RanGen Fantasy Names", "CSV Files (*.csv)")
        if not file_path:
            return
        with open(file_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for name in checked_name_boxes:
                writer.writerow([name])
        QMessageBox.information(self, "Export", "Selected names have been exported to the file.")
    
    # function for about message box dialog
    def about_message(self):
        message_box = QMessageBox()
        message_box.setWindowTitle('Story')
        message_box.setText('<p>RanGen Fantasy Names procedurally generates names by joining up to four randomly generated syllables that are constructed following "consonant-vowel-consonant" conventions. If you would like to see more about the project, check out the <a href="https://github.com/Lanecrest/RanGen-Fantasy-Names">GitHub</a> page.</p>'
        '<p>Use the check boxes to select specific names you would like to work with. Selected names will also be ignored when re-rolling. You can copy selected names to your clipboard either as text or as an image. You can also export the selected names to a CSV file which will be appended after any existing entries.</p>')
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()
        
    # function to generate names for the name text boxes that are not checked by their corresponding check box id
    def generate_targeted_names(self):
        for i in range(10):
            box_id = f"{i+1}"
            if not self.name_check_box[box_id].isChecked():
                name = self.generate_name(name_splitter=self.var_name_splitter, splitter_char=self.var_splitter_char)
                self.name_text_box[box_id].setText(name)
        
    # function to toggle whether long names will have a split in them
    def set_var_name_splitter(self, state):
        self.var_name_splitter = state == Qt.Checked
        
    # function to set what character splits the names
    def set_var_splitter_char(self, button):
        if button == self.splitter_char_radio_button1:
            self.var_splitter_char = "'"
        elif button == self.splitter_char_radio_button2:
            self.var_splitter_char = "-"
        elif button == self.splitter_char_radio_button3:
            self.var_splitter_char = " "

    # function to define the GUI and its widgets
    def init_ui(self):
        # create buttons for app menus
        self.generate_button = QPushButton('Roll')
        self.generate_button.setToolTip('Generate names for unchecked fields')
        self.generate_button.clicked.connect(self.generate_targeted_names)
        
        self.toggle_button = QPushButton('Select All')
        self.toggle_button.clicked.connect(self.toggle_checkboxes)

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
        button_layout.addWidget(self.toggle_button, 0, 1)
        button_layout.addWidget(self.about_button, 0, 2)
        button_layout.addWidget(self.quit_button, 0, 3)
        
        button_layout.addWidget(QLabel('Selected Names: '), 1, 0)
        button_layout.addWidget(self.clipboard_button, 1, 1)
        button_layout.addWidget(self.clipart_button, 1, 2)
        button_layout.addWidget(self.export_button, 1, 3)
 
        # create a grid for the name check and text boxes and style settings
        check_text_layout = QGridLayout()
        self.name_text_box = {}
        self.name_check_box = {}
        text_box_font = QFont("Consolas", 12)
        text_box_font.setBold(True)
        # create check and text boxes for each name and place them in the grid
        for i in range(10):
            box_id = f"{i+1}"          
            self.name_check_box[box_id] = QCheckBox()
            self.name_check_box[box_id].setChecked(False)
            check_text_layout.addWidget(self.name_check_box[box_id], i, 0)
            
            self.name_text_box[box_id] = QLineEdit()
            self.name_text_box[box_id].setFont(text_box_font)
            self.name_text_box[box_id].setReadOnly(True)
            check_text_layout.addWidget(self.name_text_box[box_id],i, 1)
            
        # create user variable setting inputs
        self.name_splitter_check_box = QCheckBox('Split long names with', self)
        self.name_splitter_check_box.setChecked(False)
        self.name_splitter_check_box.stateChanged.connect(self.set_var_name_splitter)
             
        self.spliter_char_button_group = QButtonGroup()
        self.splitter_char_radio_button1 = QRadioButton("Apostrophe")
        self.splitter_char_radio_button2 = QRadioButton("Dash")
        self.splitter_char_radio_button3 = QRadioButton("Space")
        self.spliter_char_button_group.addButton(self.splitter_char_radio_button1)
        self.spliter_char_button_group.addButton(self.splitter_char_radio_button2)
        self.spliter_char_button_group.addButton(self.splitter_char_radio_button3)
        self.splitter_char_radio_button1.setChecked(True)
        self.spliter_char_button_group.buttonClicked.connect(self.set_var_splitter_char)
        
        # create a grid for the setting inputs
        user_settings_layout = QGridLayout()
        user_settings_layout.addWidget(self.name_splitter_check_box, 0, 0)
        user_settings_layout.addWidget(self.splitter_char_radio_button1, 0, 1)
        user_settings_layout.addWidget(self.splitter_char_radio_button2, 0, 2)
        user_settings_layout.addWidget(self.splitter_char_radio_button3, 0, 3)
        
 
        # create a footer in a centered horizontal box
        foot_layout = QHBoxLayout()
        self.foot_link = QLabel('RanGen Fantasy Names ©2023 <a href="https://www.lanecrest.com/">Lanecrest Tech</a>')
        self.foot_link.setOpenExternalLinks(True)
        foot_layout.addWidget(self.foot_link, alignment=QtCore.Qt.AlignHCenter)
        
        # finalize the window display as a vertical box and set the window title
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(check_text_layout)
        main_layout.addLayout(user_settings_layout)
        main_layout.addLayout(foot_layout)
        self.setLayout(main_layout)

    # function define how syllables are generated
    def generate_syllable(self):
        syllable = ''
        prev_char = ''
        # generate the first part of the syllable
        if random.random() < 0.2:
            # generate a beginning cluster
            beginning_cluster = random.choice(self.beginning_clusters)
            if len(syllable) > 0 and prev_char == syllable[-1]:
                beginning_cluster = random.choice([b for b in self.beginning_clusters if b[0] != prev_char])
            syllable += beginning_cluster
            prev_char = beginning_cluster[-1]
        else:
            # generate a consonant or no consonant
            if random.random() < 0.8:
                consonant = random.choice(self.consonants)
                if len(syllable) > 0 and prev_char == syllable[-1]:
                    consonant = random.choice([c for c in self.consonants if c != prev_char])
                syllable += consonant
                prev_char = consonant[-1]
        # generate the middle part of the syllable
        if random.random() < 0.75:
            # genearate a vowel
            vowel = random.choice(self.vowels)
            if len(syllable) > 0 and prev_char == syllable[-1]:
                vowel = random.choice([v for v in self.vowels if v != prev_char])
            syllable += vowel
            prev_char = vowel[-1]
        else:
            # generate a diphthong
            diphthong = random.choice(self.diphthongs)
            if len(syllable) > 0 and prev_char == syllable[-1]:
                diphthong = random.choice([d for d in self.diphthongs if d[0] != prev_char])
            syllable += diphthong
            prev_char = diphthong[-1]
        # generate the last part of the syllable
        if random.random() < 0.15:
            # generate an ending cluster
            ending_cluster = random.choice(self.ending_clusters)
            if len(syllable) > 0 and prev_char == syllable[-1]:
                ending_cluster = random.choice([e for e in self.ending_clusters if e[0] != prev_char])
            syllable += ending_cluster
            prev_char = ending_cluster[-1]
        else:
            # generate a consonant or no consonant
            if random.random() < 0.6:
                consonant = random.choice(self.consonants)
                if len(syllable) > 0 and prev_char == syllable[-1]:
                    consonant = random.choice([c for c in self.consonants if c != prev_char])
                syllable += consonant
                prev_char = consonant[-1]
        return syllable

    # function to generate a name based on the syllable generation rules
    def generate_name(self, name_splitter='', splitter_char=''):
        name = ''
        while True:
            num_syllables = random.choices([1, 2, 3, 4], weights=[1, 3, 3, 2])[0] # this makes names with more than one syllable favored
            syllables = [self.generate_syllable() for _ in range(num_syllables)]
            name = ''.join(syllables)
            # check if a single letter repeats itself too many times and regenrate the name if so
            for i, letter in enumerate(name):
                if i > 1 and letter == name[i-1] and letter == name[i-2]:
                    name = ''
                    break
            # check if the name contains at least one consonant or cluster so a name that is only vowels isn't generated
            if any(c in self.consonants or c in self.beginning_clusters or c in self.ending_clusters for c in name):
                break
        # insert an apostrophe between syllables if there are more than a certain number of total letters generated
        if len(''.join(syllables)) > 10 and name_splitter:
            i = random.randint(1, len(syllables) - 1)
            syllables.insert(i, splitter_char)
        name = ''.join(syllables)
        return name.title()
        
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
