#Lazy Time Tracker
Sublime Text Time Tracker for the lazy in us all

## How it works

This time tracker is based off saving a file in a project. I am not going to explain Sublime projects. If you set up the Sublime project settings correctly, described below, everytime you save a file in that project the tracker will "log it". The tracker will keep adding up the time until three things happen. 1) You save a file outside this open project. 2) You close the project with `super+ctrl+w`. 3) You quit Sublime. 

#### Set up
First you will need to set up the settings of the plug in settings. The only one you really need to worry about to start with is the `"log_folder"` setting. This is the folder you want to save the log file into. Pick a spot and it will appear there. And make sure it is the full path and ends with a ` / `. The other settings are described below. What happens if you don't change this setting. It will add a folder to your home directory and put the file in there. 

You will need to set up at least one item in all your projects' `.sublime-project` file. In the settings section of the project file you can add the item `"ProjectTitle"`. The Project Title is the name you want to save the time under. The tracker also lumps all saved actions under the project name so if you want to keep track accross saves of multiple files it does that. What happens if you don't set up the Project Title. It will log all your files seperately and everytime you save a different file it will add a line to the log.

