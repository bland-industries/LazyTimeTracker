import sublime, sublime_plugin, time, datetime, random, os, json 
from datetime import timedelta

global lazyTrackerGlobal
lazyTrackerGlobal = None

# Command to display the logging.
# to run command: view.run_command('display_lazy_time_tracker')
class DisplayLazyTimeTrackerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ProjectShift.displayTimeTracking(edit)


# Command to allow for Lazy Time Tracker to clean up before user quits
class PreExitCommand(sublime_plugin.WindowCommand):
    def run(self):
        global lazyTrackerGlobal
        if lazyTrackerGlobal is not None:
            lazyTrackerGlobal.closeShift()
            lazyTrackerGlobal = None
        self.window.run_command('exit')


# Command to allow for Lazy Time Tracker to clean up before user closes the project window
class PreWindowCloseCommand(sublime_plugin.WindowCommand):
    def run(self):
        global lazyTrackerGlobal
        if lazyTrackerGlobal is not None:
            if lazyTrackerGlobal.checkShift(self.window.active_view()):
                lazyTrackerGlobal.closeShift()
                lazyTrackerGlobal = None
        self.window.run_command('close_window')

# Class to handle all the project details
class ProjectShift:
    def __init__(self, view):
        self.projectName = view.settings().get('ProjectTitle', view.file_name())
        self.savedFiles = []
        self.savedFiles.append(self.getTrucatedFilePath(view))
        self.startTime = datetime.datetime.now()
        self.lastSave = self.startTime;
        self.elapsedTime = 0

    @staticmethod
    def getSettings():
        return sublime.load_settings("LazyTimeTracker.sublime-settings")

    @staticmethod
    def getSetting(setting):
        return ProjectShift.getSettings().get(setting)

    @staticmethod
    def displayTimeTracking(edit):
        outputFormat = ProjectShift.getSetting('log_file_format')
        if isinstance(outputFormat, list):
            for item in outputFormat:
                if item == "json":
                    ProjectShift.displayTimeTrackingJSON(edit)
                elif item == "txt":
                    ProjectShift.displayTimeTrackingTXT()
                else:
                    print("You need to open the package settings and add a 'log_file_format'.")
        else:
            if outputFormat == "json":
                ProjectShift.displayTimeTrackingJSON(edit)
            elif outputFormat == "txt":
                ProjectShift.displayTimeTrackingTXT()
            else:
                print("You need to open the package settings and add a 'log_file_format'.")


    @staticmethod
    def displayTimeTrackingTXT():
        sublime.active_window().open_file(ProjectShift.getLogFilePath() + ".txt")
        

    @staticmethod
    def displayTimeTrackingJSON(edit):
        
        json_data=open(ProjectShift.getLogFilePath() +".json")
        data = json.load(json_data)

        view = sublime.active_window().new_file()
        view.set_scratch(True)
        view.set_name("Lazy Tracker")

        text = ProjectShift.condensedOutputDisplay(data)

        view.insert(edit, 0, text)


    @staticmethod
    def timedeltaFromString(string):
        parts = string.split(":")
        return datetime.timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=float(parts[2]))

    @staticmethod
    def totalTime(data):
        totalTime = timedelta(days=0)
        for shift in data:
            totalTime += ProjectShift.timedeltaFromString(shift['Time'])
        print(totalTime)
        

    @staticmethod
    def formatOutputDisplay(data):
        string = ""
        currentDate = data[0]['Date']
        string += currentDate + "\n\n"
        for shift in data:
            if currentDate != shift['Date']:
                string += "\n\n" + shift['Date'] + "\n\n"
                currentDate = shift['Date']

            string += shift['ProjectName'] + " - Time: " + shift['Time'] + "\n"
            if "FirstSave" in shift:
                string += "  * From: " + shift['FirstSave'] + "  To: " + shift["LastSave"] + "\n"
            for f in shift['FilesSaved']:
                string += "    - " + f + "\n"
            string += "\n\n"

        return string


    @staticmethod
    def condensedOutputDisplay(data):
        projects = []

        currentDate = data[0]['Date']
        dateData = {'Date': currentDate, 'Projects': {}, 'DateTime': timedelta(days=0)}
        for shift in data:
            if currentDate != shift['Date']:
                projects.append(dateData)
                currentDate = shift['Date']
                dateData = {'Date': currentDate, 'Projects': {}, 'DateTime': timedelta(days=0)}

            dateData['DateTime'] += ProjectShift.timedeltaFromString(shift['Time'])

            if shift['ProjectName'] in dateData['Projects']:
                print("yes")
                dateData['Projects'][shift['ProjectName']]['ProjectTime'] += ProjectShift.timedeltaFromString(shift['Time'])
            else:
                print("no")
                dateData['Projects'][shift['ProjectName']] = {'ProjectTime': ProjectShift.timedeltaFromString(shift['Time']), 'projectFilesString': ""}
            
            if "FirstSave" in shift:
                dateData['Projects'][shift['ProjectName']]['projectFilesString'] += "  * From: " + shift['FirstSave'] + "  To: " + shift["LastSave"] + "\n"
            # for f in shift['FilesSaved']:
            #     dateData['Projects'][shift['ProjectName']]['projectFilesString'] += "    - " + f + "\n"

        projects.append(dateData)

        string = ""

        for day in projects:
            string +="\n\n" + day['Date'] + " -Time: " + str(day['DateTime']) + "\n\n"
            for key in day['Projects']:
                string += key + " - Time: " + str(day['Projects'][key]['ProjectTime']) + "\n"
                string += day['Projects'][key]['projectFilesString']
                string += "\n"

        return string


    @staticmethod
    def getLogFilePath():
        logFileName = ProjectShift.getSetting('log_file_name')
        logFolderPath = ProjectShift.getSetting('log_folder')
        if logFolderPath is False:
            logFolderPath = os.path.expanduser('~') + "/"
        return logFolderPath + logFileName


    def closeShift(self):
        self.setLastSave()
        self.elapsedTime = self.lastSave - self.startTime
        self.printLog()


    def printLog(self):
        outputFormat = ProjectShift.getSetting('log_file_format')
        if isinstance(outputFormat, list):
            for item in outputFormat:
                if item == "json":
                    self.printLogJSON()
                elif item == "txt":
                    self.printLogTXT()
                else:
                    self.printLogConsole()
        else:
            if outputFormat == "json":
                self.printLogJSON()
            elif outputFormat == "txt":
                self.printLogTXT()
            else:
                self.printLogConsole()



    def printLogJSON(self):
        textJSON = self.formatOutputJSON()
        self.printToFileJSON(textJSON)

    def printLogTXT(self):
        text = self.formatOutputLong()
        self.printToFile(text)

    def printLogConsole(self):
        text = self.formatOutputLong()
        print(text)



    def formatOutputLong(self):
        string = "\n"
        if self.projectName is None:
            string += "Project: " + "Misc"
        else:
            string += "Project: " + self.projectName
        string += " - Time: " + str(self.elapsedTime)
        string += " - Date: " + self.lastSave.strftime("%m/%d/%Y")
        string += "\n"
        string += "  * FirstSave: " + str(self.startTime) + "\n"
        string += "  * LastSave: " + str(self.lastSave) + "\n"
        for f in self.savedFiles:
            string += "\t- " + f + "\n"
        string += "\n"

        return string


    def formatOutputJSON(self):
        output = {}
        output['ProjectName'] = self.projectName
        output['Time'] = str(self.elapsedTime)
        output['Date'] = self.lastSave.strftime('%m/%d/%Y')
        output['FilesSaved'] = self.savedFiles
        output['FirstSave'] = str(self.startTime)
        output['LastSave'] = str(self.lastSave)

        return json.dumps(output)


    def getTrucatedFilePath (self, view):
        removeString = view.settings().get('ProjectPath', None)
        if removeString is not None:
            path = view.file_name()
            return path.replace(removeString, "")
        else:
            return view.file_name()



    def printToFile(self, text):
        with open(ProjectShift.getLogFilePath() + ".txt", "a") as myfile:
            myfile.write(text)
            myfile.close()


    def printToFileJSON(self, text):

        if not os.path.isfile(ProjectShift.getLogFilePath() + ".json"):
            text = "[\n" + text + "\n]"
            with open(ProjectShift.getLogFilePath() + ".json", "a") as myfile:
                myfile.write(text)
                myfile.close()
        else:
            text = ",\n" + text + "\n]"
        
            file = open(ProjectShift.getLogFilePath() + ".json", "r+")

            file.seek(0, os.SEEK_END)
            pos = file.tell() - 1
            while pos > 0 and file.read(1) != "\n":
                pos -= 1
                file.seek(pos, os.SEEK_SET)

            if pos > 0:
                file.seek(pos, os.SEEK_SET)
                file.truncate()

            file.write(text)

            file.close()

    def addFile(self, view):
        self.savedFiles.append(self.getTrucatedFilePath(view))

    # return true if it is a fresh shift, false if it stale
    def setLastSave (self):
        if (self.lastSave + datetime.timedelta(minutes=15) < datetime.datetime.now()):
            self.lastSave = self.lastSave + datetime.timedelta(minutes=15)
            return False
        else:
            self.lastSave = datetime.datetime.now()
            return True
    # return true if the shift is the same
    # return false if the shift has changed
    def checkShift(self, view):
        ret = False
        project = view.settings().get('ProjectTitle', view.file_name())
        if (project == self.projectName):
            if self.setLastSave():
                ret = True
        else:
            ret = False

        if ret:
            self.addFile(view)
        
        return ret




class LazyTimeTrackingEventHandler(sublime_plugin.EventListener):

    def __init__(self):
        global lazyTrackerGlobal

        lazyTrackerGlobal = None








    def on_post_save(self, view):
        if int(sublime.version()) >= 2000 and int(sublime.version()) < 3000:
            self.logShiftSave(view)

    def on_post_save_async(self, view):
        self.logShiftSave(view)


    def logShiftSave(self, view):
        global lazyTrackerGlobal
        if lazyTrackerGlobal is None:
            lazyTrackerGlobal = ProjectShift(view)
        else:
            if not lazyTrackerGlobal.checkShift(view):
                lazyTrackerGlobal.closeShift()
                lazyTrackerGlobal = ProjectShift(view)

