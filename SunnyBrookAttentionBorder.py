#!/usr/bin/env/python

import os, pandas, random, numpy, itertools
from psychopy import data, gui
from psychopy import visual, core, event
from psychopy.visual import ShapeStim 
from PIL import Image
    

#set the directory from the images will be retrieved
dir = "D:/SCENESGRAYSP4/"
#file in reference to cwd that the stimuli are stored in
ndir = "D:/SCENESGRAY/"

#MONITOR FOR LAB 36.4/29.7, 57cm away 
stimNumUndergrad = 468
stimNumSunnybrook = 72
stimNumTraining = 10
version = 'PosNE2.0'

#TOOLS TO MAKE AN IMAGE FILE UNIQUE TO PARTICIPANT
def makeImageFile(dr, imgSave, numCop, size, num):
    """
    MakeImageFile takes in a directory of stored images with numCop copies of each image. 
    It then returns a randomized and paired set of each of the image name, neatly written to a csv file
    """
    tmp = os.listdir(dr)
    imgs = []
    out = [[] for i in range(size)]
    nums = ''
    
    fnames = [(imgSave + str(i) + ".csv") for i in range(num)]
    
    #sort temp array grabbing every numCop items and apending them together
    for i in range(0, len(tmp), numCop):
        #append grouped items as they share a name
        imgs.append(tmp[i:i+numCop])
    #reading the image names into file is now complete
    
    #make a list iterable by the permutations tool
    for i in range(numCop):
        nums = nums + str(i)
        
    #make a permutations list composed of all the permutations of noise levels
    per = [''.join(p) for p in itertools.permutations(nums, 2)]
    #per is now an iterable permutation list used to construct the pairs
    print(per)
    switch = size/len(per)
    #print(switch)
    #flicker array for equal flickers between blocks. 0 is neither, 1 is top 2 is bottom 3 is both.
    
    #begin the big loop to do the removing and writing to randomized non duplicated lists
    
    for name in fnames:
        j = 0
        farr = flickerarr(switch+1)
        parr = promptarr(switch+1)
        switchtest = switch
        i = 0
        for i in range(size): 
            if i >= int(switchtest):
                print(i)
                j+=1 #switch to next permutation
                print("switching: ", j)
                farr = flickerarr(switch+1)
                parr = promptarr(switch+1)
                switchtest+=switch
                
            #permutation handler, each time the counter reaches the switch threshold, move to next permutation
            
            #get first random set and pull it from the list to ensure no duplicates
            r1 = random.randint(0, len(imgs)-1)
            tarr = imgs.pop(r1)
            
            t = int(per[j][0])
            
            r2 = random.randint(0, len(imgs)-1)
            barr = imgs.pop(r2)
            
            b = int(per[j][1])
            
            out[i].append(tarr[t])
            out[i].append(barr[b])
            out[i].append(farr.pop())
            out[i].append(parr.pop())
            
        with open(name, 'w') as f:
            f.write("top,bottom,cue,prompt\n")
            for item in out:
                f.write("%s,%s,%s,%s\n" % (item[0], item[1], item[2], item[3]))

def flickerarr(le):
    flickerarr = []
    #print("quarter: ", quarter)

    for i in range(int(le)):
        flickerarr.append(0)
        flickerarr.append(1)
        flickerarr.append(2)
        flickerarr.append(3)
        
    return(flickerarr)

def promptarr(le):
    promptarr = []
    for i in range(int(le)):
        if i % 2 == 0:
            promptarr.append(0)
        else:
            promptarr.append(1)
    return promptarr

def promptScreen(Screen, Clock):
    """simply a screen which allows the participant to get comfortable and ready before the experiment trials begin"""
    #draw text to buffer
    msg = visual.TextStim(Screen, wrapWidth=1000, text="Get Ready, press any key to begin.")
    msg.draw()
    
    #flip buffer to Screen
    Screen.flip()
    #reset clock for cpu sleeping
    Clock.reset()
    
    while not event.getKeys():
        core.wait(0.1)
    
    #flip back to blank before the handoff to something else
    Screen.flip()
    return

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

