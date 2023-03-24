# RanGen-Fantasy-Names

RanGen Fantasy Names is a Python application that procedurally generates names by joining a number of randomly generated syllables that are constructed following 'consonant-vowel-consonant' conventions.

[Change Log](CHANGELOG.md)
=

About
=
This application works by running a function to generate a syllable that is created using consonant-vowel-consonant conventions. It may randomly omit the starting or ending consonant, and can generate a cluster of consonants such as "ck" or "th" intead of a single consonant, or it can generate a diphthong such as "ie" or "oo" instead of a single vowel. It will then string together a number of these syllables to form the generated name.

While using the GUI, the check boxes are used to select specific names you would like to work with. Selected names will also be ignored when re-rolling. Currently, you can copy selected names to your clipboard either as text or as an image. You can also export the selected names to a CSV file which will be appended after any existing entries. Many of the settings can be set by the user via inputs and saved to a config file. The 'About' menu in the application will give more information.

Screenshots
=
[Screenshots](/screenshots)

![Alt text](/screenshots/v4-0-0_main.png?raw=true "Main Window")
![Alt text](/screenshots/v4-0-0_settings.png?raw=true "Settings Window")

Requirements
=
[requirements.txt](requirements.txt)

JSON Config
=
The config is a JSON file and will save custom settings. The program will automatically generate this file with the system defaults as the custom settings if the file doesn't exist. You can save current settings in the program which will update the config file, so those settings will be reloaded the next time you run the program. If the file is ever corrupted, it will either rebuild the entire file with default settings, or parts of the file with default settings depending on what kind of errors arise.

JSON Charset
=
The pre-packaged [charset file](rangen_charsets.json) is just an example of how you can define your own character sets. The program will always be able to use a default character set if you don't have a charset file or the charset file is corrupted. Any custom character sets will need to contain each of the 5 dictionaries (vowels, diphthongs, consonants, beginning_clusters, and ending_clusters) to work correctly but the names (such as Sample) in the pre-packaged file can be whatever you choose, as well as the letters inside each dictionary.

CSV File
=
One of the current options is to export your names to a CSV file. In the short term, this is just so you can maintain a list of names you like as the names are appended to the file so it keeps track of all names you have exported in the past. In the long term the app may do more with this file as more features are added.

Road Map
=
The next update will likely provide the ability to work with the new settings window and the main window simultaneously and contain additional character sets in the charset json file. In a future update beyond that, the ability to create character set files through the GUI versus manipulating the json file directly might be implemented.

Credits
=
Programmed by Lanecrest Tech
