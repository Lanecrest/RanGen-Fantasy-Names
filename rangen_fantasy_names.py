import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QMessageBox, QCheckBox, QStyleFactory
from PyQt5.QtGui import QFont, QPalette, QPixmap, QPainter, QColor, QPen, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

class RanGenFantasyNames(QWidget):
    # initialize the app and set some variables
    def __init__(self):
        super().__init__()
        # define the letters
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        self.diphthongs = ['ae', 'ai', 'au', 'ay', 'ea', 'ee', 'ei', 'eo', 'eu', 'ey', 'ia', 'ie', 'io', 'oa', 'oi', 'oo', 'ou', 'oy']
        self.consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
        self.beginning_clusters = ['bl', 'br', 'ch', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'gw', 'kl', 'ph', 'pl', 'pr', 'qu', 'rh', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'th', 'tr', 'tw', 'wh', 'wr', 'zh', 'scr', 'shr', 'sph', 'spl', 'spr', 'squ', 'str', 'thr']
        self.ending_clusters = ['ch', 'ck', 'ft', 'ld', 'lt', 'nd', 'ng', 'nk', 'nt', 'ph', 'pt', 'rd', 'rk', 'sh', 'sk', 'sp', 'st', 'th', 'dd', 'ff', 'gg', 'll', 'mm', 'pp', 'rr', 'ss', 'tt', 'zz', 'rth', 'tch']

        self.init_ui()
        self.generate_names()
    
    # function to toggle check boxes
    def toggle_checkboxes(self, state):
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
        if not checked_name_boxes:  # check to do nothing if nothing is checked
            return
        height = 20
        for i in range(10):
            if self.name_check_box[f"{i+1}"].isChecked():
                height += self.name_text_box[f"{i+1}"].fontMetrics().height()
        pixmap = QPixmap(200, height)
        pixmap.fill(QColor('#704214'))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        font = QFont("Consolas", 12, QFont.Bold)
        pen = QPen(QColor('#ffefe0'))
        painter.setFont(font)
        painter.setPen(pen)
        # draw text for each checked line
        y = 20
        for name_text_box in checked_name_boxes:
            painter.drawText(5, y, name_text_box)
            y += 20
        painter.end()
        QApplication.clipboard().setPixmap(pixmap)
        
    def about_message(self):
        message_box = QMessageBox()
        message_box.setWindowTitle('About')
        message_box.setText('RanGen Fantasy Names constructs randomly generated names by joining up to four syllables that are constructed following \'consonant-vowel-consonant\' conventions. If you would like to see more about the project, check out the <a href="https://github.com/Lanecrest/RanGen-Fantasy-Names">GitHub</a>')
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()

    # set and organize the widgets
    def init_ui(self):   
        # define buttons and what they do
        self.generate_button = QPushButton('Re-Roll All')
        self.generate_button.setToolTip('Re-Roll another set of random names')
        self.generate_button.clicked.connect(self.generate_names)
        
        self.reroll_button = QPushButton('Re-Roll Unselected')
        self.reroll_button.setToolTip('Re-Roll unselected names')
        self.reroll_button.clicked.connect(self.generate_selected_names)
        
        self.clipboard_button = QPushButton('Copy as Text')
        self.clipboard_button.setToolTip('Copy selected names as text to clipboard')
        self.clipboard_button.clicked.connect(self.copy_to_clipboard)
        
        self.clipart_button = QPushButton('Copy as Image')
        self.clipart_button.setToolTip('Copy selected names as an image to clipboard')
        self.clipart_button.clicked.connect(self.copy_to_clipart)
        
        self.toggle_button = QPushButton('Select All')
        self.toggle_button.clicked.connect(self.toggle_checkboxes)

        self.about_button = QPushButton('About')
        self.about_button.clicked.connect(self.about_message)

        self.quit_button = QPushButton('Exit')
        self.quit_button.clicked.connect(QApplication.instance().quit)
        
        # create the buttons in horizontal boxes
        button_layout_1 = QHBoxLayout()
        button_layout_2 = QHBoxLayout()
        button_layout_1.addWidget(self.generate_button)
        button_layout_1.addWidget(self.toggle_button)
        button_layout_1.addWidget(self.about_button)
        button_layout_1.addWidget(self.quit_button)
        button_layout_2.addWidget(QLabel('Selected Names: '))
        button_layout_2.addWidget(self.reroll_button)
        button_layout_2.addWidget(self.clipboard_button)
        button_layout_2.addWidget(self.clipart_button)
 
        # create pairings of check box and name box for each generated name in veritcal boxes
        check_layout = QVBoxLayout()
        text_layout = QVBoxLayout()
        self.name_text_box = {}
        self.name_check_box = {}
        check_layout.setSpacing(10)
        text_box_font = QFont("Consolas", 12)
        text_box_font.setBold(True)
        # create check boxes for each name
        for i in range(10):
            box_id = f"{i+1}"          
            self.name_check_box[box_id] = QCheckBox()
            self.name_check_box[box_id].setChecked(False)
            self.name_check_box[box_id].setFixedSize(20, 20)
            check_layout.addWidget(self.name_check_box[box_id])
        # create text boxes for each name
        for i in range(10):
            box_id = f"{i+1}"
            self.name_text_box[box_id] = QLineEdit()
            self.name_text_box[box_id].setFont(text_box_font)
            self.name_text_box[box_id].setReadOnly(True)
            text_layout.addWidget(self.name_text_box[box_id])

        # create a horizontal box for the check and text boxes
        check_text_layout = QHBoxLayout()
        check_text_layout.addLayout(check_layout)
        check_text_layout.addLayout(text_layout)
 
        # create the footer in a horizontal box
        foot_layout= QHBoxLayout()
        self.foot_link = QLabel('RanGen Fantasy Names ©2023 <a href="https://www.lanecrest.com/">Lanecrest Tech</a>')
        self.foot_link.setToolTip('Lanecrest Tech')
        self.foot_link.setOpenExternalLinks(True)
        foot_layout.addWidget(self.foot_link, alignment=QtCore.Qt.AlignHCenter)
        
        # finalize the window display as a vertical box and set the window title
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout_1)
        main_layout.addLayout(button_layout_2)
        main_layout.addLayout(check_text_layout)
        main_layout.addLayout(foot_layout)
        self.setLayout(main_layout)
        self.setWindowTitle('RanGen Fantasy Names 2.2')

    # define how syllables are generated
    def generate_syllable(self, prev_char=''):
        syllable = ''
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
                prev_char = consonant
        # generate the middle part of the syllable
        if random.random() < 0.75:
            # genearate a vowel
            vowel = random.choice(self.vowels)
            if len(syllable) > 0 and prev_char == syllable[-1]:
                vowel = random.choice([v for v in self.vowels if v != prev_char])
            syllable += vowel
            prev_char = vowel
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
                prev_char = consonant
        return syllable

    # generate a name based on the syllable generation rules
    def generate_name(self):
        name = ''
        # keep generating a name until it has at least one consonant or cluster
        while not any(c in self.consonants or c in self.beginning_clusters or c in self.ending_clusters for c in name):
            num_syllables = random.choices([1, 2, 3, 4], weights=[1, 3, 3, 3])[0]
            syllables = [self.generate_syllable() for _ in range(num_syllables)]
            name = ''.join(syllables)
            # insert a space between two syllables if there are more than a certain number of total letters generated
            if len(''.join(syllables)) > 10:
                i = random.randint(1, len(syllables) - 1)
                syllables.insert(i, ' ')
            name = ''.join(syllables)
        return name.title()

    # a function that when called generates multiple names at a time
    def generate_names(self):
        for i in range(10):
            box_id = f"{i+1}"   # create the box id numbers to be referenced
            self.name_text_box[box_id].clear()  # clear each box
            name = self.generate_name()
            self.name_text_box[box_id].setText(name)    # apply the name to the line edit box
    
    # a function to only generated names that are selected via check box
    def generate_selected_names(self):
        for i in range(10):
            box_id = f"{i+1}"
            if not self.name_check_box[box_id].isChecked():
                name = self.generate_name()
                self.name_text_box[box_id].setText(name)
        
# load the app. in an if statement so it doesn't break if called in another app
if __name__ == '__main__':
    # set the palette colors
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
    
    # load the app
    app = QApplication([])
    app.setStyle(QStyleFactory.create('Fusion'))
    app.setPalette(palette)
    rangen_fantasy_names = RanGenFantasyNames()
    rangen_fantasy_names.show()
    frame = rangen_fantasy_names.frameGeometry()
    frame.moveCenter(QDesktopWidget().availableGeometry().center())
    rangen_fantasy_names.move(frame.topLeft())
    app.exec_()
