import task 
import math 
from psychopy import gui, visual, core, event 
from psychopy.visual.dot import DotStim 
from psychopy.visual.slider import Slider 
import random 
import pandas as pd 
import numpy as np 

#essentials 
win = visual.Window(size=(1920,1080), color='grey', units='pix')
square_left = visual.Polygon(win, edges = 4, radius = 200, fillColor = 'black',  pos =(-200,0), ori = 45) 
square_right = visual.Polygon(win, edges = 4, radius = 200, fillColor = 'black', pos =(200,0), ori = 45)
measurements = ["trial_num", "dot_difference", "num_dots_more", "key_pressed", 
                "decision", "correct_answer", "correctness", "staircase_dir", "boosted"] 
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
    return math.exp(log_diff)
    


#calibration data essentials 
correct = []
consecutive_correct = 0 
dot_difference = 300
less_dots = 313
trialNum = 0
log_dot_change = 0.1 
difficulty = "up" 
boosted_trials = 0
max_boosted_trials = 50
b_val = 0.41 #50/120, should be relatively equally interweaved 


#experiment + staircase decision mechanism 
while trialNum < 70 or boosted_trials < max_boosted_trials: 
    
    boosted = False 
    trial_data = []
    #after 20 "burn-in" staircase steps 
    #if under 50 boosted trials and 30% chance 
    if (trialNum >= 20 and boosted_trials < max_boosted_trials and random.random() < b_val or 
        trialNum >= 70 ):
        boosted = True 
        #multiply by 1.3 in log space 
        boosted_dot_difference = math.floor(math.exp(math.log(dot_difference) * 1.3))
        trial = display_calibration_dots(less_dots, less_dots + boosted_dot_difference) 
        boosted_trials += 1 
        trial_data.append(trialNum)
        trial_data.append(boosted_dot_difference) 
        trial_data.append(less_dots + boosted_dot_difference) 
        print("boosted")
    else: 
        boosted = False 
        #if not boosted
        trial = display_calibration_dots(less_dots, less_dots + dot_difference)
        trial_correctness = trial[3]
        trial_data.append(trialNum)
        trial_data.append(dot_difference) 
        trial_data.append(less_dots + boosted_dot_difference) 
        
        #adds to consecutive_correct if trial is correct
        if trial_correctness: 
            consecutive_correct += 1
        else: 
            consecutive_correct = 0
        
        #staircase: if last two were correct, then makes it harder
        if consecutive_correct >= 2: 
            dot_difference = math.floor(staircase(True, dot_difference, log_dot_change))
            difficulty = "up"
        #else makes it easier 
        elif consecutive_correct == 0: 
            dot_difference = math.floor(staircase(False, dot_difference, log_dot_change ))
            difficulty = "down" 
            
        trialNum += 1 
            
    
    
    
    trial_data.extend(trial) 
    trial_data.append(difficulty) 
    trial_data.append(boosted) 
    data.loc[len(data)] = trial_data 
    
individual_dot_diff = data.iloc[45:69, data.columns.get_loc('dot_difference')] 

data.to_excel(f"{subject_id}_calibration_data.xlsx") 



    
    
    

    
