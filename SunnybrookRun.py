#!/usr/bin/env/python

import os, pandas
from psychopy import data, gui
from psychopy import visual, core, event
from psychopy.visual import ShapeStim 
#set the directory from the images will be retrieved
dir = "D:/allNoise"
#file in reference to cwd that the stimuli are stored in
stimFile = "Stimuli/"

imageFile = "./imageNames1.csv"

#MONITOR FOR LAB 36.4/29.7, 57cm away 

version = 'Pilot1.4'


def promptScreen(Screen, Clock):
    """simply a screen which allows the participant to get comfortable and ready before the experiment trials begin"""
    #draw text to buffer
    msg = visual.TextStim(Screen, text="Get Ready, press any key to begin.")
    msg.draw()
    
    #flip buffer to Screen
    Screen.flip()
    
    #reset clock for cpu sleeping
    Clock.reset()
    
    while not event.getKeys():
        core.wait(0.2)
    
    #flip back to blank before the handoff to something else
    Screen.flip()
    return
    
def inputScreen():
    """screen which returns a list container with the participant number, and presentation and wait times."""
    #initialize the dictionary
    info = {'Participant': "", 'presTime': 0, "waitTime" : 0, "confTime" : 0, 'ExpVersion' : version} 
    #actual dialog box. edits the dictionary
    infoDlg = gui.DlgFromDict(dictionary=info, 
                                title='SunnyBrook Experiment', 
                                order=['ExpVersion', 'Participant', "presTime", "waitTime", "confTime"], 
                                tip={'Participant #': 'trained visual observer, initials'}, 
                                fixed=['ExpVersion'])
    
    #cancel handler 
    if infoDlg.OK: 
        print(info)
        return(info)
    else:
        print('User Cancelled')
        return False

def simpleInputScreen():
    info = gui.Dlg(title="SunnyBrook VN Experiment")
    #info.addText('Participant #')
    info.addField('Participant:')
    #info.addText('presTime')
    info.addField('presTime', 0)
    #info.addText('waitTime')
    info.addField('waitTime', 0)
    #info.addText('confTime')
    info.addField("confTime", 0)
    info.addFixedField("ExpVersion", version)
    
    ok_data = info.show()  # show dialog and wait for OK or Cancel
    if info.OK:
        print(info)
        return(info)
    else:
        print('user cancelled')
        return False

def confidencePrompt(Screen, Clock, waitTime):
    """a script to call which asks participants to respond on a scale of 0-4 how confident they were"""
    first = [(-1 , -1), (-1, -1)]
    msg = visual.TextStim(Screen, text="How confident are you in your answer?")
    prompt = visual.TextStim(Screen, pos=(0, -1), text="1, 2, 3, 4")
    arrows = visual.TextStim(Screen, pos = (0, -2.5), text="  ^       ^  ")
    values = visual.TextStim(Screen, pos = (0, -4), text="don't know      confident")
    msg.draw()
    prompt.draw()
    arrows.draw()
    values.draw()
    
    Screen.flip()
    Clock.reset()
    
    core.wait(waitTime, waitTime)
    first = event.getKeys(None, False, Clock)
    return(first)

def ChoiceConfidenceTrial(TopImage, BottomImage, Clock, Screen, tStim, bStim, expData, presTime, waitTime):
    """ForcedChoiceTrial plays one trial of a forced choice paradigm given time and stimuli and returns the keypresses of the individual"""
    first = [(-1 , -1), (-1, -1)]
    #set the argument images to the matching image object
    TopImage.setImage(tStim)
    BottomImage.setImage(bStim)
    #fixation cross
    fx = ShapeStim(Screen, vertices= 'cross', size=2, pos=(0, 0), lineColor='red', fillColor='red')
    
    expData.addData("tStim", os.path.basename(tStim))
    expData.addData("bStim", os.path.basename(bStim))
    
    #draw the fixation cross to the screen
    fx.draw()
    
    Screen.flip()
    #reset clock for counting and reaction times
    Clock.reset()
    
    #fixation cross wait, make consistent at 1 second for now
    core.wait(1, 1)
    
    #draw the stimuli to the screen's buffer
    TopImage.draw(Screen)
    BottomImage.draw(Screen)
    
    #present the stimuli simultaneously by flipping the buffer
    Screen.flip()
    
    #reset the clock on next cpu tick to allow for stimulus duration
    Clock.reset()
    #Wait for the given amount of time in arg 4, still listen for keypresses though
    core.wait(presTime, presTime)
    
    q = visual.TextStim(Screen, text="Which image was clearer? Top/Bottom?")
    #draw to the buffer
    q.draw()
    #flip screen back to blank. This is the response screen
    Screen.flip()
    #reset clock for counting and reaction times
    Clock.reset()
    
    core.wait(waitTime, waitTime)
    #pull the input from the participant's trial and return it
    #if event.getKeys(None, False, Clock) != 0:
    first = event.getKeys(None, False, Clock)
    #return first tuple
    return(first)
    

