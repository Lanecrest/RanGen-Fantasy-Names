# RanGen-Fantasy-Names

RanGen Fantasy Names is a Python application that procedurally generates names by joining a number of randomly generated syllables that are constructed following 'consonant-vowel-consonant' conventions.

[Change Log](CHANGELOG.md)
=

About
=
This application works by running a function to generate a syllable that is created using consonant-vowel-consonant conventions. It may randomly omit the starting or ending consonant, and can generate a cluster of consonants such as "ck" or "th" intead of a single consonant, or it can generate a diphthong such as "ie" or "oo" instead of a single vowel. It will then string together a number of these syllables to form the generated name.

While using the GUI, the check boxes are used to select specific names you would like to work with. Selected names will also be ignored when re-rolling. Currently, you can copy selected names to your clipboard either as text or as an image. You can also export the selected names to a CSV file which will be appended after any existing entries. Many of the settings can be set by the user via inputs. The 'About' menu in the application will give more context.

Screenshots
=
[Screenshots](/screenshots)

![Alt text](/screenshots/v3_11_main.png?raw=true "Main Window")

Requirements
=
[requirements.txt](requirements.txt)

JSON Config
=

CSV File
=
One of the current options is to export your names to a CSV file. In the short term, this is just so you can maintain a list of names you like as the names are appended to the file so it keeps track of all names you have exported in the past. In the long term the app may do more with this file as more features are added.

Road Map
=
rangen_words will be updated in the long term to allow things in the future like more character support or being able to tweak the letters themselves. In an eventual move to Qt6, the project may switch to pyside instead of pyqt, depending on what the landscape looks like at that time. As more user defined settings are added, these will likely be moved into their own menu and the ability to export custom settings.

Credits
=
Programmed by Lanecrest Tech
