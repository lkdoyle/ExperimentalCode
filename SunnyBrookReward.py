from psychopy import data, gui
from psychopy import visual, core, event
from psychopy.visual import ShapeStim 
import pandas as pd 
import numpy as np

#set the directory from the images will be retrieved
dir = ""
#file in reference to cwd that the stimuli are stored in
stimFile = "D:/SCENESGRAY/"

imageFile = ""

version = 'SBReward1.0'



def simpleInputScreen():
    
    pgui = gui.Dlg()
    pgui.addField("Subject ID:")
    pgui.addField("Session Number (0):")
    pgui.addField("CounterBalance:(cb) ")
    pgui.addField("presTime (0.2):")
    pgui.addField("waitTime (1.2):")
    pgui.addField("estTime (2):")
    
    # show the gui
    pgui.show()

    # put data in variables for return
    participant = pgui.data[0]
    sessNum = pgui.data[1]
    counterBalance = pgui.data[2]
    presTime = pgui.data[3]
    waitTime = pgui.data[4]
    estTime = pgui.data[5]
    
    return((participant, sessNum, counterBalance, presTime, waitTime, estTime))


def tagImages(nameArr, percCons, percRel):
    """tagImages takes a file of images (csv) and tags a random number of them with reward status. """
    le = len(nameArr)
    
    out = [[] for i in range(le)]
    
    randArr = [i for i in range(le)]
    #fill the new output with names
    i = 0
    for n in nameArr:
        out[i][0] = out.append(nameArr[i][0])
        out[i][1] = out.append(nameArr[i][1])
        i+=1
        
    #tag a random number of these with the percent consistent 
    for j in range(percCons):
        index = random.random(0, len(randArr))
        out[randArr.pop(index)][2] = 2
    
    #fill the reliable
    for j in range(percRel):
        index = random.random(0, len(randArr))
        out[randArr.pop(index)][2] = 1
        
    #fill the remainder
    for i in randArr:
        out[i][2] = 0
    
    return out
    
    
def getClickedImage(Mouse):
    """get clicked image gets the co-ordinates of the mouse on click and returns a number corresponding to the objects. """
    cords = Mouse.getPos()
    print(cords)
    if cords[0] >= 0:
        if cords[1] >= 0:
            #top right
            return 1
        else:
            #top left
            return 0
    else:
        if cords[1] >= 0:
            #bottom right
            return 3
        else:
            #bottom left
            return 2
            
def getImagesfromFile(dir, nameFile, percCond1, percCond2):
    """takes the directory containing all files, the csv file for experiment information, and the percentages fo reward conditions.
    This function returns a formatted array listing the paths to each image for later use""" 
    
    files = os.listdir(dir)
    #read the namefile into a dataframe
    df = pandas.read_csv(nameFile)
    #get first column   
    names1 = df["top"]
    #get second column
    names2 = df["bottom"]
    #get the reward condition
    flicker = df["reward"]
    
    length = len(names1.index)
    
    namePairs = [[] for y in range(length)]
    
    x = 0
    for n1 in names1.iteritems():
        for f in files:
            if n1[1] == f:
                #print('adding: ' + f)
                namePairs[x][0] = dir + '/' + f
                x += 1
                #print(namePairs)
    x = 0
    for n2 in names2.iteritems():
        for f in files:
            if n2[1] == f:
                #print('adding: ' + f)
                namePairs[x][1] = dir + '/' + f
                x += 1
    x = 0
    for flick in flicker.iteritems():
        namePairs[x][2] = flick
        x+=1
    print(namePairs)
    return namePairs
    
    
def fourArmedTrial(StimArr, Clock, Screen, Mouse, trialData, presTime):
    """fourArmedTrial takes in StimArr, which is a list of list of lists, first list containing a list of images, the second list containing image and reward tag"""
    #reset the mouse so previous clicks don't count
    Mouse.clickReset()
    
    #set up stimuli REDUNDANT AFTER FIRST TRIAL, COULD MOVE FOR EFFICIENCY 
    topLeft = visual.ImageStim(Screen, pos=(-6, 6))
    topRight = visual.ImageStim(Screen, pos=(6, 6))
    botLeft = visual.ImageStim(Screen, pos=(-6, -6))
    botRight = visual.ImageStim(Screen, pos=(6, -6))
    #assign corresponding images
    topLeft.setImage(StimArr[0][0])
    topRight.setImage(StimArr[1][0])
    botLeft.setImage(StimArr[2][0])
    botRight.setImage(StimArr[3][0])
    #assign reward values
    topLeftReward = StimArr[0][1]
    topRightReward = StimArr[1][1]
    botLeftReward = StimArr[2][1]
    botRightReward = StimArr[3][1]
    
    
def presentTrial(Screen, Clock, rewardCount):
    
    Screen.flip()
    Mouse.setPos(newPos=(0,0))
    Clock.reset()
    
    rewardCount = 0
    
#===========================================================================================================================
#this is the beginning of the main program, Which actually runs the participant
#===========================================================================================================================

def main():
    
#===============================
 #Global Variables
#===============================
    presTime = 2
    fxTime = 1
    revealTime = 3
    trialTime = presTime + fxTime 
    #full clock that won't reset
    expClock = core.Clock()
    #trial clock resets each trial
    trialClock = core.Clock()
    #response clock
    respClock = core.Clock()
    #Screen object to instantiate
    Screen = visual.Window(monitor='defaultMonitor', fullscr=True, units = "deg")
    #fixation cross 
    fixation = visual.TextStim(Screen, text='+', height=.05)
    #mouse event for later measurement
    Mouse = event.Mouse(visible = True, newPos = (0,0), win = Screen)
#===============================
 #Stimuli Specific to individual
#===============================
    #this is where you would import the array of stimuli from file
    stims = [["0.jpg", 1], ["1.jpg", 0], ["6.jpg", 2], ["8.jpg", 3]]
    
#===============================
 #Running the participant
#===============================

    for trial in range(len(stims))
        trialClock.reset()
        thisOnset = trial * trialTime 
        trialData = pd.DataFrame()
        
        #wait until stimulus onset time
        while expClock.getTime() < thisOnset:
            core.wait(.001)
            
        out.loc[thisTrial,'onsetactual'] = expClock.getTime()
        
        
        while expClock.getTime() < (thisOnset+presTime):
            rewardResp = fourArmedTrial(stims[trial], resplock, Screen, Mouse, trialData, presTime)
            
        #record data if response was clocked
        if rewardResp:
            trialData.loc[trial, 'choice'] = rewardResp[0]
            trailData.loc[trial, 'RT'] = rewardResp[1]
            
            
    return None 
    
    
if __name__ == "__main__":
    main()
    
