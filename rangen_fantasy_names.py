from rangen_words import rangen_word
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QStyleFactory, QAction, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QSlider, QLineEdit, QMessageBox, QSpinBox, QCheckBox, QComboBox, QButtonGroup, QRadioButton, QFileDialog, QDialog, QDialogButtonBox
from PyQt5.QtGui import QFont, QFontMetrics, QPalette, QPixmap, QPainter, QColor, QPen
import os, json, csv

class RanGenFantasyNames(QMainWindow):
    # function to initialize the app and define some universal hardcoded values for the GUI and run some startup functions
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RanGen Fantasy Names 4.0.0')
        self.generate_names_range = 10  # change the number of names that are printed at a time
        self.max_syllables_min = 1 # change the minimum value for the syllable spin box
        self.max_syllables_max = 6 # change the maxmimum value for the syllable spin box
        self.name_long_min = 4 # change the minimum value for the name length spin box
        self.name_long_max = 12 # change the maxmimum value for the name length spin box
        self.prob_slider_min = 0 # change the minimum value for the probability slider bars
        self.prob_slider_max = 100   # change the maximum value for the probability slider bars
        self.name_font = QFont('Consolas', 12, QFont.Bold) # change how the names are displayed including for copy as image
        self.config_file = 'config.json'
        self.charset_file = 'rangen_charsets.json'
        self.json_config()
        self.draw_gui()
        self.reset_values()
        self.generate_names()
       
    # function to handle json config file
    def json_config(self):
        # these are the default values for the program
        self.system_config = {
            'var_char_set': None,
            'var_beg_cons_prob': 0.8,
            'var_beg_cluster_prob': 0.2,
            'var_vowel_prob': 0.75,
            'var_end_cons_prob': 0.6,
            'var_end_cluster_prob': 0.15,
            'var_max_syllables': 4,
            'var_name_split': True,
            'var_split_char': " ",
            'var_name_long': 10            
        }
        # reset or repair the config file for various issues if it exists
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                try:
                    config = json.load(f)
                    if 'custom_config' not in config:
                        print('Error: Settings do not seem to be present in the config file. It will be rebuilt to defaults.')
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
            with open(self.config_file, 'w') as f:
                json.dump(config, f)

    # function to reset the values to system defaults or custom defaults if a config is present
    def reset_values(self):
        if not os.path.exists(self.config_file):
            for key in self.system_config:
                value = self.system_config[key]
                setattr(self, key, value)
        else:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                for key in config['custom_config']:
                    value = config['custom_config'][key]
                    setattr(self, key, value)

        
    # function to update the config file with the current values
    def save_config(self):
        # create and write the config file if it doesn't exist
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                config = {'custom_config': self.system_config}
                for key in config['custom_config']:
                    config['custom_config'][key] = getattr(self, key)             
        else:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            for key in config['custom_config']:
                config['custom_config'][key] = getattr(self, key)
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
            
    # function to reset the config file to the hardcoded system defaults
    def reset_config(self):
        if not os.path.exists(self.config_file):
            for key in self.system_config:
                value = self.system_config[key]
                setattr(self, key, value)
        else:
            with open(self.config_file, 'w') as f:
                config = {'custom_config': self.system_config}
                json.dump(config, f)
        self.reset_values()

    # function to generate names for the name text boxes that are not selected with a corresponding check box id (being checked off 'saves' the name from re-rolling)
    def generate_names(self):
        for i in range(self.generate_names_range):
            box_id = f'{i+1}'
            if not self.name_check_box[box_id].isChecked():
                name = rangen_word(
                    load_set=self.var_char_set,
                    beg_cons_prob=self.var_beg_cons_prob,
                    beg_cluster_prob=self.var_beg_cluster_prob,
                    vowel_prob=self.var_vowel_prob,
                    end_cons_prob=self.var_end_cons_prob,
                    end_cluster_prob=self.var_end_cluster_prob,
                    max_syllables=self.var_max_syllables,
                    split_char=self.var_split_char,
                    word_split=self.var_name_split,
                    word_long=self.var_name_long
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
            QMessageBox.critical(self, 'Export', f'Error exporting names: {e}')

    # functions to toggle check boxes
    def select_all(self):
        for i in range(1, self.generate_names_range+1):
            self.name_check_box[f'{i}'].setChecked(True)
            
    def deselect_all(self):
        for i in range(1, self.generate_names_range+1):
            self.name_check_box[f'{i}'].setChecked(False)

    # function for about message box
    def about_message(self):
        about_box = QMessageBox()
        about_box.setWindowTitle('About')
        about_box.setText(
            '<p>RanGen Fantasy Names procedurally generates names by joining together randomly generated syllables that are constructed following "consonant-vowel-consonant" conventions. If you would like to see more about the project, check out the <a href="https://github.com/Lanecrest/RanGen-Fantasy-Names">GitHub</a> page.</p>'
            '<p>The main display consists of randomly generated names based on the current settings. You can select names with the corresponding check box to prevent them from being re-rolled and you can also copy the selected names to your clipboard or export them to a CSV file.</p>'
            '<p>In the settings panel, you can adjust several settings dynamically. You can save the settings at any time which will export them to a JSON file and become your new defaults. Resetting the config will revert your custom defaults to the original program defaults. Resetting values will reset to the current default values (either your custom or the program).</p>'
            '<p>You can also choose and view the current character set in the settings panel. If you do not have a JSON file of custom character sets, the only character set option available will be the default.</p>'
            '<p align="center">RanGen Fantasy Names ©2023 <a href="https://www.lanecrest.com/">Lanecrest Tech</a></p>'
            )
        about_box.setStandardButtons(QMessageBox.Ok)
        about_box.exec_()
    
    # function to display the character set in a message box
    def view_charset(self):
        charset_box = QMessageBox()
        if self.var_char_set  == None:
            charset_title = 'Default'
        else:
            charset_title = self.var_char_set
        charset_box.setWindowTitle(f'{charset_title} Character Set')
        from rangen_words import load_charset
        char_dict = load_charset(load_set=self.var_char_set).__dict__
        char_text = ''
        for key, value in char_dict.items():
            char_text += f'{key}: {value}\n\n'
        charset_box.setText(char_text)
        charset_box.setStandardButtons(QMessageBox.Ok)
        charset_box.exec_()
        
    # function to load the settings dialog box
    def settings_dialog(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle('Settings')
        settings_button_box = QDialogButtonBox(QDialogButtonBox.Close)
        settings_button_box.rejected.connect(settings_dialog.reject)

        # combo box to select the character set
        user_settings_charset = QHBoxLayout()
        self.char_set_label = QLabel('Use character set: ')
        self.char_set_combo_box = QComboBox()
        self.char_set_combo_box.addItem("Default")
        if os.path.exists(self.charset_file):
            with open(self.charset_file, 'r') as f:
                char_sets = json.load(f)
            for key in char_sets.keys():
                self.char_set_combo_box.addItem(key)
        self.char_set_combo_box.currentIndexChanged.connect(self.set_var_char_set)
        self.charset_button = QPushButton('View Character Set')
        self.charset_button.setToolTip('View the selected character set')
        self.charset_button.clicked.connect(self.view_charset)   
        user_settings_charset.addWidget(self.char_set_label)
        user_settings_charset.addWidget(self.char_set_combo_box)
        user_settings_charset.addWidget(self.charset_button)

        # slider to choose the maximum number of syllables that can generate
        user_settings_syllables = QHBoxLayout()
        self.max_syllables_label = QLabel(f'Maximum syllables to generate: 1')      
        self.max_syllables_slider = QSlider(Qt.Horizontal)
        self.max_syllables_slider.setMinimum(self.max_syllables_min)
        self.max_syllables_slider.setMaximum(self.max_syllables_max)
        self.max_syllables_slider.valueChanged.connect(self.set_var_max_syllables)
        user_settings_syllables.addWidget(self.max_syllables_label)
        user_settings_syllables.addWidget(self.max_syllables_slider)       

        # check box to determine if a name can be split and radio buttons to choose the character to use as the split
        user_settings_split = QHBoxLayout()
        self.name_split_check_box = QCheckBox('Split long names with: ', self)
        self.name_split_check_box.setChecked(True)
        self.name_split_check_box.stateChanged.connect(self.set_var_name_split)             
        # the radio buttons
        self.split_char_radio_group = QButtonGroup()
        self.split_char_radio1 = QRadioButton('Space')
        self.split_char_radio_group.addButton(self.split_char_radio1)
        self.split_char_radio2 = QRadioButton('Apostrophe')
        self.split_char_radio_group.addButton(self.split_char_radio2)
        self.split_char_radio3 = QRadioButton('Dash')
        self.split_char_radio_group.addButton(self.split_char_radio3)
        self.split_char_radio_group.buttonClicked.connect(self.set_var_split_char)
        user_settings_split.addWidget(self.name_split_check_box) 
        user_settings_split.addWidget(self.split_char_radio1)
        user_settings_split.addWidget(self.split_char_radio2)
        user_settings_split.addWidget(self.split_char_radio3)
        
        # spin box to choose how long a name should be before it can split
        user_settings_long = QHBoxLayout()
        self.name_long_label = QLabel(f'Only split if the name has at least this many letters: {self.name_long_min} - {self.name_long_max}')
        self.name_long_spin_box = QSpinBox()
        self.name_long_spin_box.setFixedWidth(75)
        self.name_long_spin_box.setMinimum(self.name_long_min)
        self.name_long_spin_box.setMaximum(self.name_long_max)
        self.name_long_spin_box.valueChanged.connect(self.set_var_name_long)
        user_settings_long.addWidget(self.name_long_label)
        user_settings_long.addWidget(self.name_long_spin_box)

        # sliders for the syllable generation values. labels are dynamically updated via the connect function calls
        user_settings_probs = QVBoxLayout()

        self.beg_cons_slider = QSlider(Qt.Horizontal)
        self.beg_cons_label = QLabel(f'Beginning Consonant more likely than Cluster/Nothing: 0%')
        self.beg_cons_slider.setMinimum(self.prob_slider_min)
        self.beg_cons_slider.setMaximum(self.prob_slider_max)
        self.beg_cons_slider.valueChanged.connect(self.set_var_beg_cons_prob)

        self.beg_cluster_slider = QSlider(Qt.Horizontal)
        self.beg_cluster_label = QLabel(f'Beginning Cluster more likely than Nothing: 0%')
        self.beg_cluster_slider.setMinimum(self.prob_slider_min)
        self.beg_cluster_slider.setMaximum(self.prob_slider_max)
        self.beg_cluster_slider.valueChanged.connect(self.set_var_beg_cluster_prob)

        self.vowel_slider = QSlider(Qt.Horizontal)
        self.vowel_label = QLabel(f'Vowel more likely than Diphthong: 0%')
        self.vowel_slider.setMinimum(self.prob_slider_min)
        self.vowel_slider.setMaximum(self.prob_slider_max)
        self.vowel_slider.valueChanged.connect(self.set_var_vowel_prob)

        self.end_cons_slider = QSlider(Qt.Horizontal)
        self.end_cons_label = QLabel(f'Ending Consonant more likely than Cluster/Nothing: 0%')
        self.end_cons_slider.setMinimum(self.prob_slider_min)
        self.end_cons_slider.setMaximum(self.prob_slider_max)
        self.end_cons_slider.valueChanged.connect(self.set_var_end_cons_prob)

        self.end_cluster_slider = QSlider(Qt.Horizontal)
        self.end_cluster_label = QLabel(f'Ending Cluster more likely than Nothing: 0%')
        self.end_cluster_slider.setMinimum(self.prob_slider_min)
        self.end_cluster_slider.setMaximum(self.prob_slider_max)
        self.end_cluster_slider.valueChanged.connect(self.set_var_end_cluster_prob)

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
        user_settings_probs.addWidget(settings_button_box)
       
        # update the GUI to reflect the default settings
        if self.var_char_set == None:
            self.char_set_combo_box.setCurrentIndex(self.char_set_combo_box.findText('Default'))
        else:
            self.char_set_combo_box.setCurrentIndex(self.char_set_combo_box.findText(self.var_char_set))
        self.max_syllables_slider.setValue(self.var_max_syllables)
        self.beg_cons_slider.setValue(int(self.var_beg_cons_prob * 100))
        self.beg_cluster_slider.setValue(int(self.var_beg_cluster_prob * 100))
        self.vowel_slider.setValue(int(self.var_vowel_prob * 100))
        self.end_cons_slider.setValue(int(self.var_end_cons_prob * 100))
        self.end_cluster_slider.setValue(int(self.var_end_cluster_prob * 100))
        self.name_split_check_box.setChecked(self.var_name_split)
        if self.var_split_char == ' ':
            self.split_char_radio1.setChecked(True)
        elif self.var_split_char == '\'':
            self.split_char_radio2.setChecked(True)
        elif self.var_split_char == '-':
            self.split_char_radio3.setChecked(True)
        self.name_long_spin_box.setValue(self.var_name_long)
        
        # set the settings dialog layout
        settings_layout = QVBoxLayout()        
        settings_layout.addLayout(user_settings_charset)
        settings_layout.addLayout(user_settings_syllables)
        settings_layout.addLayout(user_settings_split)
        settings_layout.addLayout(user_settings_long)
        settings_layout.addLayout(user_settings_probs)
        settings_dialog.setLayout(settings_layout) 
        settings_dialog.exec()

    # function to determine the character set to use
    def set_var_char_set(self, index):
        if index == 0:
            self.var_char_set = None
        else:
            self.var_char_set = self.char_set_combo_box.currentText()
     
    # function to determine the maximum number of syllables a word can generate with
    def set_var_max_syllables(self, value):
        self.var_max_syllables = value
        current_label = self.max_syllables_label.text()
        new_label = f'{current_label.split(":")[0]}: {value}'
        self.max_syllables_label.setText(new_label)
     
    # function to toggle whether long names will have a split in them
    def set_var_name_split(self, state):
        self.var_name_split = state == Qt.Checked
        
    # function to set what character splits the names
    def set_var_split_char(self, button):
        if button == self.split_char_radio1:
            self.var_split_char = ' '
        elif button == self.split_char_radio2:
            self.var_split_char = '\''
        elif button == self.split_char_radio3:
            self.var_split_char = '-'
            
    # function to determine the how long a name should be before it would be split
    def set_var_name_long(self, value):
        self.var_name_long = value
            
    # functions to set the syllable generation values
    def set_var_beg_cons_prob(self, value):
        self.var_beg_cons_prob = value / 100
        current_label = self.beg_cons_label.text()
        new_label = f'{current_label.split(":")[0]}: {value}%'
        self.beg_cons_label.setText(new_label)

    def set_var_beg_cluster_prob(self, value):
        self.var_beg_cluster_prob = value / 100
        current_label = self.beg_cluster_label.text()
        new_label = f'{current_label.split(":")[0]}: {value}%'
        self.beg_cluster_label.setText(new_label)

    def set_var_vowel_prob(self, value):
        self.var_vowel_prob = value / 100
        current_label = self.vowel_label.text()
        new_label = f'{current_label.split(":")[0]}: {value}%'
        self.vowel_label.setText(new_label)

    def set_var_end_cons_prob(self, value):
        self.var_end_cons_prob = value / 100
        current_label = self.end_cons_label.text()
        new_label = f'{current_label.split(":")[0]}: {value}%'
        self.end_cons_label.setText(new_label)

    def set_var_end_cluster_prob(self, value):
        self.var_end_cluster_prob = value / 100
        current_label = self.end_cluster_label.text()
        new_label = f'{current_label.split(":")[0]}: {value}%'
        self.end_cluster_label.setText(new_label)

    # function to define the main window with file menu
    def draw_gui(self):
        # create a file menu
        menu_bar = self.menuBar()
        menu_bar_style = """
            QMenuBar {
                background-color: #ffefe0;
                color: #000000;
            }    
            QMenuBar::item:selected {
                background-color: #d5a05a;
                color: #ffefe0;
            }
            QMenuBar::item:hover {
                background-color: #d5a05a;
                color: #ffefe0;
            }
        """    
        menu_bar.setStyleSheet(menu_bar_style)
        
        # file menu options
        file_menu = menu_bar.addMenu('File')
        self.generate_action = QAction('Generate Names', self)
        self.generate_action.triggered.connect(self.generate_names)
        file_menu.addAction(self.generate_action)       
        
        file_menu.addSeparator()
        self.select_action = QAction('Select All', self)
        self.select_action.triggered.connect(self.select_all)
        self.select_action.setShortcut('Ctrl+A')
        file_menu.addAction(self.select_action)

        self.deselect_action = QAction('Deselect All', self)
        self.deselect_action.triggered.connect(self.deselect_all)
        self.deselect_action.setShortcut('Ctrl+Shift+A')
        file_menu.addAction(self.deselect_action)
        
        file_menu.addSeparator()
        self.about_action = QAction('About', self)
        self.about_action.setShortcut('F1')
        self.about_action.triggered.connect(self.about_message)
        file_menu.addAction(self.about_action)      
        
        file_menu.addSeparator()
        self.quit_action = QAction('Quit', self)
        self.quit_action.triggered.connect(QApplication.instance().quit)
        self.quit_action.setShortcut('Alt+F4')
        file_menu.addAction(self.quit_action)
        
        # settings menu options
        settings_menu = menu_bar.addMenu('Settings')
        self.settings_action = QAction('Open Settings', self)
        self.settings_action.triggered.connect(self.settings_dialog)
        self.settings_action.setShortcut('Ctrl+O')
        settings_menu.addAction(self.settings_action)
        
        settings_menu.addSeparator()
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
        self.reset_action.setShortcut('Ctrl+Shift+R')
        settings_menu.addAction(self.reset_action)
        
        # export menu options
        export_menu = menu_bar.addMenu('Export')
        self.clipboard_action = QAction('Copy as Text', self)
        self.clipboard_action.triggered.connect(self.copy_to_clipboard)
        self.clipboard_action.setShortcut('Ctrl+C')
        export_menu.addAction(self.clipboard_action)

        self.clipart_action = QAction('Copy as Image', self)
        self.clipart_action.triggered.connect(self.copy_to_clipart)
        self.clipart_action.setShortcut('Ctrl+Shift+C')
        export_menu.addAction(self.clipart_action)
        
        export_menu.addSeparator()
        self.export_action = QAction('Export to CSV', self)
        self.export_action.triggered.connect(self.export_names)
        self.export_action.setShortcut('Ctrl+P')
        export_menu.addAction(self.export_action)       
        
        # create widgets for the main display
        main_display = QWidget(self)
        
        # button to roll names (there is also a file menu option but buttons are satisfying)
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton('Roll')
        self.generate_button.setToolTip('Generate names for unchecked fields')
        self.generate_button.clicked.connect(self.generate_names)         
        button_layout.addWidget(self.generate_button)
 
        # create a grid for the name check and text boxes and style settings for main output display
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
            self.name_text_box[box_id].setMinimumWidth(325)
            check_text_layout.addWidget(self.name_text_box[box_id],i, 1)
      
        # finalize the main display as a vertical box and place it as the central widget under the file menu
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(check_text_layout)
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
    rangen_class = RanGenFantasyNames()
    rangen_class.show()
    frame = rangen_class.frameGeometry()
    frame.moveCenter(QDesktopWidget().availableGeometry().center())
    rangen_class.move(frame.topLeft())
    app.exec_()