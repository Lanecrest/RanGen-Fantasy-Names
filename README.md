# RanGen-Fantasy-Names

RanGen Fantasy Names is a Python application that procedurally generates names by joining up to four randomly generated syllables that are constructed following 'consonant-vowel-consonant' conventions. It requires the PyQt module.

Version History
===

v2.3
---
-Removed possibility for a letter to repeat itself more than twice in a row (maybe)

-Chananged split names to have an apostrophe instead of a space.

-Updated pixmap spacing when copy as image

-Updated gui to better align widgets

v2.25
---
-Added an export function. This will export selected names to a .csv file and will append names if names already exist

-Fixed some typos and updated the About box

-Made four syllable names slightly less frequent

-There is now just one re-roll button and it ignores selected names. This is explained in the About box


v2.2
---
-Overhaul to the GUI layout

-Changed the name of the program and project

-Names now generate in their own text boxes and have corresponding check boxes to select them

-Can multi select names to copy to clipboard as either text or an image

-Can re-reroll names based on what is selected

-Added an 'About' dialog box and link to github project

v2.1
---
-Minor tweaks to the GUI

-Changed some of the values for syllable generation

-Added a few more diphthongs

v2.0
---
-Adjusted many of the conditions for generating syllables

-Now runs in PyQt5

-Can copy text out of the text box or copy as image for easy sharing

v1.0
---
-Initial release, runs in console

---
Credits
===
Programmed by Lanecrest Tech. Uses PyQt for GUI
