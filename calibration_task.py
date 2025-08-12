import task 
import math 
from psychopy import gui, visual, core, event 
from psychopy.visual.dot import DotStim 
from psychopy.visual.slider import Slider 
import random 
import pandas as pd 
import numpy as np 

#essentials 
win = visual.Window(size=(800,600), color='grey', units='pix')
square_left = visual.Polygon(win, edges = 4, radius = 200, fillColor = 'black',  pos =(-200,0), ori = 45) 
square_right = visual.Polygon(win, edges = 4, radius = 200, fillColor = 'black', pos =(200,0), ori = 45)
measurements = ["trial_num", "dot_difference", "num_dots_more", "key_pressed", "decision", "correct_answer", "correctness", "staircase_dir"] 
data = pd.DataFrame(columns = measurements) 

info = {'Subject ID (type manually):': ''}
dlg = gui.DlgFromDict(dictionary=info, title='Experimenter Input')
if dlg.OK:
    subject_id = info['Subject ID (type manually):']
else:
    core.quit()

def display_evidence(lDots, rDots): 
    
    for i in range(5):
        square_left.draw()
        square_right.draw()
        dots_left = DotStim(win, nDots = lDots, fieldPos = (-200,0), 
                        fieldSize = (250,250), fieldShape = 'square', 
                        dotSize = 3.0) 
        dots_right = DotStim(win, nDots = rDots, fieldPos = (200,0), 
                        fieldSize = (250,250), fieldShape = 'square', 
                        dotSize = 3.0) 
    
        dots_left.draw()
        dots_right.draw()
        win.flip() 
        core.wait(0.15)
    
    #dots disappear, makes decision (infinite wait time) 
    square_left.draw()
    square_right.draw() 
    win.flip()


def display_calibration_dots(dots_count_one, dots_count_two): 
    coinFlip = random.randint(0,1)
    if coinFlip == 0: 
        lDots = dots_count_one 
        rDots = dots_count_two 
    else: 
        lDots = dots_count_two 
        rDots = dots_count_one 
    square_left.lineColor = "black"
    square_right.lineColor = "black"
    #sets up correct answer 
    correct_answer = "None" 
    correctness = False 
    if lDots > rDots: 
        correct_answer = "left" 
    else: 
        correct_answer = "right" 
    
    display_evidence(lDots, rDots)
    
    
    #waits for response 
    response = event.waitKeys(keyList = ['w','e'])
    if response: 
        response_key = response[0][0]
        decision = "None"
        if response_key == 'w':
            decision = "left" 
            if decision == correct_answer: 
                correctness = True 
                square_left.lineColor = "lightgreen"
            else: 
                square_left.lineColor = "red" 
        else: 
            decision = "right" 
            if decision == correct_answer: 
                correctness = True 
                square_right.lineColor = "lightgreen"
            else: 
                square_right.lineColor = "red"
            
        square_left.draw()
        square_right.draw() 
        win.flip()
        core.wait(0.5)
    
    return [response_key, decision, correct_answer, correctness] 

#for figuring out how much dot difference should be lowered by (on log scale) 
#harder - boolean: if true, then difference is smaller 
#difference - current dot difference 
#amount of log change - 0.1 roughly is 10%, etc
def staircase(harder, difference, step): 
    log_diff = math.log(difference) 
    if harder: 
        log_diff -= step
    else: 
        log_diff += step
        #return new dot_difference, should be ~10% less 
    return math.floor(math.exp(log_diff))
    



#calibration data essentials 
correct = []
consecutive_correct = 0 
dot_difference = 300
less_dots = 313
trialNum = 0
log_dot_change = 0.1 
difficulty = "up" 

#experiment + staircase decision mechanism 
while trialNum < 70: #change later
    
    trial_data = []
    trial = display_calibration_dots(less_dots, less_dots + dot_difference) 
    trial_correctness = trial[3]
    if trial_correctness: 
        consecutive_correct += 1
    else: 
        consecutive_correct = 0
    trialNum += 1 
    
    if consecutive_correct >= 2: 
        dot_difference = staircase(True, dot_difference, log_dot_change)
        difficulty = "up"
    elif consecutive_correct == 0: 
        dot_difference = staircase(False, dot_difference, log_dot_change)
        difficulty = "down" 
    trial_data.append(trialNum) 
    trial_data.append(dot_difference) 
    trial_data.append(less_dots + dot_difference) 
    trial_data.extend(trial) 
    trial_data.append(difficulty) 
    data.loc[len(data)] = trial_data 

data.to_excel(f"{subject_id}_calibration_data.xlsx") 


    
    
    

    
