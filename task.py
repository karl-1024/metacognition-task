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

#dot difference
dot_info = {'Dot Difference (type manually):': ''}
dlg = gui.DlgFromDict(dictionary=dot_info, title='Experimenter Input')
if dlg.OK:
    dot_difference = dot_info['Dot Difference (type manually):']
else:
    core.quit()
    
#essentials 
experiment_clock = core.Clock()
win = visual.Window(size=(800,600), color='grey', units='pix')
measurements = ["dot_count_one", "dot_count_two", "key_pressed", "decision", "correct_answer", "correctness", "confidence"] #add decision time later? 
data = pd.DataFrame(columns = measurements) 

#sets up two squares 
#radius of square = 200 --> square is 141 x 141 pixels 
square_left = visual.Polygon(win, edges = 4, radius = 200, fillColor = 'black',  pos =(-200,0), ori = 45) 
square_right = visual.Polygon(win, edges = 4, radius = 200, fillColor = 'black', pos =(200,0), ori = 45)

#instructions 
def display_instructions(): 
    instruction_text = ("如上一個遊戲一樣，您將看到兩個方塊逐一出現。\n\n"
                        "方塊內會有許多一閃一閃的點點。\n\n"
                        "您的任務是選擇含比較多點點的方塊。\n\n"
                        "儘量快速和準確地回應。\n\n"
                        "回應鍵如下:\n\n"
                        "w = 左邊方塊\n\n"
                        "e = 右邊方塊\n\n"
                        "選擇之後，您必須選您對您的選擇的信心。\n\n"
                        "0%代表您對您的選擇毫無信心，而100%代表您非常有信心。\n\n"
                        "按 'Enter' 開始，一旦您理解了規則。")
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
    
    
    #displays squares & dots
    for i in range(5):
        square_left.draw()
        square_right.draw()
        dots_left = DotStim(win, nDots = leftDots, fieldPos = (-200,0), 
                        fieldSize = (250,250), fieldShape = 'square', 
                        dotSize = 3.0) 
        dots_right = DotStim(win, nDots = rightDots, fieldPos = (200,0), 
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
    
    
def display_evidence(dots_count_one, dots_count_two): 
    
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
    flicker_dots(lDots, rDots)
    return correct_answer
    

def response():
    #waits for response 
    response = event.waitKeys(keyList = ['w','e'])
    if response: 
        response_key = response[0]
        decision = "None"
        #highlights the chosen square cyan 
        if response_key == 'w':
            square_left.lineColor = "cyan"
            square_left.draw() 
            decision = "left" 
        else: 
            square_right.lineColor = "cyan"
            square_right.draw() 
            decision = "right" 
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
    slider_text = "請問您對剛剛的決定多有信心?"
    slider_instructions = visual.TextStim(win, text = slider_text, pos = (0.0, 100.0))
    confidence_rating = Slider(win, ticks = ticks, labels = labels, 
                                font = "Open Sans", granularity = 1, 
                                style = "slider") 
    #waits for confidence_rating response 
    while confidence_rating.getRating() is None: 
        slider_instructions.draw()
        confidence_rating.draw() 
        win.flip()

    return confidence_rating.getRating()         
    
       

    
display_instructions()   
for i in range(60): 
    dot_count_one = 313
    dot_count_two = 313 + int(dot_difference)
    display_fixation() 
    correct_answer = display_evidence(dot_count_one, dot_count_two)
    key_pressed, decision = response() 
    confidence = display_rating()
    correctness = False 
    if decision == correct_answer:
        correctness = True 
    data.loc[len(data)] = [dot_count_one, dot_count_two, key_pressed, decision, 
                            correct_answer, correctness, confidence] 
data.to_excel(f"{subject_id}_metacognition_data.xlsx") 
