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


def tagImages(nameFile, percCons, percRel):
    """tagImages takes a file of images (csv) and tags a random number of them with reward status. """
    
    
    
    
def getClickedImage(Screen, Mouse):
    """get clicked image gets the co-ordinates of the mouse on click and returns a number corresponding to the objects. """
    
    cords = Mouse.getPos()
    
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
    
