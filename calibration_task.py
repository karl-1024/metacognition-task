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
measurements = ["trial", "trial_num", "dot_difference", "num_dots_more", "key_pressed", 
                "decision", "correct_answer", "correctness", "staircase_dir", "boosted"] 
data = pd.DataFrame(columns = measurements) 

#subject id pop up box 
info = {'Subject ID (type manually):': ''}
dlg = gui.DlgFromDict(dictionary=info, title='Experimenter Input')
if dlg.OK:
    subject_id = info['Subject ID (type manually):']
else:
    core.quit()

#instructions 
def display_instructions(): 
    instruction_text = ("在這個遊戲中，您將看到兩個方塊逐一出現。\n\n"
                        "方塊內會有許多一閃一閃的點點。\n\n"
                        "您的任務是選擇含比較多點點的方塊。\n\n"
                        "儘量快速和準確地回應。\n\n"
                        "回應鍵如下:\n\n"
                        "w = 左邊方塊\n\n"
                        "e = 右邊方塊\n\n"
                        "選擇之後，方塊邊的顏色會改變，顯示您的選擇的對錯。\n\n"
                        "綠色代表您的選擇正確，則紅色代表選擇錯誤。\n\n"
                        "按 'Enter' 開始，一旦您理解了規則。")
    instructions = visual.TextStim(win, text = instruction_text) 
    instructions.draw()
    win.flip()
    enter_key = event.waitKeys(keyList = ['return'])
    
#displays flickering dots & squares (150 x 5 = 750 ms) 
def display_evidence(lDots, rDots): 
    for i in range(5):
        #draws flickering dots, squares 
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


#single calibration trial + wait 
def display_calibration_dots(dots_count_one, dots_count_two): 
    coinFlip = random.randint(0,1)
    if coinFlip == 0: #chooses where to put dots_count_one (313 dots) and other square
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
    
    #displays dots
    display_evidence(lDots, rDots)
    
    
    #waits for response 
    response = event.waitKeys(keyList = ['w','e'])
    if response: 
        response_key = response[0]
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
    #returns key pressed, corresponding square, correct square, correctness 
    return [response_key, decision, correct_answer, correctness] 

#for figuring out how much dot difference should be lowered by (on log scale) 
#harder - boolean: if true, then difference is smaller 
#difference - current dot difference 
#amount of log change - 0.1 roughly is 10%, etc
def staircase(harder, difference, step): 
    log_diff = math.log(difference) 
    if harder: 
        #ensures dot diff will be at least 1
        log_diff = max(1, log_diff - step)
    else: 
        log_diff = max(1, log_diff + step)
        #return new dot_difference, should be ~10% less 
    print("non-rounded dot difference: " + str(math.exp(log_diff)))
    return math.exp(log_diff)
    


#calibration data essentials 
trialCount = 0
consecutive_correct = 0 #amount of consecutive answers correct 
dot_difference = 300 #difference between square with less dots and square with more dots
less_dots = 313 #amount of dots in the square with less dots 
trialNum = 0
log_dot_change = 0.1 #staircase diff in logarithmic space. roughly translates to ~10%
difficulty = "up" #up means harder, down means easier
boosted_trials = 0 #50 interweaved boosted trials. 
max_boosted_trials = 50 
b_val = 0.41 #50/120, should be relatively equally interweaved 


#experiment + staircase decision mechanism 
while trialNum < 70 or boosted_trials < max_boosted_trials: 
    trialCount += 1
    boosted = False 
    trial_data = []
    trial_data.append(trialCount) 
    #after 20 "burn-in" staircase steps 
    #if under 50 boosted trials and 30% chance 
    if (trialNum >= 20 and boosted_trials < max_boosted_trials and random.random() < b_val or 
        trialNum >= 70 ):
        boosted = True 
        #multiply by 1.3 in log space 
        boosted_dot_difference = int(round(math.exp(math.log(dot_difference) * 1.3)))
        trial = display_calibration_dots(less_dots, less_dots + boosted_dot_difference) 
        boosted_trials += 1 
        trial_data.append(trialNum)
        trial_data.append(boosted_dot_difference) 
        trial_data.append(less_dots + boosted_dot_difference) 
        
    else: 
        boosted = False 
        #if not boosted
        trial = display_calibration_dots(less_dots, less_dots + dot_difference)
        trial_correctness = trial[3]
        trial_data.append(trialNum)
        trial_data.append(dot_difference) 
        trial_data.append(less_dots + dot_difference) 
        
        #adds to consecutive_correct if trial is correct
        if trial_correctness: 
            consecutive_correct += 1
        else: 
            consecutive_correct = 0
        
        #staircase: if last two were correct, then makes it harder
        if consecutive_correct >= 2: 
            dot_difference = int(round((staircase(True, dot_difference, log_dot_change))))
            difficulty = "up"
        #else makes it easier 
        elif consecutive_correct == 0: 
            dot_difference = int(round((staircase(False, dot_difference, log_dot_change ))))
            difficulty = "down" 
            
        trialNum += 1 
            
    
    
    #attaches data onto trial_data then onto dataframe 
    
    trial_data.extend(trial) 
    trial_data.append(difficulty) 
    trial_data.append(boosted) 
    data.loc[len(data)] = trial_data 
    
individual_dot_diff = data.iloc[45:69, data.columns.get_loc('dot_difference')] 

#final data processing 
non_boosted_data = data[data["boosted"] == False]
calibrated_dot_diff_data = non_boosted_data.iloc[45:69, non_boosted_data.columns.get_loc('dot_difference')] 
calibrated_dot_diff = sum(calibrated_dot_diff_data) / 25
print("calibrated dot difference for trial: " + str(calibrated_dot_diff))
data.to_excel(f"{subject_id}_calibration_data.xlsx") 



    
    
    

    
