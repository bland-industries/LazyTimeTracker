#Lazy Time Tracker *Beta*
Sublime Text Time Tracker for the lazy in us all

This is a beta. I am not resposible for the loss of tracking your time. I currently am using is so I am very interested in making it the best ever.

## How it works

This time tracker is based off saving a file in a project. I am not going to explain Sublime projects. If you set up the Sublime project settings correctly, described below, everytime you save a file in that project the tracker will "log it". The tracker will keep adding up the time until three things happen. 1) You save a file outside this open project. 2) You close the project with `super+ctrl+w`. 3) You quit Sublime. 

#### Set up
First you will need to set up the settings of the plug in settings. The only one you really need to worry about to start with is the `"log_folder"` setting. This is the folder you want to save the log file into. Pick a spot and it will appear there. And make sure it is the full path and ends with a ` / `. The other settings are described below. What happens if you don't change this setting. It will add the files to your home directory. you just need to move them to the folder you eventually add to this settings and all should be fine.

You will need to set up at least one item in all your projects' `.sublime-project` file. In the settings section of the project file you can add the item `"ProjectTitle"`. The Project Title is the name you want to save the time under. The tracker also lumps all saved actions under the project name so if you want to keep track accross saves of multiple files it does that. What happens if you don't set up the Project Title. It will log all your files seperately and everytime you save a different file it will add a line to the log.

## Output

This tracker saves its logs to files. There is no need to sign up to any service or be connected to the internet. It saves to a .txt file or a .json file. It can save to both if you choose. 

The output of the txt file looks like this:

```
Project: Awesome Project - Time: 0:20:02.062951 - Date: 03/02/2015
  * FirstSave: 2015-03-02 11:05:33.991104
  * LastSave: 2015-03-02 11:25:36.054055
    - awesomeProject/file1.md
    - awesomeProject/file2.md
```

The output of the json file looks like this (prettied up):

```
  {
    "LastSave": "2015-03-02 11:05:36.054055",
    "ProjectName": "Awesome Project",
    "FirstSave": "2015-03-02 11:25:33.991104",
    "FilesSaved": [
      "awesomeProject/file1.md",
      "awesomeProject/file2.md"
    ],
    "Time": "0:20:02.062951",
    "Date": "03/02/2015"
  },
```

## View Output

Obviosly you can open the files and read the log as you would any other file. But for convience there is a built in way to view the log files. 

By default `super+ctrl+t` is set to display the log. However if you want to change it you can set it to something else with this:

```
{"keys": ["super+ctrl+t"], "command": "display_lazy_time_tracker"},
```

When you are using the txt output option it opens up the log file.

When you are using the json output option it loads the json and creates a scratch view to display the json nicely. 


## All the settings

After the initial set up above there are some more settings that can be configured for a better experience. Just as above there are the two areas of settings, plug-in settings and project settings.

#### Plugin settings

There are currently only three plugin settings: log_folder, log_file_name and log_file_format.

* `log_folder`: We talked about above but this is the folder you want to put the log files into. This can be any existing folder on your computer.
* `log_file_name`: If you don't want to use the default file name you can change it. Do not add an extension, it is figured base on the next setting.
* `log_file_format`: Currently there are only two file types that are available: JSON and txt. You can use one or the other or both. For Both you need them in an array as shown in the default.

Here is an example set up

```
{
    "log_folder": "/Users/username/Dropbox/LazyTimeTracker/",
    "log_file_name": "timetracker",
    "log_file_format": "json", // can be "json", "txt", or ["json", "txt"]
}
```

#### Project Settings

There are currently only two project settings: ProjectTitle and ProjectPath.

* `ProjectTitle`: As discussed above, this settings groups and labels files saved under a single time block.
* `ProjectPath`: This tracker keeps track of which files you save by their full file path. If you don't need the full path setting this to part of the path to the files will truncate the matching part so it doesn't log all the information. It is just a convienence thing. 

Here is an example of a full sublime project file.

```
{
    "folders":
    [
        {
            "follow_symlinks": true,
            "path": "."
        }
    ],
    "settings":
    {
        "ProjectPath": "/Users/username/Dropbox/projects/",
        "ProjectTitle": "Awesome Project"
    }
}
```



