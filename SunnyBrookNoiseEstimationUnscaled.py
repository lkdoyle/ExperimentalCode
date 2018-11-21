#!/usr/bin/env/python

import os, pandas, random, numpy
from psychopy import data, gui
from psychopy import visual, core, event
from psychopy.visual import ShapeStim 
from PIL import Image


#set the directory from the images will be retrieved
dir = "D:/GreyscaleSP4"
#file in reference to cwd that the stimuli are stored in
ndir = "D:/OBJECTSGRAY/"

imageFile = "./lists/SPNoiseRating0.csv"

#MONITOR FOR LAB 36.4/29.7, 57cm away 

version = 'NE1.0'


def promptScreen(Screen, Clock):
    """simply a screen which allows the participant to get comfortable and ready before the experiment trials begin"""
    #draw text to buffer
    msg = visual.TextStim(Screen, color='black', text="Get Ready, press any key to begin.")
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
        #print(info)
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
    msg = visual.TextStim(Screen, color='black', text="How confident are you in your answer?")
    prompt = visual.TextStim(Screen, color='black', pos=(0, -1), text="1, 2, 3, 4")
    arrows = visual.TextStim(Screen, color='black', pos = (0, -2.5), text="  ^       ^  ")
    values = visual.TextStim(Screen, color='black', pos = (0, -4), text="don't know      confident")
    msg.draw()
    prompt.draw()
    arrows.draw()
    values.draw()
    
    Screen.flip()
    Clock.reset()
    
    core.wait(waitTime, waitTime)
    first = event.getKeys(None, False, Clock)
    return(first)

def ChoiceConfidenceTrial(TopImage, BottomImage, flicker, Clock, Screen, tStim, bStim, expData, presTime, waitTime):
    """ForcedChoiceTrial plays one trial of a forced choice paradigm given time and stimuli and returns the keypresses of the individual"""
    first = [(-1 , -1), (-1, -1)]
    #set the argument images to the matching image object
    TopImage.setImage(tStim)
    BottomImage.setImage(bStim)
    #fixation cross
    fx = ShapeStim(Screen, vertices= 'cross', size = 1, pos=(0, 0), lineColor = 'red', fillColor = 'red')
    
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
    
    #4 hz jitter begin
    #if top image is flickered
    for i in range(2):
        xdiff = random.uniform(-.25, .25)
        ydiff = random.uniform(-.25, .25)
        x1diff = random.uniform(-.25, .25)
        y1diff = random.uniform(-.25, .25)
        
        if flicker == 0:
            BottomImage.pos = (0, -8)
            TopImage.pos = (0, 8)
            
        elif flicker == 1: #flicker == 1, bottom image needs to be flickered
            #present the stimuli simultaneously by flipping the buffer
            #Screen.flip()
            BottomImage.pos = (0+xdiff, -8+ydiff)
            
        elif flicker == 2:
            #present the stimuli simultaneously by flipping the buffer
            #Screen.flip()
            TopImage.pos = (0+xdiff, 8+ydiff)
            #reset the clock on next cpu tick to allow for stimulus duration
            
        else: #flicker == 3:
            #Screen.flip()
            TopImage.pos = (0+x1diff, 8+y1diff)
            BottomImage.pos = (0+xdiff, -8+ydiff)
            
        #Wait for the 1/3 given amount of time in arg 4, still listen for keypresses though
        TopImage.draw(Screen)
        BottomImage.draw(Screen)
        Screen.flip()
        Clock.reset()
        core.wait(presTime/10, presTime/10)
        
    BottomImage.pos = (0, -8)
    TopImage.pos = (0, 8)
    TopImage.draw(Screen)
    BottomImage.draw(Screen)
    Screen.flip()
    core.wait(2*presTime/3, 2*presTime/3)
    
    
    q = visual.TextStim(Screen, color='black', text="Which image was clearer? Top/Bottom?")
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
    
    #return pressed Keys
    return(first)
    
def getCorrect(name1, name2):
    """returns the noise difference between the two passed images as an int"""
    i = 0
    j = 0
    ret = [0, 0]
    if "HighNoise" in name1:
        i = 3
    elif "MedNoise" in name1:
        i = 2
    elif "LowNoise" in name1:
        i = 1
        
    if "HighNoise" in name2:
        j = 3
    elif "MedNoise" in name2:
        j = 2
    elif "LowNoise" in name2:
        j = 1
        
    if i > j:
        ret[0] = "down"
    elif i == j:
        ret[0] = "equal"
    else:
        ret[0] = "up"
    
    ret[1] = abs(i-j)
    return(ret)

def getImagesfromFile(dir, nameFile):
    files = os.listdir(dir)
    #read the namefile into a dataframe
    df = pandas.read_csv(nameFile)
    print(df)
    #get first column   
    names1 = df["top"]
    #get second column
    names2 = df["bottom"]
    #get the flicker condition
    flicker = df["flicker"]
    
    length = len(names1.index)
    
    namePairs = [[0, 0, 0] for y in range(length)]
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

def populateFileArray(nameFile):
    df = pandas.readcsv(nameFile)
        #simpler version of above script

