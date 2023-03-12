import random, os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QStyleFactory, QMessageBox
from PyQt5.QtGui import QFont, QPalette, QColor, QDesktopServices, QPixmap, QClipboard
from PyQt5.QtCore import Qt, QUrl

class FantasyNameGenerator(QWidget):
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
        
    # create a function to copy to clipboard as an image
    def copy_to_clipboard(self):
        pixmap = self.names_text_edit.grab()
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(pixmap)

    # set and organize the widgets
    def init_ui(self):
        # create a function to open links
        def handle_link(url):
            QDesktopServices.openUrl(QUrl(url))
        
        # define buttons and what they do
        self.generate_button = QPushButton('Generate')
        self.generate_button.setFixedWidth(125)
        self.generate_button.clicked.connect(self.generate_names)
        self.copy_button = QPushButton('Copy as Image')
        self.copy_button.setFixedWidth(125)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.quit_button = QPushButton('Quit')
        self.quit_button.setFixedWidth(125)
        self.quit_button.clicked.connect(QApplication.instance().quit)

        # define the text edit box that will contain the generated names
        self.names_text_edit = QTextEdit()
        text_edit_font = QFont("Consolas", 12)
        text_edit_font.setBold(True)
        self.names_text_edit.setFont(text_edit_font)
        self.names_text_edit.setReadOnly(True)

        # create the buttons in a horizontal box
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.quit_button)
 
        # create the footer in a horizontal box
        foot_layout= QHBoxLayout()
        foot_link = QLabel('Fantasy Name Generator ©2023 <a href="https://www.lanecrest.com/">Lanecrest Tech</a>')
        foot_link.setOpenExternalLinks(True)
        foot_link.linkActivated.connect(handle_link)
        foot_layout.addWidget(foot_link, alignment=QtCore.Qt.AlignHCenter)

        # create a veritcal box for the main display and layer the buttons, text edit, and footer in that order
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(QLabel('Click \'Generate\' for another set of random names'))
        main_layout.addWidget(self.names_text_edit)
        main_layout.addLayout(foot_layout)
        
        # finalize the window display and set the window title
        self.setLayout(main_layout)
        self.setWindowTitle('Fantasy Name Generator 2.1')

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
        self.names_text_edit.clear()
        for i in range(8):
            self.names_text_edit.append(self.generate_name() + '\n')
        
# load the app. in an if statement so it doesn't break if called in another app
if __name__ == '__main__':
    # set the palette colors
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#d5a05a')) # window background color
    palette.setColor(QPalette.WindowText, QColor('#ffefe0')) # window font color
    palette.setColor(QPalette.Base, QColor('#704214')) # text edit background color
    palette.setColor(QPalette.Text, QColor('#ffefe0')) # text edit font color
    palette.setColor(QPalette.Button, QColor('#704214')) # button background color
    palette.setColor(QPalette.ButtonText, QColor('#ffefe0')) # button font color
    palette.setColor(QPalette.AlternateBase, QColor('#b8803c')) # table and dropdown background color
    palette.setColor(QPalette.ToolTipBase, QColor('#b8803c')) # tooltip background color
    palette.setColor(QPalette.ToolTipText, QColor('#ffefe0')) # tooltip font color
    palette.setColor(QPalette.BrightText, QColor('#ffefe0')) # highlighted font color
    
    # load the app
    app = QApplication([])
    app.setStyle(QStyleFactory.create('Fusion'))
    app.setPalette(palette)
    fantasy_name_generator = FantasyNameGenerator()
    fantasy_name_generator.setGeometry(100, 100, 800, 600)
    fantasy_name_generator.show()
    app.exec_()
