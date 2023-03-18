from rangen_words import rangen_word
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QStyleFactory, QAction, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QSlider, QLineEdit, QMessageBox, QCheckBox, QRadioButton, QButtonGroup, QFileDialog
from PyQt5.QtGui import QKeySequence, QFont, QFontMetrics, QPalette, QPixmap, QPainter, QColor, QPen
import os, json, csv

class RanGenFantasyNames(QMainWindow):
    # initialize the app and call some starting functions and universal hardcoded values
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RanGen Fantasy Names 3.2')
        self.max_syllables_range = 6    # change the selectable range of syllable generation options
        self.generate_names_range = 10  # change the number of names that are printed in the GUI
        self.slider_min = 1 # change the minimum value for the slider bar settings
        self.slider_max = 100   # change the maximum value for the slider bar settings
        self.name_font = QFont('Consolas', 12, QFont.Bold) # change how the names are displayed including copy as image
        self.init_ui()
        self.json_config()
        self.reset_values()
        self.generate_names()
        
    # function to handle json config file
    def json_config(self):
        # these are the default values for the app
        self.system_config = {
            "var_beg_cons_prob": 0.8,
            "var_beg_cluster_prob": 0.2,
            "var_vowel_prob": 0.75,
            "var_end_cons_prob": 0.6,
            "var_end_cluster_prob": 0.15,
            "var_name_splitter": True,
            "var_splitter_char": " ",
            "var_max_syllables": 4
        }
        # create config file if it doesn't exist with the system default values
        if not os.path.exists('config.json'):
            with open('config.json', 'w') as f:
                config = {'custom_config': self.system_config}
                json.dump(config, f)   
        # reset or repair the config file for various issues
        else:
            with open('config.json', 'r') as f:
                try:
                    config = json.load(f)
                    if 'custom_config' not in config:
                        print('Error: Custom settings are not present in the config file. It will be rebuilt to defaults.')
                        config = {'custom_config': self.system_config}
                    for key in self.system_config.keys():
                        if key not in config['custom_config']:
                            print(f'Error: Required setting {key} not found in the config file. Adding default value for the setting.')
                            config['custom_config'][key] = self.system_config[key]
                    for key in list(config['custom_config'].keys()):
                        if key not in self.system_config:
                            print(f'Error: Unneeded setting {key} found in the config file. It will be removed.')
                            del config['custom_config'][key]                               
                except json.JSONDecodeError:
                    print('Error: The config file is corrupt. It will be rebuilt to defaults.')
                    config = {'custom_config': self.system_config}
            with open('config.json', 'w') as f:
                json.dump(config, f)

    # function to reset the values to default and used for initialization
    def reset_values(self):
        # load user_config from json config to set defaults
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.var_beg_cons_prob = config['custom_config']['var_beg_cons_prob']
            self.var_beg_cluster_prob = config['custom_config']['var_beg_cluster_prob']
            self.var_vowel_prob = config['custom_config']['var_vowel_prob']
            self.var_end_cons_prob = config['custom_config']['var_end_cons_prob']
            self.var_end_cluster_prob = config['custom_config']['var_end_cluster_prob']
            self.var_name_splitter = config['custom_config']['var_name_splitter']
            self.var_splitter_char = config['custom_config']['var_splitter_char']
            self.var_max_syllables = config['custom_config']['var_max_syllables']
        # update the GUI to reflect the defaults
        self.beg_cons_slider.setValue(int(self.var_beg_cons_prob * 100))
        self.beg_cluster_slider.setValue(int(self.var_beg_cluster_prob * 100))
        self.vowel_slider.setValue(int(self.var_vowel_prob * 100))
        self.end_cons_slider.setValue(int(self.var_end_cons_prob * 100))
        self.end_cluster_slider.setValue(int(self.var_end_cluster_prob * 100))
        self.name_splitter_check_box.setChecked(self.var_name_splitter)
        if self.var_splitter_char == ' ':
            self.splitter_char_radio1.setChecked(True)
        elif self.var_splitter_char == '\'':
            self.splitter_char_radio2.setChecked(True)
        elif self.var_splitter_char == '-':
            self.splitter_char_radio3.setChecked(True)
        self.max_syllables_radio[str(self.var_max_syllables)].setChecked(True)

    # function to update the config file with the current values
    def save_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['custom_config']['var_beg_cons_prob'] = self.var_beg_cons_prob
        config['custom_config']['var_beg_cluster_prob'] = self.var_beg_cluster_prob
        config['custom_config']['var_vowel_prob'] = self.var_vowel_prob
        config['custom_config']['var_end_cons_prob'] = self.var_end_cons_prob
        config['custom_config']['var_end_cluster_prob'] = self.var_end_cluster_prob
        config['custom_config']['var_name_splitter'] = self.var_name_splitter
        config['custom_config']['var_splitter_char'] = self.var_splitter_char
        config['custom_config']['var_max_syllables'] = int(self.var_max_syllables)
        with open('config.json', 'w') as f:
            json.dump(config, f)
            
    # function to reset the config file to the hardcoded system defaults
    def reset_config(self):
        with open('config.json', 'w') as f:
            config = {'custom_config': self.system_config}
            json.dump(config, f)
        self.reset_values()

    # function to generate names for the name text boxes that are not selected with a corresponding check box id (being checked off 'saves' the name from re-rolling)
    def generate_names(self):
        for i in range(self.generate_names_range):
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
        checked_name_boxes = [self.name_text_box[f'{i+1}'].text() for i in range(self.generate_names_range) if self.name_check_box[f'{i+1}'].isChecked()]
        if not checked_name_boxes:  # check to do nothing if nothing is checked
            return
        text = '\n'.join(checked_name_boxes)
        QApplication.clipboard().setText(text)
        print(f'The following names were copied to your clipboard as text: \n{text}')
        
    # function to copy to clipboard as an image
    def copy_to_clipart(self):
        # checks if a name box has a corresponded check box checked
        checked_name_boxes = [self.name_text_box[f'{i+1}'].text() for i in range(self.generate_names_range) if self.name_check_box[f'{i+1}'].isChecked()]
        if not checked_name_boxes:
            return
        height = 20
        for name_text_box in checked_name_boxes:
            height += QFontMetrics(self.name_font).height()
        pixmap = QPixmap(220, height)
        pixmap.fill(QColor('#704214'))  # should match QPalette.Base as defined for the GUI
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor('#ffefe0'))   # should match QPalette.Text as defined for the GUI
        painter.setFont(self.name_font)
        painter.setPen(pen)
        # draw text for each checked line
        y = 20
        for name_text_box in checked_name_boxes:
            painter.drawText(5, y, name_text_box)
            y += QFontMetrics(self.name_font).height()
        painter.end()
        text = '\n'.join(checked_name_boxes)
        print(f'The following names were copied to your clipboard as an image: \n{text}')
        QApplication.clipboard().setPixmap(pixmap)
        
    # function to export names to a file
    def export_names(self):
        checked_name_boxes = [self.name_text_box[f'{i+1}'].text() for i in range(self.generate_names_range) if self.name_check_box[f'{i+1}'].isChecked()]
        if not checked_name_boxes:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, 'Export to CSV', 'RanGen Fantasy Names', 'CSV Files (*.csv)')
        if not file_path:
            return
        try:
            with open(file_path, 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for name in checked_name_boxes:
                    writer.writerow([name])
            text = '\n'.join(checked_name_boxes)
            print(f'The following names were exported to {file_path}: \n{text}')
            QMessageBox.information(self, 'Export', f'Selected names have been exported to "{file_path}"')
        except Exception as e:
            print(f'Error exporting names: {e}')
            QMessageBox.critical(self, 'Export Error', f'Error exporting names: {e}')

    # functions to toggle check boxes
    def select_all(self):
        for i in range(1, self.generate_names_range+1):
            self.name_check_box[f'{i}'].setChecked(True)
            
    def deselect_all(self):
        for i in range(1, self.generate_names_range+1):
            self.name_check_box[f'{i}'].setChecked(False)

    # function for about message box dialog
    def about_message(self):
        message_box = QMessageBox()
        message_box.setWindowTitle('About')
        message_box.setText(
            '<p>RanGen Fantasy Names procedurally generates names by joining up to four randomly generated syllables that are constructed following "consonant-vowel-consonant" conventions. If you would like to see more about the project, check out the <a href="https://github.com/Lanecrest/RanGen-Fantasy-Names">GitHub</a> page.</p>'
            '<p>Use the check boxes to select specific names you would like to work with. Selected names will also be ignored when rolling. You can copy selected names to your clipboard either as text or as an image. You can also export the selected names to a CSV file which will be appended after any existing entries.</p>'
            '<p>Use the settings at the bottom of the interface to adjust values. You can toggle whether long names will be split somewhere randomly and choose the symbol that splits them. You can also adjust the frequency of consonants, clusters, vowels, diphthongs, etc. These values will effect every syllable a name contains, which is another setting you can adjust to determine the maximum number of syllables a name can have.</p>'
            '<p>You can save your custom settings to a JSON file via the menu. Resetting the values will reset all of the values to your custom defaults. You can also reset the settings back the the system defaults via the menu. If you modify the JSON file directly, the entire file will be rebuilt if it contains any errors.</p>'
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
        # create a file menu
        menu_bar = self.menuBar()
        main_display = QWidget(self)    # assign all widgets outside the menu to a single value to be pulled as a central widget for the display
        
        file_menu = menu_bar.addMenu('File')
        self.generate_action = QAction('Generate Names', self)
        self.generate_action.triggered.connect(self.generate_names)
        self.generate_action.setShortcut('Ctrl+G')
        file_menu.addAction(self.generate_action)       
        
        file_menu.addSeparator()
        self.select_action = QAction('Select All', self)
        self.select_action.triggered.connect(self.select_all)
        self.select_action.setShortcut('Ctrl+A')
        file_menu.addAction(self.select_action)

        self.deselect_action = QAction('Deselect All', self)
        self.deselect_action.triggered.connect(self.deselect_all)
        self.deselect_action.setShortcut('Ctrl+Alt+A')
        file_menu.addAction(self.deselect_action)
        
        file_menu.addSeparator()
        self.about_action = QAction('About', self)
        self.about_action.setShortcut('Ctrl+H')
        self.about_action.triggered.connect(self.about_message)
        file_menu.addAction(self.about_action)      
        
        file_menu.addSeparator()
        self.quit_action = QAction('Quit', self)
        self.quit_action.triggered.connect(QApplication.instance().quit)
        self.quit_action.setShortcut('Ctrl+Q')
        file_menu.addAction(self.quit_action)
        
        settings_menu = menu_bar.addMenu('Settings')
        self.values_action = QAction('Reset Values', self)
        self.values_action.triggered.connect(self.reset_values)
        self.values_action.setShortcut('Ctrl+R')
        settings_menu.addAction(self.values_action)
        
        settings_menu.addSeparator()
        self.save_action = QAction('Save Config', self)
        self.save_action.triggered.connect(self.save_config)
        self.save_action.setShortcut('Ctrl+S')
        settings_menu.addAction(self.save_action)
        
        self.reset_action = QAction('Reset Config', self)
        self.reset_action.triggered.connect(self.reset_config)
        self.reset_action.setShortcut('Ctrl+Alt+R')
        settings_menu.addAction(self.reset_action)
        
        export_menu = menu_bar.addMenu('Export')
        self.clipboard_action = QAction('Copy as Text', self)
        self.clipboard_action.triggered.connect(self.copy_to_clipboard)
        self.clipboard_action.setShortcut('Ctrl+C')
        export_menu.addAction(self.clipboard_action)

        self.clipart_action = QAction('Copy as Image', self)
        self.clipart_action.triggered.connect(self.copy_to_clipart)
        self.clipart_action.setShortcut('Ctrl+E')
        export_menu.addAction(self.clipart_action)
        
        export_menu.addSeparator()
        self.export_action = QAction('Export to CSV', self)
        self.export_action.triggered.connect(self.export_names)
        self.export_action.setShortcut('Ctrl+P')
        export_menu.addAction(self.export_action)       
        
        # create buttons for app menus
        self.generate_button = QPushButton('Roll')
        self.generate_button.setToolTip('Generate names for unchecked fields')
        self.generate_button.clicked.connect(self.generate_names) 
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_button)
 
        # create a grid for the name check and text boxes and style settings
        check_text_layout = QGridLayout()
        self.name_text_box = {}
        self.name_check_box = {}
        # create check and text boxes for the number of names that can be generated at a time and place them in the grid
        for i in range(self.generate_names_range):
            box_id = f'{i+1}'          
            self.name_check_box[box_id] = QCheckBox()
            self.name_check_box[box_id].setChecked(False)
            check_text_layout.addWidget(self.name_check_box[box_id], i, 0)
            
            self.name_text_box[box_id] = QLineEdit()
            self.name_text_box[box_id].setFont(self.name_font)
            self.name_text_box[box_id].setReadOnly(True)
            check_text_layout.addWidget(self.name_text_box[box_id],i, 1)
            
        # create user variable setting inputs for the GUI
        settings_font = QFont()
        settings_font.setPointSize(7)   # affects font size used for settings text across the board

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
        self.beg_cons_slider.setMinimum(self.slider_min)
        self.beg_cons_slider.setMaximum(self.slider_max)
        self.beg_cons_slider.valueChanged.connect(self.set_var_beg_cons_prob)

        self.beg_cluster_label = QLabel('Beginning Cluster more likely than Nothing: ')
        self.beg_cluster_label.setFont(settings_font)
        self.beg_cluster_slider = QSlider(Qt.Horizontal)
        self.beg_cluster_slider.setMinimum(self.slider_min)
        self.beg_cluster_slider.setMaximum(self.slider_max)
        self.beg_cluster_slider.valueChanged.connect(self.set_var_beg_cluster_prob)

        self.vowel_label = QLabel('Vowel more likely than Diphthong: ')
        self.vowel_label.setFont(settings_font)
        self.vowel_slider = QSlider(Qt.Horizontal)
        self.vowel_slider.setMinimum(self.slider_min)
        self.vowel_slider.setMaximum(self.slider_max)
        self.vowel_slider.valueChanged.connect(self.set_var_vowel_prob)

        self.end_cons_label = QLabel('Ending Consonant more likely than Cluster/Nothing: ')
        self.end_cons_label.setFont(settings_font)
        self.end_cons_slider = QSlider(Qt.Horizontal)
        self.end_cons_slider.setMinimum(self.slider_min)
        self.end_cons_slider.setMaximum(self.slider_max)
        self.end_cons_slider.valueChanged.connect(self.set_var_end_cons_prob)

        self.end_cluster_label = QLabel('Ending Cluster more likely than Nothing: ')
        self.end_cluster_label.setFont(settings_font)
        self.end_cluster_slider = QSlider(Qt.Horizontal)
        self.end_cluster_slider.setMinimum(self.slider_min)
        self.end_cluster_slider.setMaximum(self.slider_max)
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
        
        # finalize the main display as a vertical box and place it as the central widget under the file menu
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(check_text_layout)
        main_layout.addLayout(user_settings_syllables)
        main_layout.addLayout(user_settings_splitter)
        main_layout.addLayout(user_settings_probs)
        main_display.setLayout(main_layout)
        self.setCentralWidget(main_display)
        
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
    main_window = RanGenFantasyNames()
    main_window.show()
    frame = main_window.frameGeometry()
    frame.moveCenter(QDesktopWidget().availableGeometry().center())
    main_window.move(frame.topLeft())
    app.exec_()