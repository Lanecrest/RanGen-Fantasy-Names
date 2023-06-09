# RanGen Fantasy Names
RanGen Fantasy Names is a Python application that procedurally generates names by joining a number of randomly generated syllables that are constructed following 'consonant-vowel-consonant' conventions. It uses a custom module (rangen_words) as the back-end for name generation, and a GUI front-end using PyQt5.

# About
This application works by running a function to generate a syllable that is created using consonant-vowel-consonant conventions. It may randomly omit the starting or ending consonant, and can generate a cluster of consonants such as "ck" or "th" intead of a single consonant, or it can generate a diphthong such as "ie" or "oo" instead of a single vowel. It will then string together a number of these syllables to form the generated name.

While using the GUI, the check boxes are used to select specific names you would like to work with. Selected names will also be ignored when re-rolling. Currently, you can copy selected names to your clipboard either as text or as an image. You can also export the selected names to a CSV file which will be appended after any existing entries. Many of the settings can be set by the user via inputs and saved to a config file. The 'About' menu in the application will give more information.

# Screenshots
[Screenshots](/screenshots)

![Alt text](/screenshots/v1-0-0_main.png?raw=true "Main Window")
![Alt text](/screenshots/v1-0-0_charsets.png?raw=true "Charset Window")

# Change Log
[Change Log](CHANGELOG.md)

# Requirements
[Requirements](requirements.txt)

# Other Files
JSON Config
-
The config is a JSON file and will save custom settings. The program will only generate this file if you ever choose to save your settings. You can save current settings in the program which will update the config file and will be the new settings that the program will reset to unless you choose to reset the config file back to system defaults. If the file is ever corrupted, it will always be able to use the default settings.

JSON Charset
-
The pre-packaged [charset file](/rangen/charsets.json) is just an example of how you can define your own character sets. The program will always be able to use a default character set if you don't have a charset file or the charset file is corrupted. Any custom character sets will need to contain each of the 5 dictionaries (vowels, diphthongs, consonants, beginning_clusters, and ending_clusters) to work correctly but the names (such as 'Orc') in the pre-packaged file can be whatever you choose, as well as the letters inside each dictionary.

CSV File
-
One of the current options is to export your names to a CSV file. In the short term, this is just so you can maintain a list of names you like as the names are appended to the file so it keeps track of all names you have exported in the past. In the long term, the program may do more with this file as more features are added.

# Road Map
The basic intended functions of the program have all been implemented. The next feature likely to be implemented will be the ability to create or modify character sets directly in the GUI and perhaps the ability to view exported names in the CSV file directly within the GUI.

# Credits
Lanecrest Tech © 2023

This program uses Qt Framework Essentials, specifically the PyQt5 binder from [Riverbank Computing](https://www.riverbankcomputing.com/)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
