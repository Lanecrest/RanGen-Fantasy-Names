# Change Log

v3.11
-
-Fixed a bug with slider values that caused the program to crash

-A couple of minor tweaks to presentation

v3.1
-
-Added ability to choose the maximum number of syllables that can generate for each name (updated rangen_words to support this as a feature of the core module).

-Fixed some references in code to other parts of code including commits that was missed in the 3.0 update

-Changed the ui a bit to account for the more user settings options

v3.0
-
-Split the syllable/name generation functions into their own module. "rangen_words" is now its own script and contains the functions for word generation. this can allow it to be easily imported into other projects. rangen_fantasy_names is now just the GUI front end that uses rangen_words to make 'fantasy names.'

-Added ability for users to adjust many of the settings

-Removed some code in the name generation (rangen_words) that turned out to not be very useful

-Optimized some code and behaviors over all


v2.3
-
-Removed possibility for a letter to repeat itself more than twice in a row (maybe)

-Chananged split names to have an apostrophe instead of a space.

-Updated pixmap spacing when copy as image

-Updated gui to better align widgets

v2.25
-
-Added an export function. This will export selected names to a .csv file and will append names if names already exist

-Fixed some typos and updated the About box

-Made four syllable names slightly less frequent

-There is now just one re-roll button and it ignores selected names. This is explained in the About box


v2.2
-
-Overhaul to the GUI layout

-Changed the name of the program and project

-Names now generate in their own text boxes and have corresponding check boxes to select them

-Can multi select names to copy to clipboard as either text or an image

-Can re-reroll names based on what is selected

-Added an 'About' dialog box and link to github project

v2.1
-
-Minor tweaks to the GUI

-Changed some of the values for syllable generation

-Added a few more diphthongs

v2.0
-
-Adjusted many of the conditions for generating syllables

-Now runs in PyQt5

-Can copy text out of the text box or copy as image for easy sharing

v1.0
-
-Initial release, runs in console
