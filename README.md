# easyKey
easier translation of .json keyvalue pair files





easyKey is a simple program, that i just slapped together to help me in translation of key value pairs for .json files.

Right now it only accepts .json files but if there is demand for other syntaxes those can be implemented quite simply.


Feel free to use it under the license but be warned, there are still some bugs so if you have any fixes please send a commit or message and i will take a look.

Its all written in python so should be easy to compile and run on any os. 







# Shortcuts and info.


F1 - load from current directory (this works best as an executable file).
F5 - reload files.
F12 - toggle overwrite, see status. 

Ctrl+s - save files (will overwrite files if enabled)




I would recommend to use this with git otherwise it might be hard to identify issues if they appear.




# Run or make executable

If you just want to run it as its own executable compile with pyinstaller and move the executable into the folder where the translation en.json files are. 

Use pyinstaller or something like it to make an executable.

to install pyinstaller you must have a version of python 3 and pip installed.

To install any missing dependables use pip.

example:

pip3 install pyinstaller


To use pyinstaller from the directory of the files, open a terminal and run:

pyinstaller --onefile easyKeyProgram.py