def noiseEstimation(chosenImage, Clock, Screen, expData):
    noiseScale = visual.RatingScale(Screen, lineColor='black', choices=None, low=0, high=300, tickMarks=None, 
                                    labels=None, mouseOnly=True, showValue=False, acceptText='Match', 
                                    acceptKeys='return')
    #change image to the default read
    name, ext = os.path.splitext(chosenImage)
    name = os.path.basename(name)
    defImage = name.split('_', 1)[0]
    
    tmp = Image.open(ndir + defImage + ".jpg")
    pic = numpy.array(tmp)
    im = Image.fromarray(pic)
    pres =  visual.ImageStim(Screen, im, pos=(0, 4), size=(20,20))
    num = 0
    
    while noiseScale.noResponse:
        noiseScale.draw()
        pres.draw()
        Screen.flip()
        rating = noiseScale.getRating()
        if rating:
            if rating != num:
                num = rating
                n = rating/1000
                tp = applySaltPepper(pic, n)
                tsp = Image.fromarray(tp)
                pres.setImage(tsp)

    rating = noiseScale.getRating()
    #print("rating:", rating)
    ratingRT = noiseScale.getRT()
    #print("rating RT:", decisionTime)
    choiceHistory = noiseScale.getHistory()
    print("rating Hist:", choiceHistory)
    
    return((rating, ratingRT))
    
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
    
    
def applySaltPepper(imagearray, noiseProb):
    #applies noise and returns images
    row, col = imagearray.shape
    nPic = imagearray
    output = numpy.zeros((row, col), numpy.uint8)
    inv = 1 - noiseProb
    
    for i in range(row):
        for j in range(col):
            rdn = random.uniform(0, 1)
            if rdn < noiseProb:
                output[i][j] = 0
            elif rdn > inv:  
                output[i][j] = 255
            else:
                output[i][j] = nPic[i][j]
    return output
    
    
#===========================================================================================================================
#this is the beginning of the main program, Which actually runs the participant
#===========================================================================================================================

def main():

    #Collect participant information
    expInfo = inputScreen()
    
    breakNum = 3
    breaktime = 60
    print(expInfo)
    
    #without info experiment can't run. Immediately end.
    if expInfo == False:
        exit()
        
    #Initialize the screen object
    Screen = visual.Window(size=(1920, 1080), monitor='defaultMonitor', fullscr=False, color='white', units = "deg")
    
    TopImage = visual.ImageStim(Screen, pos=(0, 8))
    BottomImage = visual.ImageStim(Screen, pos=(0, -8))
    #create a clock object in order to time and report reaction times
    Clock = core.Clock()
    
    #collect stimuli and make a 2d array to be passed to the files
    stim = getImagesfromFile(dir, imageFile)

    dataFile = expInfo["Participant"] + version + "_data"

    #Experiment handler
    expData = data.ExperimentHandler(name=expInfo["Participant"], extraInfo= expInfo, version=version, dataFileName = dataFile + "backup")

    #screen which is drawn until keystrokes indicate participant is ready
    promptScreen(Screen, Clock)

    #loop through stimulus list, presenting the image pairs in the trial setting.
    #expData.addLoop(trialData)
    
    #shuffle the stimuli
    random.shuffle(stim)
    breaknote = int(len(stim) / breakNum)
    
    for i in range(len(stim)):

        #breakHandling
        if i%breaknote == 0 and i != 0:
            visual.TextStim(Screen, color='black', text="1 minute break").draw()
            Screen.flip()
            core.wait(breaktime/3, breaktime/3)
            #wait half of the break duration
            
            k = event.getKeys()
            if k == 'escape':
                k = event.getKeys()
                Screen.close
                core.quit
                print("participant cancelled")
                
            core.wait(2*breaktime/3, 2*breaktime/3)
            Screen.flip()
            
            promptScreen(Screen, Clock)
            
        
        flicker = stim[i][2][1]
        
        expData.addData("trial", i)
        
        result = ChoiceConfidenceTrial(TopImage, BottomImage, flicker, Clock, Screen, 
                                        stim[i][0], stim[i][1], expData, 
                                        float(expInfo["presTime"]), float(expInfo["waitTime"]))
                                        
        #checking for participant cancel
        
        if result:
            if result[0][0] == 'escape':
                print("participant cancelled")
                Screen.close
                core.quit
                return("participant cancelled")
                
        if result:
            if result[0][0] == 'up':
                chosenImage = stim[i][0] #present chosen image
                #present the noise estimation task
                noise = noiseEstimation(chosenImage, Clock, Screen, expData)
                
            elif result[0][0] == 'down':
                chosenImage = stim[i][1] #present chosen image
                #present the noise estimation task
                noise = noiseEstimation(chosenImage, Clock, Screen, expData)
            else:
                visual.TextStim(Screen, color='black', text="Missing Response").draw()
                Screen.flip()
                core.wait(3)
        
        conf = confidencePrompt(Screen, Clock, float(expInfo["confTime"]))
        
        correct = getCorrect(stim[i][0], stim[i][1])
        
        expData.addData("corrAns", correct[0])
        expData.addData("stimDiff", correct[1])
        expData.addData("flicker", flicker)
        
        #handling empty results
        if(len(result) > 0):
            expData.addData("fchoice", result[0][0])
            expData.addData("fcRT", result[0][1])  # add the data to our set
        
        else:
            expData.addData("fchoice", 'NaN')
            expData.addData("fcRT", 'NaN')
        
        if(len(conf) > 0):
            expData.addData("conf", conf[0][0])
            expData.addData("confRT", conf[0][1])
        
        else:
            #trialData
            expData.addData("conf", 'NaN')
            expData.addData("confRT", 'NaN')
            
        if noise:
            expData.addData("est", noise)
        else:
            expData.addData("est", 'NaN')
            
        
        expData.nextEntry()
        #manage data in loop or outside. Write to a file with participant name generated by the participant handling file
        
        
    expData.saveAsWideText(dataFile, delim=',', appendFile=True)
        
        
    #cleanup cleanup
    Screen.close()
    #everybody clap your hands
    core.quit()

if __name__ == "__main__":
    main()
    
