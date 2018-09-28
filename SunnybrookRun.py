#!/usr/bin/env/python

import os
from psychopy import data, gui
from psychopy import visual, core, event
from psychopy.visual import ShapeStim 
#set the directory from the images will be retrieved
Dir = "C:/Users/lkdoy/Scripts/GitHub/MA/ExperimentalCode/Stimuli/"
#file in reference to cwd that the stimuli are stored in
stimFile = "Stimuli/"

#MONITOR FOR LAB 36.4/29.7, 57cm away 

version = 'Pilot1.2'



def promptScreen():
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



def confidencePrompt(waitTime):
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
    #if event.getKeys(None, False, Clock) != 0: 
    first = event.getKeys(None, False, Clock)
    return(first[0])

    
    
def ChoiceConfidenceTrial(tStim, bStim, participant, presTime, waitTime):
    """ForcedChoiceTrial plays one trial of a forced choice paradigm given time and stimuli and returns the keypresses of the individual"""
    first = [(-1 , -1), (-1, -1)]
    #set the argument images to the matching image object
    TopImage.setImage(tStim)
    BottomImage.setImage(bStim)
    
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
    print(first[0])
    #if event.getKeys(None, False, Clock) != 0:
    first = event.getKeys(None, False, Clock)
    #return first tuple
    return(first[0])
    
    
#getStimuli takes a directory in the form of a string and a number of images to look for
def getStimuli(dir, num):
    """getStimuli fetches a file of images given a directory and returns a 2d array of those images paired"""
    #start with an empty 2d array of pairs of images
    len = int(num/2)
    
    stimuli = [[0 for x in range(2)] for y in range(len)]
    #print(stimuli)
    
    files = os.listdir(dir)
    
    x = 0
    y = 0
    
    #for all files in the given directory search for images and add them to the list paired off in a 2d array
    
    for f in files:
        #print(x)
        #print(y)
        
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

numImages = 8
#Collect participant information
expInfo = inputScreen()
    #without info experiment can't run. Immediately end.
if expInfo == False:
    exit()
        
#Initialize the screen object
Screen = visual.Window(size=(1920, 1080), monitor='defaultMonitor', fullscr=True, units = "deg")


#initialize all of the necessary image stimuli objects to be specified later
TopImage = visual.ImageStim(Screen, pos=(0,10))
BottomImage = visual.ImageStim(Screen, pos=(0, -10))
#fixation cross
fx = ShapeStim(Screen, vertices= 'cross', size=3, pos=(0, 0), lineColor='red', fillColor='red')

#create a clock object in order to time and report reaction times
Clock = core.Clock()


#collect stimuli and make a 2d array to be passed to the files
stim = getStimuli(Dir, numImages)
#print(stim)

dataFile = expInfo["Participant"] + version + "_data"
print(dataFile)
conditions = data.importConditions("./conditions.xlsx")

#Experiment handler
expData = data.ExperimentHandler(name=expInfo["Participant"], extraInfo= expInfo, version=version, dataFileName = dataFile)


trialData = data.TrialHandler(conditions, numImages/2)
#screen which is drawn until keystrokes indicate participant is ready
promptScreen()

#loop through stimulus list, presenting the image pairs in the trial setting.
expData.addLoop(trialData)
i = 0
for trial in trialData:
    result = ChoiceConfidenceTrial(stim[i][0], stim[i][1], "test", float(expInfo["presTime"]), float(expInfo["waitTime"]))
    conf = confidencePrompt(float(expInfo["confTime"]))
    trialData.addData("fchoice", result[0])
    trialData.addData("fcRT", result[1])  # add the data to our set
    trialData.addData("conf", conf[0])
    trialData.addData("confRT", conf[1])
    i+=1
    expData.nextEntry()
    #manage data in loop or outside. Write to a file with participant name generated by the participant handling file


expData.saveAsWideText(dataFile, delim=',', appendFile=True)

#cleanup cleanup
Screen.close()
#everybody clap your hands
core.quit()