def confidencePrompt(fx, Screen, Clock, trialClock, waitTime, counterBalance):
    """a script to call which asks participants to respond on a scale of 0-7 how confident they were"""
    first = [[-1 , -1]]
    
    targetTime = trialClock.getTime() + waitTime
    
    if counterBalance == 'cb':
        msg = visual.TextStim(Screen, wrapWidth=1000,pos=(0, 1), text="How confident are you in your answer?")
        ConfScale = visual.RatingScale(Screen, showAccept=False, scale="Certain              Guessed")
        ConfScale.draw()
       
        Clock.reset()
        while trialClock.getTime() < targetTime:
            msg.draw()
            ConfScale.draw()
            fx.draw()
            Screen.flip()
            core.wait(0.001)
        
        if ConfScale:
            first[0][0] = ConfScale.getRating()
            first[0][1] = ConfScale.getRT()
        else:
            first[0][0] = 'NaN'
            first[0][1] = 'NaN'
    
    else:
        msg = visual.TextStim(Screen, wrapWidth=1000,pos=(0, 1), text="How confident are you in your answer?")
        ConfScale = visual.RatingScale(Screen, showAccept=False, scale="Guessed              Certain")
        Clock.reset()
        
        while trialClock.getTime() < targetTime:
            msg.draw()
            ConfScale.draw()
            fx.draw()
            Screen.flip()
            core.wait(0.001)
        
        if ConfScale:
            first[0][0] = ConfScale.getRating()
            first[0][1] = ConfScale.getRT()
        else:
            first[0][0] = 'NaN'
            first[0][1] = 'NaN'
        
        while Clock.getTime() < .992:
            core.wait(0.001)
            
    return(first)

def ChoiceConfidenceTrial(fx, TopImage, BottomImage, cue, prompt, Clock, trialClock, Screen, tStim, bStim, presTime, waitTime):
    """ForcedChoiceTrial plays one trial of a forced choice paradigm given time and stimuli and returns the keypresses of the individual"""
    first = [(-1 , -1), (-1, -1)]
    #set the argument images to the matching image object
    TopImage.setImage(tStim)
    BottomImage.setImage(bStim)
    
    topFrame = visual.Rect(Screen, width=9, height=9, lineColorSpace='rgb', fillColorSpace='rgb', pos=(0, 6), lineColor=(.4,.4,.4), fillColor=(.4,.4,.4))
    bottomFrame = visual.Rect(Screen, width=9, height=9, lineColorSpace='rgb', fillColorSpace='rgb', pos=(0, -6), lineColor=(.4,.4,.4), fillColor=(.4,.4,.4))
    
    #time before cue starts 56 milliseconds on screen without cue
    cueOnsetTime = 1.200
    #time cue is onscreen
    cueActionTime = .144
    
    #draw the fixation cross to the screen
    fx.draw()
    topFrame.draw()
    bottomFrame.draw()
    Screen.flip()
    #draw to screen again, you'll need it
    
    fx.draw()
    
    #wait for fixation cross time
    while trialClock.getTime() < cueOnsetTime:
        core.wait(0.001)
        
    #THIS IS WHEN POSNER CUEING BEGINS
    if cue == 0: #no cue, do nothing to images and wait.
        #DO NOTHING
        while trialClock.getTime() < cueOnsetTime+0.046:
            core.wait(0.001)
            
    elif cue == 1: #flicker == 1, bottom image needs to be cued
        bottomFrame.fillColor = (1, 1, 1)
        bottomFrame.lineColor = (1, 1, 1)
        topFrame.draw()
        bottomFrame.draw()
        Screen.flip()
        fx.draw()
        while trialClock.getTime() < cueOnsetTime+0.046:
            core.wait(0.001)
        
    elif cue == 2: #flicker == 2, top image needs to be cued
        topFrame.fillColor = (1, 1, 1)
        topFrame.lineColor = (1, 1, 1)
        topFrame.draw()
        bottomFrame.draw()
        Screen.flip()
        fx.draw()
        while trialClock.getTime() < cueOnsetTime+0.046:
            core.wait(0.001)
            
    else: #flicker == 3: both image need to be cued
        topFrame.fillColor = (1, 1, 1)
        bottomFrame.fillColor = (1, 1, 1)
        topFrame.lineColor = (1, 1, 1)
        bottomFrame.lineColor = (1, 1, 1)
        topFrame.draw()
        bottomFrame.draw()
        Screen.flip()
        fx.draw()
        
        while trialClock.getTime() < cueOnsetTime+0.046:
            core.wait(0.001)
            
    #reset back to normal
    topFrame.fillColor = (.4, .4, .4)
    bottomFrame.fillColor = (.4, .4, .4)
    topFrame.lineColor = (.4, .4, .4)
    bottomFrame.lineColor = (.4, .4, .4)
    topFrame.draw()
    bottomFrame.draw()
    Screen.flip()
    fx.draw()
    
    #wait another 50 milliseconds
    while trialClock.getTime() < cueOnsetTime + 0.046 + cueActionTime:
        core.wait(0.001)
        
    topFrame.draw()
    bottomFrame.draw()
    TopImage.draw(Screen)
    BottomImage.draw(Screen)
    fx.draw()
    Screen.flip()
    Clock.reset()
    
    while trialClock.getTime() < cueOnsetTime + cueActionTime + 0.046 + presTime:
        core.wait(0.001)
    
    q = visual.TextStim(Screen, color='white', wrapWidth=1000, pos=(0, 1), text="Which image was clearer? Top/Bottom?")
    #draw to the buffer
    q.draw()
    fx.draw()
    Screen.flip()
    Clock.reset()
    
    while trialClock.getTime() < cueOnsetTime + cueActionTime + 0.046 + presTime + waitTime:
        core.wait(0.001)
        
    #pull the input from the participant's trial and return it
    first = event.getKeys(None, False, Clock)
    
    #print(trialClock.getTime())
    #return pressed Keys
    return(first)
    