def getCorrect(name1, name2):
    if 
    
def getImagesfromFile(dir, nameFile):
    
    
    files = os.listdir(dir)
    #read the namefile into a dataframe
    df = pandas.read_csv(nameFile)
    #get first column   
    names1 = df["top"]
    #get second column
    names2 = df["bottom"]
    
    length = len(names1.index)
    namePairs = [[0, 0] for y in range(length)] 
    x = 0
    
    for n1 in names1.iteritems():
        #print(n1[1])
        for f in files:
            if n1[1] == f:
                print('adding: ' + f)
                namePairs[x][0] = dir + '/' + f
                x += 1
                #print(namePairs)
    x = 0
    for n2 in names2.iteritems():
        #print(n2)
        for f in files:
            if n2[1] == f:
                print('adding: ' + f)
                namePairs[x][1] = dir + '/' + f
                x += 1
                
    
    print(namePairs)
    return namePairs

def populateFileArray(nameFile):
    df = pandas.readcsv(nameFile)
        #simpler version of above script


#getStimuli takes a directory in the form of a string and a number of images to look for
def getStimuli(dir, num):
    """getStimuli fetches a file of images given a directory and returns a 2d array of those images paired"""
    #start with an empty 2d array of pairs of images
    len = int(num/2)
    
    #stimuli = [(0 for x in range(2)], for y in range(len)]
    #print(stimuli)
    
    files = os.listdir(dir)
    
    x = 0
    y = 0
    
    #for all files in the given directory search for images and add them to the list paired off in a 2d array
    
    for f in files:

        if f.endswith(".png") or f.endswith(".jpg"):
            stimuli[y][x] = stimFile + f
        
        x += 1
        
        if(x == 2):
            x = 0
            y += 1
        
    #here is where randomization would occur if it were required
    #random.shuffle(stimuli)
    
    return stimuli
    

#===========================================================================================================================
#this is the beginning of the main program, Which actually runs the participant
#===========================================================================================================================

def main():
    #Collect participant information
    expInfo = inputScreen()
    
    print(expInfo)
    
    #without info experiment can't run. Immediately end.
    if expInfo == False:
        exit()
        
    #Initialize the screen object
    Screen = visual.Window(size=(1920, 1080), monitor='defaultMonitor', fullscr=True, units = "deg")
    
    TopImage = visual.ImageStim(Screen, pos=(0, 10))
    BottomImage = visual.ImageStim(Screen, pos=(0, -10))
    
    #create a clock object in order to time and report reaction times
    Clock = core.Clock()

    #collect stimuli and make a 2d array to be passed to the files
    stim = getImagesfromFile(dir, imageFile)

    dataFile = expInfo["Participant"] + version + "_data"

    #conditions = data.importConditions("./conditions.xlsx")

    #Experiment handler
    expData = data.ExperimentHandler(name=expInfo["Participant"], extraInfo= expInfo, version=version, dataFileName = dataFile + "backup")


    #trialData = data.TrialHandler(conditions, len(stim), method=u'random')

    #screen which is drawn until keystrokes indicate participant is ready
    promptScreen(Screen, Clock)

    #loop through stimulus list, presenting the image pairs in the trial setting.
    #expData.addLoop(trialData)

    i = 0
    for trial in trialData:
        result = ChoiceConfidenceTrial(TopImage, BottomImage, Clock, Screen, 
                                        stim[i][0], stim[i][1], expData, 
                                        float(expInfo["presTime"]), float(expInfo["waitTime"]))
                                        
        conf = confidencePrompt(Screen, Clock, float(expInfo["confTime"]))
        
        exp.addData("trial", i)
        #handling empty results
        if(len(result) > 0):
            expData.addData("fchoice", result[0][0])
            expData.addData("fcRT", result[0][1])  # add the data to our set
        else:
            expData.addData("fchoice", 'NR')
            expData.addData("fcRT", 'NR') 
    
        print(len(conf))
        if(len(conf) > 0):
            expData.addData("conf", conf[0][0])
            expData.addData("confRT", conf[0][1])
        else:
            #trialData
            expData.addData("conf", 'NR')
            expData.addData("confRT", 'NR') 
        
        i+=1
        expData.nextEntry()
        #manage data in loop or outside. Write to a file with participant name generated by the participant handling file


    expData.saveAsWideText(dataFile, delim=',', appendFile=True)


    #cleanup cleanup
    Screen.close()
    #everybody clap your hands
    core.quit()


if __name__ == "__main__":
    main()
    
