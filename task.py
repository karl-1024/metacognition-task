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

#sets up two squares 
#radius of square = 200 --> square is 141 x 141 pixels 
square_left = visual.Polygon(win, edges = 4, radius = 200, fillColor = 'black',  pos =(-200,0), ori = 45) 
square_right = visual.Polygon(win, edges = 4, radius = 200, fillColor = 'black', pos =(200,0), ori = 45)

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
    
def flicker_dots(leftDots, rightDots):
    #sets up dots 
    dots_left = DotStim(win, nDots = leftDots, fieldPos = (-200,0), 
                        fieldSize = (250,250), fieldShape = 'square', 
                        dotSize = 3.0) 
    dots_right = DotStim(win, nDots = rightDots, fieldPos = (200,0), 
                        fieldSize = (250,250), fieldShape = 'square', 
                        dotSize = 3.0) 
    
    dots_left.draw()
    dots_right.draw()
    
    
    
def display_evidence(lDots, rDots): 
    #displays squares & dots
    for i in range(5):
        square_left.draw()
        square_right.draw()
        flicker_dots(lDots, rDots) 
        win.flip() 
        core.wait(0.15)
    
    #dots disappear, makes decision (infinite wait time) 
    square_left.draw()
    square_right.draw() 
    win.flip()

def response():
    #waits for response 
    response = event.waitKeys(keyList = ['w','e'])
    if response: 
        response_key = response[0][0]
        decision = "None"
        #highlights the chosen square cyan 
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
        square_left.lineColor = "black"
        square_right.lineColor = "black" 
        
        return response_key, decision

def display_rating():
    #9 confidence ticks
    confidence_ticks = 9
    ticks = list(range(confidence_ticks))
    labels = ["0%", "50%", "100%"] 
    confidence_rating = Slider(win, ticks = ticks, labels = labels, 
                                font = "Open Sans", granularity = 1, 
                                style = "slider") 
    #waits for confidence_rating response 
    while confidence_rating.getRating() is None: 
        confidence_rating.draw() 
        win.flip()

    print(confidence_rating.getRating())         
    
       

    
display_instructions()   
for i in range(1): 
    left_dots = 0 
    right_dots = 0 
    display_fixation() 
    display_evidence(100,100)
    key_pressed, decision = response() 
    display_rating()
    data.loc[len(data)] = [left_dots, right_dots, key_pressed, decision, 0] 