def getImagesfromFile(dir, nameFile):
    files = os.listdir(dir)
    #read the namefile into a dataframe
    df = pandas.read_csv(nameFile)
    #get first column   
    names1 = df["top"]
    #get second column
    names2 = df["bottom"]
    #get the cue condition
    cue = df["cue"]
    #get prompt condition
    prompt = df["prompt"]
    length = len(names1.index)
    
    namePairs = [[0, 0, 0, 0] for y in range(length)]
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
    for c in cue.iteritems():
        namePairs[x][2] = c[1]
        x+=1
    
    x = 0
    for p in prompt.iteritems():
        namePairs[x][3] = p[1]
        x+=1
        
    return namePairs
    
def noiseEstimation(chosenImage, estTime, Clock, Screen):
    #fix the scale here
    noiseScale = visual.RatingScale(Screen, marker="slider", markerColor="white", choices=None, low=0, high=125,  showAccept=False, tickMarks=[0, 25, 50, 75, 100, 125], 
                                    labels=None, showValue=False, acceptText='Match', size=1.0, textSize=0.0,
                                    scale=None)
    #change image to the default read
    name, ext = os.path.splitext(chosenImage)
    name = os.path.basename(name)
    defImage = name.split('_', 1)[0]
    
    tmp = Image.open(ndir + defImage + ".jpg")
    pic = numpy.array(tmp)
    im = Image.fromarray(pic)
    pres =  visual.ImageStim(Screen, im, pos=(0, 0), size=(8,8))
    num = 0 
    
    Clock.reset()
    while Clock.getTime() < estTime:
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
    if rating:
        rating = noiseScale.getRating()/1000
        ratingRT = noiseScale.getRT()
        choiceHistory = noiseScale.getHistory()
    else:
        rating = 'NaN'
        ratingRT = 'Nan'
    return((rating, ratingRT))

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
    #add an escape character to 
    event.globalKeys.add(key='escape',func=core.quit)
    
    #Collect participant information
    participant, sessNum, counterBalance, presTime, waitTime, estTime = simpleInputScreen()
    presTime = float(presTime)
    waitTime = float(waitTime)
    estTime = float(estTime)

    #make a dictionary to appease the file writing gods
    expInfo = {
    'Participant': participant, 
    'sessNum': sessNum,
    'presTime': presTime,
    'counterBalance': counterBalance,
    'waitTime': waitTime,
    'estTime':estTime}
    
    print("beginning file read")
    #492 pairs for a true 40 minutes and 82 of each permutation, 480 is current versions 468
    
    imageFile = "./lists/" + participant + "imageFile"
    
    makeImageFile(dir, imageFile, 4, stimNumTraining, 1)
    #makeImageFile(dir, imageFile, 4, stimNumSunnybrook, 1)
    #makeImageFile(dir, imageFile, 4, stimNumUndergrad, 1)
    
    #cueTime is the time it takes to cue attention
    cueTime = .200
    #global variables for break
    breakNum = 5
    breakTime = 60
    
    totTrialTime = 1 + float(cueTime) + float(presTime) + float(waitTime)
    
    #print(totTrialTime)
    #print(2.5)
    #Initialize the screen object
    Screen = visual.Window(size=(1920, 1080), monitor='defaultMonitor', fullscr=True, units = "deg")
    
    fx = visual.TextStim(Screen, text="+")
    TopImage = visual.ImageStim(Screen, pos=(0, 6))
    BottomImage = visual.ImageStim(Screen, pos=(0, -6))
    #create a clock object in order to time and report reaction times
    Clock = core.Clock()
    
    #collect stimuli and make a 2d array to be passed to the files
    stim = getImagesfromFile(dir, imageFile+ sessNum +".csv")
    dataFile = participant + version + "_" + sessNum + "_data"
    random.shuffle(stim)
    breaknote = int(len(stim) / breakNum)
    
    #Experiment handler
    expData = data.ExperimentHandler(name=expInfo["Participant"], extraInfo=expInfo, version=version, dataFileName = dataFile + "backup")

    #screen which is drawn until keystrokes indicate participant is ready
    promptScreen(Screen, Clock)
    
    expClock = core.Clock() # won't reset
    trialClock = core.Clock() # will reset at the beginning of each trial
    respClock = core.Clock() # will reset when response time begins
    breakClock = core.Clock() #resets on breaks
    
    for i in range(len(stim)):
        #begin new trial
        #breakHandling
        if i%breaknote == 0 and i != 0:
            breakClock.reset()
            while breakClock.getTime() < breakTime:
                visual.TextStim(Screen, text="break",pos=(0, 4)).draw()
                visual.TextStim(Screen, text = int(60-breakClock.getTime())).draw()
                Screen.flip()
                core.wait(.001)
                #clear the screen before going back 
            Screen.flip()
            
        #begin the trial
        trialClock.reset()
        
        tStim = stim[i][0]
        bStim = stim[i][1]
        cue = stim[i][2]
        prompt = stim[i][3]
        
        expData.addData("trial", i)
        
        
        result = ChoiceConfidenceTrial(fx, TopImage, BottomImage, cue, prompt,
                                        respClock, trialClock, Screen, tStim, bStim, 
                                        float(presTime), float(waitTime))
        
        if prompt == 1: #bottom image
            chosenImage = bStim
        else:
            chosenImage = tStim
        
        while trialClock.getTime() < totTrialTime:
            core.wait(0.001)
            
        noiseest = noiseEstimation(chosenImage, estTime, respClock, Screen)
            
        while trialClock.getTime() < totTrialTime + estTime:
            core.wait(0.001)
            
            
        conf = confidencePrompt(fx, Screen, respClock, trialClock, float(waitTime), counterBalance)
        
        while trialClock.getTime() < totTrialTime + estTime + waitTime:
            core.wait(0.001)
        
        expData.addData("tStim", os.path.basename(tStim))
        expData.addData("bStim", os.path.basename(bStim))
        expData.addData("cue", cue)
        expData.addData("prompt", prompt)
        
        #handling empty results
        if result:
            expData.addData("fchoice", result[0][0])
            expData.addData("fcRT", result[0][1])  # add the data to our set
        else:
            expData.addData("fchoice", 'NaN')
            expData.addData("fcRT", 'NaN')
            
        if noiseest:
            expData.addData("est", noiseest[0])
            expData.addData("estRT", noiseest[1])  # add the data to our set
        else:
            expData.addData("fchoice", 'NaN')
            expData.addData("fcRT", 'NaN')
            
        if conf:
            expData.addData("conf", conf[0][0])
            expData.addData("confRT", conf[0][1])
        
        else:
            expData.addData("conf", 'NaN')
            expData.addData("confRT", 'NaN')
            
        
        print(trialClock.getTime()) # 6.1 seconds per trial
        while trialClock.getTime() < totTrialTime + estTime + waitTime + 0.25:
            core.wait(0.001)
        expData.nextEntry()
        #manage data in loop or outside. Write to a file with participant name generated by the participant handling file
            
    expData.saveAsWideText(dataFile, delim=',', appendFile=True)
        
    msg = visual.TextStim(Screen, text="Thank you! \n The experiment is now complete.")
    msg.draw()
    Screen.flip
    core.wait(5,5)
    
    #cleanup cleanup
    Screen.close()
    #everybody clap your hands
    core.quit()

if __name__ == "__main__":
    main()
    
