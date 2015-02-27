#Lazy Time Tracker
Sublime Text Time Tracker for the lazy in us all

## How it works

This time tracker is based off saving a file in a project. I am not going to explain Sublime projects. If you set up the Sublime project settings correctly, described below, everytimg you save a file in that project the tracker will "log it". The tracker will keep adding up the time until three things happen. 1) You save a file outside this open project. 2) You close the project with `super+ctrl+w`. 3) You quit Sublime. 

#### Set up
You will need to set up a few items in your project's `.sublime-project` file. In the settings section of the project file you can add two items `"ProjectTitle"` and `"ProjectPath"`. 

The Project Title is the name you want to save the time under. The tracker also lumps all saved actions under the project name so if you want to keep track accross saves of multiple files it does that.

The Project Path is not too important. When the tracker logs a save it tracks what files you have saved. It uses the full path of the file to keep track. But the full path can be long and repetative so I made it so you can have a section of it trucated off. The part that you put in the settings is the part you want gone. 

An example for reference
```
"ProjectPath": "/Users/AwesomeGuy5/Projects/SecretProjects/SuperSecretProject/",
"ProjectTitle": "Shh... Tell Know One"
```

