from psychopy import data, gui
from psychopy import visual, core, event
from psychopy.visual import ShapeStim 


#set the directory from the images will be retrieved
dir = ""
#file in reference to cwd that the stimuli are stored in
stimFile = ""

imageFile = ""


version = ''

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
        return(info)
    else:
        print('User Cancelled')
        return False


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
    for j in range(percCons)
        index = random.random(0, len(randArr))
        out[randArr.pop(index)][2] = 2
    
    #fill the reliable
    for j in range(percRel)
        index = random.random(0, len(randArr))
        out[randArr.pop(index)][2] = 1
        
    #fill the remainder
    for i in randArr
        out[i][2] = 0
    
def getClickedImage(Screen, Mouse):
    """get clicked image gets the co-ordinates of the mouse on click and returns a number corresponding to the objects. """
    cords = Mouse.getPos()
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
            
            
            

#===========================================================================================================================
#this is the beginning of the main program, Which actually runs the participant
#===========================================================================================================================

def main():
    
    #Screen object to instantiate
    Screen = visual.Window(size=(1920, 1080), monitor='defaultMonitor', fullscr=True, units = "deg")
    #mouse event
    event.Mouse(vivible = True, newPos = (0,0), win = Screen)
    return None 
    
    
if __name__ == "__main__":
    main()
    
