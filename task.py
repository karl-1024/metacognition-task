from psychopy import gui, visual, core, event 
from psychopy.visual.dot import DotStim 
from psychopy.visual.slider import Slider 
import random 
import pandas as pd 
import numpy as np 

#subject id
info = {'Subject ID (type manually):': ''}
dlg = gui.DlgFromDict(dictionary=info, title='Experimenter Input')
if dlg.OK:
    subject_id = info['Subject ID (type manually):']
else:
    core.quit()
    
#essentials 
experiment_clock = core.Clock()
win = visual.Window(size=(800,600), color='grey', units='pix')
measurements = ["left_dots", "right_dots", "key_pressed", "decision", "correctness"] #add decision time later? 
data = pd.DataFrame(columns = measurements) 

#instructions 
def display_instructions(): 
    instruction_text = ("something blah blah blah")
    instructions = visual.TextStim(win, text = instruction_text) 
    instructions.draw()
    win.flip()
    enter_key = event.waitKeys(keyList = ['return']) 
    
#1000 ms fixation
def display_fixation(): 
    fixation_cross = visual.TextStim(win, text='+', height=40, color='black')
    fixation_cross.draw()
    win.flip()
    core.wait(1.0)
    
    
def display_evidence(leftDots, rightDots): 
    #sets up two squares 
    square_left = visual.Polygon(win, edges = 4, radius = 200, fillColor = 'black',  pos =(-200,0), ori = 45) 
    square_right = visual.Polygon(win, edges = 4, radius = 200, fillColor = 'black', pos =(200,0), ori = 45)

    #sets up dots 
    dots_left = DotStim(win, nDots = leftDots, fieldPos = (-200,0), 
                        fieldSize = (250,250), fieldShape = 'square', 
                        dotSize = 3.0) 
    dots_right = DotStim(win, nDots = rightDots, fieldPos = (200,0), 
                        fieldSize = (250,250), fieldShape = 'square', 
                        dotSize = 3.0) 

    #displays squares & dots
    square_left.draw()
    square_right.draw()
    dots_left.draw()
    dots_right.draw() 
    win.flip() 
    core.wait(0.75)
    
    #dots disappear, makes decision (infinite wait time) 
    square_left.draw()
    square_right.draw() 
    win.flip()
    #waits for response 
    response = event.waitKeys(keyList = ['w','e'])
    if response: 
        response_key = response[0][0]
        decision = "None"
        if response_key == 'w':
            square_left.lineColor = "cyan"
            square_left.draw() 
            decision = "Left" 
        else: 
            square_right.lineColor = "cyan"
            square_right.draw() 
            decision = "Right" 
        win.flip()
        core.wait(0.5)

def display_rating():
    confidence_ticks = 7
    ticks = list(range(confidence_ticks))
    labels = ["1", "4", "7"] 
    confidence_rating = Slider(win, ticks = ticks, labels = labels, font = "Open Sans") 
  
    confidence_rating.draw() 
    win.flip()
    core.wait(5) 
    confidence_rating.getRating()           
  
       

    
    

display_instructions() 
print(win.getActualFrameRate())
display_fixation() 
display_evidence(100,100)
display_rating()
