##### house-visiting task (code revision on-going) #####


# Preliminaries ---------------------------------------------------------------

# Import modules
import os
import csv
import datetime
from psychopy import prefs
prefs.hardware['audioLib'] = ['pygame']
from psychopy import gui, core, visual, event, sound # This may require installation
from psychopy.hardware import keyboard
import sys
from random import shuffle
import pandas as pd
import numpy as np
import itertools
import yaml
from scipy.stats import truncnorm

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


# Set working directory to script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Specify paths in dictionary
path = {}
path = {
    "fractal": "../house_visiting-C/fractal/", # Location of images
    "house": "../house_visiting-C/house/gray_house/", # external house image
    "inside": "../house_visiting-C/inside/", # internal house image
    "inside1": "../house_visiting-C/inside/day_inside", #internal image for each day (context differences)
    "inside2": "../house_visiting-C/inside/night_inside",
    "inside3": "../house_visiting-C/inside/new_inside",
    "winsound": "../house_visiting-C/winsound/winsound.wav", #winning sound
    "win": "../house_visiting-C/win/coins.png", #coin image
    "minus": "../house_visiting-C/lose/minus.png",
    "plus": "../house_visiting-C/win/plus.png",
    "losesound": "../house_visiting-C/losesound/losesound.wav",
    "faces": "../house_visiting-C/faces/",
    "open": "../house_visiting-C/others/open.png",
    "closed": "../house_visiting-C/others/closed.png",
    "inst": "../house_visiting-C/others/inst.png",
    "null": "../house_visiting-C/null/null.png"
}

# Define task versions
task_versions = [
    "Day1",
    "Day2",
    "Day3"
]
condition = [
    'pR', #Retrieval condition with reward
    'mR', #Retrieval condition without reward?: not implemented yet
    'NR'  #No Retrieval condition
]

generalize = [ #stimulus generalization? --> no need for now. Everyone is 'yes'
    'yes',
    'no'
] 

order = [ 
    'ac',
    'ca'
] 

# Initialise task parameter dictionary
param = {
    'session_start': '{:%y%m%d_%H%M%S}'.format(datetime.datetime.now()),
    'version': "unspecified",
    'condition': 'unspecified',
    'generalize': 'unspecified',
    'order': 'unspecified'
}

# Get participant info ---------------------------------------------------------

# Get participant ID
gui_id = gui.Dlg() # create box
gui_id.addField("ID:")
gui_id.show()

if gui_id.OK:
    param["id"] = gui_id.data[0]
else:
    sys.exit("user cancelled")


# Get task version -------------------------------------------------------------

while param["version"] == "unspecified" or param['condition'] =='unspecified':

    gui_task = gui.Dlg() # create box
    gui_task.addField("Task version:", choices=task_versions)
    gui_task.addField('Condition:', choices=condition)
    gui_task.addField('Generalize:', choices=generalize)
    gui_task.addField("Order:", choices=order)
    gui_task.show()

    if gui_task.OK:
        param["version"] = gui_task.data[0]
        param['condition'] = gui_task.data[1]
        param['generalize'] = gui_task.data[2]
        param["order"] = gui_task.data[3]
    else:
        sys.exit("user cancelled")



# Assign rating scale ----------------------------------------------------------

if param["version"] == "Day1": #conditioning

    param["question"] = "아래 이미지는...."
    param["anchors"] = "매우 싫다(0) - 매우 좋다(10)"
    param["choices"] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    param["keys"] = ['0','1', '2', '3', '4', '5','6','7','8','9','10']

elif param["version"] == "Day2": #counterconditioning

    param["question"] = "아래 이미지는...."
    param["anchors"] = "매우 싫다(0) - 매우 좋다(10)"
    param["choices"] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    param["keys"] = ['0','1', '2', '3', '4', '5','6','7','8','9','10']

elif param["version"] == "Day3": #renewal

    param["question"] = "아래 이미지는...."
    param["anchors"] = "매우 싫다(0) - 매우 좋다(10)"
    param["choices"] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    param["keys"] = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

else:

    sys.exit("No rating scale available for task version")


##stimuli initializtion

# List stimuli in directory
all_fractals = os.listdir(path["fractal"])
fractal_list = [s for s in all_fractals if "z" in s]
print(len(fractal_list))

all_faces = os.listdir(path["faces"])
faces_list = [v for v in all_faces if "N" in v] # all neutral faces

# Randomise stimlus order
shuffle(fractal_list)
shuffle(faces_list)
faces_list = faces_list[0:10]

fn_inst = '../house_visiting-C/instructions.yml'
with open(fn_inst, 'r', encoding='utf-8') as f:
    instructions = yaml.load(f, Loader=Loader)

#text for the text functions
text1 = ''

#### global escape ####

event.globalKeys.add(key='escape', func=core.quit, name='shutdown')

####drawer set-up####

class Drawer:

    def __init__(self, window):
        self.window = window

    def draw_spacebar(self, day=1):
        if day==2:
            press_space = visual.ImageStim(
                self.window,
                '../house_visiting-C/others/button-to-proceed.png',
                pos=(0, -400),
                size=(450,90),
                interpolate=True
            )
            press_space.draw()
        elif day==1:
            press_space = visual.ImageStim(
                self.window,
                '../house_visiting-C/others/black_button-to-proceed.png',
                pos=(0, -400),
                size=(450,90),
                interpolate=True
            )
            press_space.draw()

    def draw_text(self, text, opacity=1, wrap=None, pos=(0,0), height=None, day=1):
        if day==1:
            text = visual.TextStim(
                win=self.window,
                text=text,
                font='NanumGothic',
                bold=True,
                pos=pos,
                wrapWidth=wrap,
                height=height,
                opacity=opacity,
                color=(-1,-1,-1)
            )
            text.draw()
        else:
            text = visual.TextStim(
                win=self.window,
                text=text,
                font='NanumGothic',
                bold=True,
                pos=pos,
                wrapWidth=wrap,
                height=height,
                opacity=opacity,
                color=(1,1,1)
            )
            text.draw()

    def draw_image(self, image, size=(500,400), pos=(0,0), opacity=1):
        image = visual.ImageStim(
            win=self.window,
            image=image,
            size=size,
            pos=pos,
            opacity=1
        )
        image.draw()

    def draw_inside(self, inside, day=None, size=(1920,1080), pos=(0,0), opacity=1):
        if day==1:
            inside = visual.ImageStim(
            win=self.window,
            image=path['inside'] + 'day_inside/' + inside,
            size=size,
            pos=pos,
            opacity=opacity
            )
            inside.draw()
        elif day==2:
            inside = visual.ImageStim(
            win=self.window,
            image=path['inside'] + 'night_inside/' + inside,
            size=size,
            pos=pos,
            opacity=opacity
            )
            inside.draw()
        elif day==3:
            inside = visual.ImageStim(
            win=self.window,
            image=path['inside'] + 'new_inside/' + inside,
            size=size,
            pos=pos,
            opacity=opacity
            )
            inside.draw()
        elif day==None:
            inside = visual.ImageStim(
            win=self.window,
            image=path['inside'] + inside,
            size=size,
            pos=pos,
            opacity=opacity
            )
            inside.draw()
            
    
    def draw_outside(self, house, pos=(0,0), opacity=1):
        houseStim = visual.ImageStim(self.window, image = path['house'] + house, size = (550,500), pos = pos, opacity = opacity)
        houseStim.draw()

    def draw_town(self, house_list, opacity=1):
        shuffle(house_list)
        house1 = visual.ImageStim(win=self.window, image = path['house']+house_list[0], size = (250, 200), pos = (-700, 300), opacity = opacity)
        house2 = visual.ImageStim(win=self.window, image = path['house']+house_list[1], size = (250, 200), pos = (0, 300), opacity = opacity)
        house3 = visual.ImageStim(win=self.window, image = path['house']+house_list[2], size = (250, 200), pos = (700, 300), opacity = opacity)
        house4 = visual.ImageStim(win=self.window, image = path['house']+house_list[3], size = (250, 200), pos = (-700, 0), opacity = opacity)
        house5 = visual.ImageStim(win=self.window, image = path['house']+house_list[4], size = (250, 200), pos = (0, 0), opacity = opacity)
        house6 = visual.ImageStim(win=self.window, image = path['house']+house_list[5], size = (250, 200), pos = (700, 0), opacity = opacity)
        house7 = visual.ImageStim(win=self.window, image = path['house']+house_list[6], size = (250, 200), pos = (-700, -300), opacity = opacity)            
        house8 = visual.ImageStim(win=self.window, image = path['house']+house_list[7], size = (250, 200), pos = (0, -300), opacity = opacity)
        house9 = visual.ImageStim(win=self.window, image = path['house']+house_list[8], size = (250, 200), pos = (700, -300), opacity = opacity)
        house1.draw()
        house2.draw()
        house3.draw()
        house4.draw()
        house5.draw()
        house6.draw()
        house7.draw()
        house8.draw()
        house9.draw()



def update_text(text1, text2, day=0):
    if day==2:
        text1.text = text2
        text1.color = (1,1,1)
        return text1
    elif day==1 or day==3:
        text1.text = text2
        text1.color = (-1,-1,-1)
        return text1
    elif day==0:
        text1.text = text2
        return text1


def update_pos(text, position):
    text.pos = position
    return text

def update_opacity(image,op):
    image.opacity = op
    return image

def update_color(win, color):
    win.color = color
    return win

def get_truncated_normal(mean=0, sd=1, low=0, upp=10, n=1):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd).rvs(n)


number = ['1','2','3','4','5','6','7','8','9','0']
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
template_house = ['template.png' for i in range(9)]

##### Task component set-up ####

class Task:
    def __init__(self,window,drawer):
        self.window = window
        win = self.window
        self.drawer = drawer
        self.window=window
        self.plusStim = visual.ImageStim(self.window, image = path['plus'], size = (275,275), pos = (0,-350))
        self.minusStim = visual.ImageStim(self.window, image = path['minus'], size = (275,275), pos = (0,-350))
        self.closed = visual.ImageStim(self.window, image = path['closed'], size = (400,400), pos = (0,0))
        self.opened = visual.ImageStim(self.window, image = path['open'], size = (420,350), pos = (0,0))
        self.instStim = visual.ImageStim(self.window, image = path['inst'], size = (1000,550), pos = (0,-240))
        self.nullStim = visual.ImageStim(self.window, image = path['null'], size = (275,45), pos = (0,-350))
        self.winsoundStim = sound.Sound(path['winsound'])
        self.losesoundStim = sound.Sound(path['losesound'])
        self.ResponseInstruction = visual.TextStim(self.window,
                                    height=55,
                                    pos=(0,400), text = '',
                                    bold=True,
                                    color=(1,1,1))
        self.captured_string = ''
        self.CapturedResponseString = visual.TextStim(self.window, 
                        height = 50,
                        pos=(0, -100), text=self.captured_string,
                        bold=True,
                        anchorHoriz = 'center',
                        color=(1,1,1))  
        self.t=''
        self.text = visual.TextStim(
            self.window,
            self.t,
            font='NanumGothic',
            pos=(0, 0),
            wrapWidth=2000,
            height=50,
            color=(-1,-1,-1))
    
    def instrumental_component(self, step, alphabetornumber, wordStim, captured_string, instruction,
                                insideStim, day, paired_color=None, df1=None):

        ResponseInstruction = update_text(self.ResponseInstruction, instruction)
        CapturedResponseString = self.CapturedResponseString
        subject_response_finished = 0 # only changes when they hit return
        instrumentalClock = core.Clock()
        win = self.window
        drawer = self.drawer

        while subject_response_finished == 0:
            kb = keyboard.Keyboard(waitForStart=True)
            CapturedResponseString=update_text(CapturedResponseString, captured_string)
            drawer.draw_inside(inside=insideStim, day=day)
            ResponseInstruction.draw()
            self.closed.draw()
            wordStim.draw()
            CapturedResponseString.draw()
            win.flip()
            kb.start()
            keys = kb.getKeys(waitRelease=False, clear=True)
            
            if len(captured_string) == 3:
                subject_response_finished = 1
                kb.stop()

            if instrumentalClock.getTime()>1.5:
                subject_response_finished = 1
                kb.stop()
            if keys:
                for alpha in alphabetornumber:
                    if alpha in keys:
                        captured_string += alpha
                        CapturedResponseString=update_text(CapturedResponseString, captured_string)
                        drawer.draw_inside(inside=insideStim, day=day)
                        self.closed.draw()
                        ResponseInstruction.draw()
                        wordStim.draw()
                        CapturedResponseString.draw()
                        win.flip()
                    else:
                        pass
                if 'backspace' in keys:
                    captured_string=captured_string[:-1]
                    CapturedResponseString=update_text(CapturedResponseString, captured_string)
                    drawer.draw_inside(inside=insideStim, day=day)
                    self.closed.draw()
                    ResponseInstruction.draw()
                    wordStim.draw()
                    CapturedResponseString.draw()
                    win.flip()
                else:
                    pass

        if step == 'instruction':
            c=0
            wordstim = wordStim.text

            for letter in captured_string:
                if letter in wordstim:
                    c+=1
                else:
                    pass
            if c == 3:
                instrt=instrumentalClock.getTime()
                if instrt<=1.5:
                    drawer.draw_inside(inside=insideStim, day=day)
                    self.opened.draw()
                    win.flip()
                    core.wait(1)
                else:
                    drawer.draw_inside(inside=insideStim, day=day)
                    self.closed.draw()
                    win.flip()
                    core.wait(1)
            else:
                instrt=instrumentalClock.getTime()
                drawer.draw_inside(inside=insideStim, day=day)
                self.closed.draw()
                win.flip()
                core.wait(1)
            
            instreward = 0

            df1=df1.append(pd.Series({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                            'instrt':instrt, 'instreward':instreward}), ignore_index = True)

        elif step == 'conditioning':
            if paired_color in insideStim:
                instrt=instrumentalClock.getTime()
                print(instrt)

                c=0
                wordstim = wordStim.text

                for letter in captured_string:
                    if letter in wordstim:
                        c+=1
                    else:
                        pass
                if c == 3:
                    if instrt<=2.5:
                        money = round(get_truncated_normal(mean=10, sd=2, low=5, upp=20, n=1)[0]+(2.5-instrt)*5).astype(int)
                        if money == 0:
                            money = 0
                            drawer.draw_inside(inside=insideStim, day=day)
                            self.opened.draw()
                            self.nullStim.draw()
                            win.flip()
                            core.wait(2)
                        else:
                            moneyStim = visual.TextStim(win,
                            height=50,
                            pos=(0,-50), text = ("+%s원" %str(money)),
                            bold=True,
                            colorSpace='rgb255',
                            color=(255,255,255))
                            drawer.draw_inside(inside=insideStim, day=day)
                            self.opened.draw()
                            self.plusStim.draw()
                            moneyStim.draw()
                            win.flip()
                            self.winsoundStim.play()
                            core.wait(2)

                    else:
                        money = 0
                        drawer.draw_inside(inside=insideStim, day=day)
                        self.closed.draw()
                        self.nullStim.draw()
                        win.flip()
                        core.wait(2)
                else:
                    money = 0
                    drawer.draw_inside(inside=insideStim, day=day)
                    self.closed.draw()
                    self.nullStim.draw()
                    win.flip()
                    core.wait(2)

            else:
                c=0
                wordstim = wordStim.text

                for letter in captured_string:
                    if letter in wordstim:
                        c+=1
                    else:
                        pass

                instrt=instrumentalClock.getTime()
                print(instrt)               
                drawer.draw_inside(inside=insideStim, day=day)
                if c==3:
                    if instrt<=2.5:
                        money = round(get_truncated_normal(mean=0, sd=1, low=0, upp=2, n=1)[0]+(2.5-instrt)*1).astype(int)
                        if money == 0:
                            drawer.draw_inside(inside=insideStim, day=day)
                            self.opened.draw()
                            self.nullStim.draw()
                            win.flip()
                            core.wait(2)
                        else:
                            moneyStim = visual.TextStim(win,
                            height=50,
                            pos=(0,-50), text = ("+%s원" %str(money)),
                            bold=True,
                            colorSpace='rgb255',
                            color=(255,255,255))
                            drawer.draw_inside(inside=insideStim, day=day)
                            self.opened.draw()
                            self.plusStim.draw()
                            moneyStim.draw()
                            win.flip()
                            self.winsoundStim.play()
                            core.wait(2)           
                    else:
                        money = 0
                        drawer.draw_inside(inside=insideStim, day=day)
                        self.closed.draw()
                        self.nullStim.draw()
                        win.flip()
                        core.wait(2)
                else:
                    money = 0
                    drawer.draw_inside(inside=insideStim, day=day)
                    self.closed.draw()
                    self.nullStim.draw()
                    win.flip()
                    core.wait(2)

                win.flip()
                core.wait(2)
            
            instreward = money

            df1=df1.append(pd.Series({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                            'instrt':instrt, 'instreward':instreward}), ignore_index = True)

        elif step == 'counterconditioning':
            if paired_color in insideStim:
                instrt=instrumentalClock.getTime()
                print(instrt)

                c=0
                wordstim = wordStim.text

                for letter in captured_string:
                    if letter in wordstim:
                        c+=1
                    else:
                        pass
                
                if c == 3:
                    if instrt<=2:
                        money = np.abs(round(((2-instrt)*5)-get_truncated_normal(mean=10, sd=2, low=5, upp=20, n=1)[0]).astype(int))
                        moneyStim = visual.TextStim(win,
                                    height=50,
                                    pos=(0,-50), text = ("-%s원" %str(money)),
                                    bold=True,
                                    colorSpace='rgb255',
                                    color=(255,255,255))
                        drawer.draw_inside(inside=insideStim, day=day)
                        self.opened.draw()
                        self.minusStim.draw()
                        moneyStim.draw()
                        win.flip()
                        self.losesoundStim.play()
                        core.wait(2) 
                    else:
                        money = round(get_truncated_normal(mean=10, sd=2, low=5, upp=20, n=1)[0]).astype(int)
                        moneyStim = visual.TextStim(win,
                                    height=50,
                                    pos=(0,-50), text = ("-%s원" %str(money)),
                                    bold=True,
                                    colorSpace='rgb255',
                                    color=(255,255,255))
                        drawer.draw_inside(inside=insideStim, day=day)
                        self.closed.draw()
                        self.minusStim.draw()
                        moneyStim.draw()
                        win.flip()
                        self.losesoundStim.play()
                        core.wait(2) 
                else:
                    money = round(get_truncated_normal(mean=10, sd=2, low=5, upp=20, n=1)[0]).astype(int)
                    moneyStim = visual.TextStim(win,
                                height=50,
                                pos=(0,-50), text = ("-%s원" %str(money)),
                                bold=True,
                                colorSpace='rgb255',
                                color=(255,255,255))
                    drawer.draw_inside(inside=insideStim, day=day)
                    self.closed.draw()
                    self.minusStim.draw()
                    moneyStim.draw()
                    win.flip()
                    self.losesoundStim.play()
                    core.wait(2) 

            else:
                instrt=instrumentalClock.getTime()
                print(instrt)

                c=0
                wordstim = wordStim.text

                for letter in captured_string:
                    if letter in wordstim:
                        c+=1
                    else:
                        pass
                
                if c == 3:
                    if instrt<=2:
                        money = np.abs(round(((2-instrt)*1)-get_truncated_normal(mean=0, sd=1, low=0, upp=2, n=1)[0]).astype(int))
                        if money == 0:
                            money = 0
                            drawer.draw_inside(inside=insideStim, day=day)
                            self.closed.draw()
                            win.flip()
                            core.wait(2)
                        else:
                            moneyStim = visual.TextStim(win,
                                        height=50,
                                        pos=(0,-50), text = ("-%s원" %str(money)),
                                        bold=True,
                                        colorSpace='rgb255',
                                        color=(255,255,255))
                            drawer.draw_inside(inside=insideStim, day=day)
                            self.opened.draw()
                            self.minusStim.draw()
                            moneyStim.draw()
                            win.flip()
                            self.losesoundStim.play()
                            core.wait(2) 
                    else:
                        money = round(get_truncated_normal(mean=0, sd=1, low=0, upp=2, n=1)[0]).astype(int)
                        if money == 0:
                                money = 0
                                drawer.draw_inside(inside=insideStim, day=day)
                                self.closed.draw()
                                win.flip()
                                core.wait(2)
                        else:
                            moneyStim = visual.TextStim(win,
                                        height=50,
                                        pos=(0,-50), text = ("-%s원" %str(money)),
                                        bold=True,
                                        colorSpace='rgb255',
                                        color=(255,255,255))
                            drawer.draw_inside(inside=insideStim, day=day)
                            self.closed.draw()
                            self.minusStim.draw()
                            moneyStim.draw()
                            win.flip()
                            self.losesoundStim.play()
                            core.wait(2) 
                else:
                    money = round(get_truncated_normal(mean=0, sd=1, low=0, upp=2, n=1)[0]).astype(int)
                    if money == 0:
                        money = 0
                        drawer.draw_inside(inside=insideStim, day=day)
                        self.closed.draw()
                        win.flip()
                        core.wait(2)
                    else:
                        moneyStim = visual.TextStim(win,
                                    height=50,
                                    pos=(0,-50), text = ("-%s원" %str(money)),
                                    bold=True,
                                    colorSpace='rgb255',
                                    color=(255,255,255))
                        drawer.draw_inside(inside=insideStim, day=day)
                        self.closed.draw()
                        self.minusStim.draw()
                        moneyStim.draw()
                        win.flip()
                        self.losesoundStim.play()
                        core.wait(2) 
            
            instreward = money

            df1=df1.append(pd.Series({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                            'instrt':instrt, 'instreward':instreward}), ignore_index = True)

        return captured_string, df1

#### binary choice component set-up ####

    def binary_choice(self, house_list, paired_color, day, unused=None, renewal_type=None):
        win=self.window
        drawer=self.drawer
        n=0
        while n<4:
            text = update_text(self.text,instructions['binary_task'][n],day=day)
            text.draw()
            if all(self.window.color) == (-1,-1,-1) or day == 1 or renewal_type == 'aba':
                drawer.draw_spacebar(day=1)
            else:
                drawer.draw_spacebar(day=2)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])
            n=n+1

        paired=[]
        unpaired=[]
        for house in house_list:
            if paired_color in house:
                paired.append(house)
            else:
                unpaired.append(house)
        
        if paired_color=='green':
            red=[]
            blue=[]
            for house in unpaired:
                if 'red' in house:
                    red.append(house)
                elif 'blue' in house:
                    blue.append(house)
            unpaired_combination=list(itertools.product(red,blue))
        
        elif paired_color=='red':
            green=[]
            blue=[]
            for house in unpaired:
                if 'green' in house:
                    green.append(house)
                elif 'blue' in house:
                    blue.append(house)
            unpaired_combination=list(itertools.product(green,blue))

        elif paired_color=='blue':
            red=[]
            green=[]
            for house in unpaired:
                if 'red' in house:
                    red.append(house)
                elif 'green' in house:
                    green.append(house)
            unpaired_combination=list(itertools.product(red,green))
        
        combination=list(itertools.product(paired, unpaired))

        for combo in unpaired_combination:
            combination.append(combo)

        print(combination)

        shuffle(combination)
        df2 = pd.DataFrame(columns=['Id', 'Version', 'Condition','house1','house2', 'house1_paired','house2_paired','Choice','RT'])
        choiceclock = core.Clock()

        for l in combination:
            choice = list(l)
            shuffle(choice)
            choiceclock.reset()
            house1 = visual.ImageStim(win, image = path['house'] + choice[0], size = (450,400), pos = (-350,0))
            house2 = visual.ImageStim(win, image = path['house'] + choice[1], size = (450,400), pos = (350,0))
            highlight1 = visual.ImageStim(win, image = '../house_visiting/house/' + 'highlight.png', size = (475,425), pos = (-350,0)) #house1 골랐을 때 후광
            highlight2 = visual.ImageStim(win, image = '../house_visiting/house/' + 'highlight.png', size = (475,425), pos = (350,0)) #house2 골랐을 때 후광
            house1.draw()
            house2.draw()
            win.flip()

            keys = event.waitKeys(keyList = ['f','j'])
                        
            if 'f' in keys:
                highlight1.draw()
                house1.draw()
                house2.draw()
                win.flip()
                if paired_color in choice[0] and paired_color in choice[1]:
                    df2=df2.append({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                    'house1':choice[0], 'house2':choice[1], 'house1_paired':1, 'house2_paired':1, 'Choice':1,'RT':choiceclock.getTime()},
                    ignore_index = True)
                    core.wait(1)
                elif paired_color not in choice[0] and paired_color in choice[1]:
                    df2=df2.append({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                    'house1':choice[0], 'house2':choice[1], 'house1_paired':0, 'house2_paired':1, 'Choice':0,'RT':choiceclock.getTime()},
                    ignore_index = True)
                    core.wait(1)
                elif paired_color in choice[0] and paired_color not in choice[1]:
                    df2=df2.append({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                    'house1':choice[0], 'house2':choice[1], 'house1_paired':1, 'house2_paired':0, 'Choice':1,'RT':choiceclock.getTime()},
                    ignore_index = True)
                    core.wait(1)
                elif paired_color not in choice[0] and paired_color not in choice[1]:
                    df2=df2.append({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                    'house1':choice[0], 'house2':choice[1], 'house1_paired':0, 'house2_paired':0, 'Choice':0,'RT':choiceclock.getTime()},
                    ignore_index = True)
                    core.wait(1)

            elif 'j' in keys:
                highlight2.draw()
                house1.draw()
                house2.draw()
                win.flip()
                if paired_color in choice[0] and paired_color in choice[1]:
                    df2=df2.append({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                    'house1':choice[0], 'house2':choice[1], 'house1_paired':1, 'house2_paired':1, 'Choice':1,'RT':choiceclock.getTime()},
                    ignore_index = True)
                    core.wait(1)
                elif paired_color not in choice[0] and paired_color in choice[1]:
                    df2=df2.append({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                    'house1':choice[0], 'house2':choice[1], 'house1_paired':0, 'house2_paired':1, 'Choice':1,'RT':choiceclock.getTime()},
                    ignore_index = True)
                    core.wait(1)
                elif paired_color in choice[0] and paired_color not in choice[1]:
                    df2=df2.append({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                    'house1':choice[0], 'house2':choice[1], 'house1_paired':1, 'house2_paired':0, 'Choice':0,'RT':choiceclock.getTime()},
                    ignore_index = True)
                    core.wait(1)
                elif paired_color not in choice[0] and paired_color not in choice[1]:
                    df2=df2.append({'Id':param['id'], 'Version':param['version'], 'Condition':param['condition'],
                    'house1':choice[0], 'house2':choice[1], 'house1_paired':0, 'house2_paired':0, 'Choice':0,'RT':choiceclock.getTime()},
                    ignore_index = True)
                    core.wait(1)
        
        print(df2)
        if day==1:
            df2.to_csv("../house_visiting-C/data/"+param["version"]+"/binary/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + '_' + param["session_start"] + "_" + "BinaryChoice" + ".csv",index=False)
        elif day==2:
            for i in range(len(df2)):
                if unused in df2.loc[i,'house1'] or unused in df2.loc[i,'house2']:
                    df2.at[i,"Paired_Unused"] = 1
                else:
                    df2.at[i,"Paired_Unused"] = 0
            df2.to_csv("../house_visiting-C/data/"+param["version"]+"/binary/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + '_' + param["session_start"] + "_" + "BinaryChoice" + ".csv",index=False)
        elif day==3:
            if renewal_type == 'abc':
                for i in range(len(df2)):
                    if unused in df2.loc[i,'house1'] or unused in df2.loc[i,'house2']:
                        df2.at[i,"Paired_Unused"] = 1
                    else:
                        df2.at[i,"Paired_Unused"] = 0
                df2.to_csv("../house_visiting-C/data/"+param["version"]+"/binary/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + '_' + param["session_start"] + "_" + "ABC_BinaryChoice" + ".csv",index=False)
            elif renewal_type == 'aba':
                for i in range(len(df2)):
                    if unused in df2.loc[i,'house1'] or unused in df2.loc[i,'house2']:
                        df2.at[i,"Paired_Unused"] = 1
                    else:
                        df2.at[i,"Paired_Unused"] = 0
                df2.to_csv("../house_visiting-C/data/"+param["version"]+"/binary/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + '_' + param["session_start"] + "_" + "ABA_BinaryChoice" + ".csv",index=False)


#### fractal-liking task 1 set-up ####
    def initial_liking_task(self):
        win=self.window
        drawer=self.drawer
        ratingScale = visual.RatingScale(
            win,
            pos=(0, -250),
            textColor=[-1, -1, -1],
            lineColor=(-1,-1,-1),
            choices=param["choices"],
            respKeys=param["keys"],
            marker='circle',
            markerColor='Black',
            mouseOnly=True
        )

        text = update_text(self.text, instructions['intro'])
        text.draw()
        drawer.draw_spacebar()
        core.wait(1)
        win.flip()
        _=event.waitKeys(keyList=['space'])

        n=0
        while n<3:
            text = update_text(self.text, instructions['fractal_liking'][n])
            if n == 1:
                while ratingScale.noResponse:
                    text = update_pos(text, (0,150))
                    text.draw()
                    ratingScale.draw()
                    win.flip()
                n=n+1
            else:
                text = update_pos(text, (0,0))
                text.draw()
                drawer.draw_spacebar()
                core.wait(1)
                win.flip()
                _=event.waitKeys(keyList=['space'])
                n=n+1

        # Begin loop through stimuli ---------------------------------------------------

        #trial_n = 0
        df = pd.DataFrame(columns=['Id','Version', 'Condition','Fractal','Rating1','rt1','Timestamp'])
        for stimulus in fractal_list:

            #trial_n = trial_n + 1

            # Get image filename
            fractal_fn = path["fractal"] + stimulus

            # Pause for 100ms
            core.wait(0.1)

            # Construct image component
            imgStim = visual.ImageStim(win, image=fractal_fn, size=(400,400))

            # Construct rating scale component below image
            ratingScale = visual.RatingScale(
                win,
                pos=(0, -250),
                textColor=[-1,-1,-1],
                lineColor=(-1,-1,-1),
                choices=param["choices"],
                respKeys=param["keys"],
                marker='circle',
                markerColor='Black',
                mouseOnly=True
            )

            # Draw components and listen for response
            while ratingScale.noResponse:
                drawer.draw_image(image = fractal_fn)
                drawer.draw_text(text=param["question"], opacity=1, pos=(0,400))
                drawer.draw_text(text=param["anchors"], opacity=1, pos=(0,300))
                ratingScale.draw()
                win.flip()

            # Extract response
            rating = ratingScale.getRating()
            decisionTime = ratingScale.getRT()

            # Store relevant information in array - each element goes in a separate
            # column of the session csv file
            df=df.append({'Id':param['id'],
            'Version':param['version'],
            'Condition':param['condition'],
            'Fractal':stimulus,
            'Rating1':rating,
            'rt1':decisionTime,
            'Timestamp':'{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())},
            ignore_index=True)

            # Print trial data to console
            print(param['id'], param['version'], param['condition'], stimulus, rating, decisionTime)

            # End loop through trials
        print(df)

        #calculate mean liking rate
        av_rating=df['Rating1'].mean(axis=0)
        print(av_rating)

        for i in range(len(df)):
            distance = abs(av_rating-df.loc[i,'Rating1'])
            df.loc[i,'Distance'] = distance
            print(distance)
        print(df)

        #pick 3 green fractals
        green_fractal_dict = {}
        for i in range(len(df)):
            if 'green' in df.loc[i,'Fractal']:
                green_fractal_dict[df.loc[i,'Fractal']] = df.loc[i,'Distance']


        green1 = min(green_fractal_dict, key=green_fractal_dict.get)
        del green_fractal_dict[green1]
        green2 = min(green_fractal_dict, key=green_fractal_dict.get)
        del green_fractal_dict[green2]
        green3 = min(green_fractal_dict, key=green_fractal_dict.get)
        del green_fractal_dict[green3]

        print(green1, green2, green3)

        #pick 3 red fractals

        red_fractal_dict = {}
        for i in range(len(df)):
            if 'red' in df.loc[i,'Fractal']:
                red_fractal_dict[df.loc[i,'Fractal']] = df.loc[i,'Distance']


        red1 = min(red_fractal_dict, key=red_fractal_dict.get)
        del red_fractal_dict[red1]
        red2 = min(red_fractal_dict, key=red_fractal_dict.get)
        del red_fractal_dict[red2]
        red3 = min(red_fractal_dict, key=red_fractal_dict.get)
        del red_fractal_dict[red3]

        print(red1, red2, red3)

        #pick 3 blue fractals

        blue_fractal_dict = {}
        for i in range(len(df)):
            if 'blue' in df.loc[i,'Fractal']:
                blue_fractal_dict[df.loc[i,'Fractal']] = df.loc[i,'Distance']


        blue1 = min(blue_fractal_dict, key=blue_fractal_dict.get)
        del blue_fractal_dict[blue1]
        blue2 = min(blue_fractal_dict, key=blue_fractal_dict.get)
        del blue_fractal_dict[blue2]
        blue3 = min(blue_fractal_dict, key=blue_fractal_dict.get)
        del blue_fractal_dict[blue3]

        print(blue1, blue2, blue3)

        #designate CS
        df.set_index('Fractal', inplace=True)
        green_av = (df.at[green1,'Rating1'] + df.at[green2,'Rating1'] + df.at[green3,'Rating1'])/3
        red_av = (df.at[red1,'Rating1'] + df.at[red2,'Rating1'] + df.at[red3,'Rating1'])/3
        blue_av = (df.at[blue1,'Rating1'] + df.at[blue2,'Rating1'] + df.at[blue3,'Rating1'])/3

        print(green_av, red_av, blue_av)

        av = [green_av, red_av, blue_av]

        if min(av) == green_av:
            unpaired_color1 = 'green'
            av.remove(green_av)
            if min(av) == red_av:
                paired_color = 'red'
                unpaired_color2 = 'blue'
            elif min(av) == blue_av:
                paired_color = 'blue'
                unpaired_color2 = 'red'    
        elif min(av) == red_av:
            unpaired_color1 = 'red'
            av.remove(red_av)
            if min(av) == green_av:
                paired_color = 'green'
                unpaired_color2 = 'blue'
            elif min(av) == blue_av:
                paired_color = 'blue'
                unpaired_color2 = 'green' 
        elif min(av) == blue_av:
                unpaired_color1 = 'blue'
                av.remove(blue_av)
                if min(av) == green_av:
                    paired_color = 'green'
                    unpaired_color2 = 'red'
                elif min(av) == red_av:
                    paired_color = 'red'
                    unpaired_color2 = 'green'

        print('unpaired color1:', unpaired_color1)
        print('paired color:', paired_color)
        print('unpaired color2:', unpaired_color2)
        win.flip()

    # shuffle house stimuli
        house_list = [green1, green2, green3, red1, red2, red3, blue1, blue2, blue3]
        shuffle(house_list)
        return(house_list, paired_color, unpaired_color1, unpaired_color2, df)

#### fractal-liking task 2 set-up ####
    def second_liking_task(self, df, day, paired_color, house_list, txt_color=(1,1,1), unused=None, renewal_type=None):
        win=self.window
        drawer=self.drawer
        if day==1 or day==3:
            text=update_text(self.text, instructions['house_liking_task'])
        elif day==2:
            text=update_text(self.text, instructions['house_liking_task'], day=2)
        text.draw()

        if all(self.window.color) == (-1,-1,-1) or day==2 or renewal_type == 'abc':
            drawer.draw_spacebar(day=2)
        else:
            drawer.draw_spacebar(day=1)
        core.wait(1)
        win.flip()
        _=event.waitKeys(keyList=["space"])

        if day==1:
            n=0

            for stimulus in fractal_list:
                fractal_fn = path["fractal"] + stimulus

                # Pause for 100ms
                core.wait(0.1)

                # Construct image component
                imgStim = visual.ImageStim(win, image=fractal_fn, size=(400,400))

                # Construct text component above image
                txtQuestion = visual.TextStim(
                    self.window,
                    text=param["question"],
                    anchorHoriz="center",
                    pos=(0, 400),
                    color=txt_color,
                    bold=True,
                )
                txtAnchor = visual.TextStim(
                    self.window,
                    text=param["anchors"],
                    anchorHoriz="center",
                    pos=(0, 300),
                    color=txt_color,
                    bold=True
                )

                # Construct rating scale component below image
                ratingScale = visual.RatingScale(
                    win,
                    pos=(0, -250),
                    textColor=txt_color,
                    lineColor=txt_color,
                    choices=param["choices"],
                    respKeys=param["keys"],
                    marker='circle',
                    mouseOnly=True,
                    markerColor=txt_color
                )

                # Draw components and listen for response
                while ratingScale.noResponse:

                    imgStim.draw()
                    txtQuestion.draw()
                    txtAnchor.draw()
                    ratingScale.draw()
                    win.flip()

                # Extract response
                rating = ratingScale.getRating()
                decisionTime = ratingScale.getRT()

                # Store relevant information in array - each element goes in a separate
                # column of the session csv file
                df.loc[stimulus,'rating2']=rating
                df.loc[stimulus,'rt2']=decisionTime

                if paired_color in stimulus:
                    df.loc[stimulus,'paired'] = 1
                else:
                    df.loc[stimulus,'paired'] = 0
                
                if stimulus in house_list:
                    df.loc[stimulus,'used'] = 1
                else:
                    df.loc[stimulus,'used'] = 0
                df.loc[stimulus,'index'] = int(n)
                n = n+1
        
        elif day == 2:
            n=0

            for stimulus in fractal_list:
                fractal_fn = path["fractal"] + stimulus

                # Pause for 100ms
                core.wait(0.1)

                # Construct image component
                imgStim = visual.ImageStim(win, image=fractal_fn, size=(400,400))

                # Construct text component above image
                txtQuestion = visual.TextStim(
                    self.window,
                    text=param["question"],
                    anchorHoriz="center",
                    pos=(0, 400),
                    color=txt_color,
                    bold=True,
                )
                txtAnchor = visual.TextStim(
                    self.window,
                    text=param["anchors"],
                    anchorHoriz="center",
                    pos=(0, 300),
                    color=txt_color,
                    bold=True
                )

                # Construct rating scale component below image
                ratingScale = visual.RatingScale(
                    win,
                    pos=(0, -250),
                    textColor=txt_color,
                    lineColor=txt_color,
                    choices=param["choices"],
                    respKeys=param["keys"],
                    marker='circle',
                    mouseOnly=True,
                    markerColor=txt_color
                )

                # Draw components and listen for response
                while ratingScale.noResponse:

                    imgStim.draw()
                    txtQuestion.draw()
                    txtAnchor.draw()
                    ratingScale.draw()
                    win.flip()

                # Extract response
                rating = ratingScale.getRating()
                decisionTime = ratingScale.getRT()

                # Store relevant information in array - each element goes in a separate
                # column of the session csv file
                df.loc[stimulus,'day2_rating']=rating
                df.loc[stimulus,'day2_rt']=decisionTime
                n = n+1

        elif day == 3 and renewal_type == 'aba':

            n=0

            for stimulus in fractal_list:
                fractal_fn = path["fractal"] + stimulus

                # Pause for 100ms
                core.wait(0.1)

                # Construct image component
                imgStim = visual.ImageStim(win, image=fractal_fn, size=(400,400))

                # Construct text component above image
                txtQuestion = visual.TextStim(
                    self.window,
                    text=param["question"],
                    anchorHoriz="center",
                    pos=(0, 400),
                    color=txt_color,
                    bold=True,
                )
                txtAnchor = visual.TextStim(
                    self.window,
                    text=param["anchors"],
                    anchorHoriz="center",
                    pos=(0, 300),
                    color=txt_color,
                    bold=True
                )

                # Construct rating scale component below image
                ratingScale = visual.RatingScale(
                    win,
                    pos=(0, -250),
                    textColor=txt_color,
                    lineColor=txt_color,
                    choices=param["choices"],
                    respKeys=param["keys"],
                    marker='circle',
                    mouseOnly=True,
                    markerColor=txt_color
                )

                # Draw components and listen for response
                while ratingScale.noResponse:

                    imgStim.draw()
                    txtQuestion.draw()
                    txtAnchor.draw()
                    ratingScale.draw()
                    win.flip()

                # Extract response
                rating = ratingScale.getRating()
                decisionTime = ratingScale.getRT()

                # Store relevant information in array - each element goes in a separate
                # column of the session csv file
                df.at[stimulus,'day3_aba_rating']=rating
                df.at[stimulus,'day3_aba_rt']=decisionTime
                n = n+1

        elif day == 3 and renewal_type == 'abc':

            n=0

            for stimulus in fractal_list:
                fractal_fn = path["fractal"] + stimulus

                # Pause for 100ms
                core.wait(0.1)

                # Construct image component
                imgStim = visual.ImageStim(win, image=fractal_fn, size=(400,400))

                # Construct text component above image
                txtQuestion = visual.TextStim(
                    self.window,
                    text=param["question"],
                    anchorHoriz="center",
                    pos=(0, 400),
                    color=txt_color,
                    bold=True,
                )
                txtAnchor = visual.TextStim(
                    self.window,
                    text=param["anchors"],
                    anchorHoriz="center",
                    pos=(0, 300),
                    color=txt_color,
                    bold=True
                )

                # Construct rating scale component below image
                ratingScale = visual.RatingScale(
                    win,
                    pos=(0, -250),
                    textColor=txt_color,
                    lineColor=txt_color,
                    choices=param["choices"],
                    respKeys=param["keys"],
                    marker='circle',
                    mouseOnly=True,
                    markerColor=txt_color
                )

                # Draw components and listen for response
                while ratingScale.noResponse:

                    imgStim.draw()
                    txtQuestion.draw()
                    txtAnchor.draw()
                    ratingScale.draw()
                    win.flip()

                # Extract response
                rating = ratingScale.getRating()
                decisionTime = ratingScale.getRT()

                # Store relevant information in array - each element goes in a separate
                # column of the session csv file
                df.at[stimulus,'day3_abc_rating']=rating
                df.at[stimulus,'day3_abc_rt']=decisionTime
                n = n+1
            # End loop through trials
        print(df)
        if day==1:
            df.to_csv("../house_visiting-C/data/day1/liking/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + "_" + "Liking" + ".csv")
        elif day==2:
            df['Fractal'] = df.index
            df['index'] = df['index'].apply(np.int64)
            df.set_index('index',inplace=True)
            print(df)
            for i in range(len(df)):
                if unused in df.at[i,'Fractal']:
                    df.at[i,"Paired_Unused"] = 1
                else:
                    df.at[i,"Paired_Unused"] = 0
            df.to_csv("../house_visiting-C/data/day2/liking/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + "_" + "Liking" + ".csv")
        elif day==3:
            if renewal_type == 'abc':
                df['Fractal'] = df.index
                print(df)
                df.to_csv("../house_visiting-C/data/day3/liking/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + "_" + "ABC_Liking" + ".csv")
            elif renewal_type == 'aba':
                df['Fractal'] = df.index
                print(df)
                df.to_csv("../house_visiting-C/data/day3/liking/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + "_" + "ABA_Liking" + ".csv")

#### face liking task set-up ####
    def face_liking_task(self, txt_color=(1,1,1), day=1):
        win=self.window
        drawer=self.drawer
        if day==1:
            text = update_text(self.text,instructions['faces_liking_task'], day=1)
        else:
            text = update_text(self.text,instructions['faces_liking_task'], day=2)
        text.draw()
        if all(self.window.color) == (-1,-1,-1):
            drawer.draw_spacebar(day=2)
        else:
            drawer.draw_spacebar(day=1)
        core.wait(1)
        self.window.flip()
        _=event.waitKeys(keyList=["space"])

        for stimulus in faces_list:
            faces_fn = path["faces"] + stimulus

            # Pause for 100ms
            core.wait(0.1)

            # Construct image component
            imgStim = visual.ImageStim(win, image=faces_fn, size=(470,400))

            # Construct text component above image
            txtQuestion = visual.TextStim(
                win,
                text=param["question"],
                anchorHoriz="center",
                pos=(0, 400),
                color=txt_color,
                bold=True,
            )
            txtAnchor = visual.TextStim(
                win,
                text=param["anchors"],
                anchorHoriz="center",
                pos=(0, 300),
                color=txt_color,
                bold=True
            )

            # Construct rating scale component below image
            ratingScale = visual.RatingScale(
                win,
                pos=(0, -250),
                textColor=txt_color,
                lineColor=txt_color,
                choices=param["choices"],
                respKeys=param["keys"],
                marker='circle',
                markerColor=txt_color,
                mouseOnly=True
            )

            # Draw components and listen for response
            while ratingScale.noResponse:

                imgStim.draw()
                txtQuestion.draw()
                txtAnchor.draw()
                ratingScale.draw()
                win.flip()

#### movie set-up ####
    def movie(self):
        win = self.window
        drawer = self.drawer
        movie = visual.MovieStim3(win, '../house_visiting-C/movie/NZ.mp4', size = (1920,1080), opacity=1.0, pos = (0,0))

        #Filler
        text = update_text(self.text,instructions['natural_filler_task'], day=1)
        text.draw()
        core.wait(1)
        win.flip()
        _=event.waitKeys(keyList=["space"])

        ##1
        correct = 0
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=40:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)
        Itext = visual.TextStim(
            win,
            text = instructions['filler'][0],
            height = 40,
            pos = (0,300),
            font = 'NamuGothic',
            bold = True,
            color = (-1,-1,-1)
        )
        Qtext = update_pos(update_text(self.text, instructions['filler'][1], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '2' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        ##2
        movie.opacity=1
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=56:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)

        Qtext = update_pos(update_text(self.text, instructions['filler'][2], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '3' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        #3
        movie.opacity=1
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=84:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)

        Qtext = update_pos(update_text(self.text, instructions['filler'][3], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '4' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        ##4
        movie.opacity=1
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=63:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)

        Qtext = update_pos(update_text(self.text, instructions['filler'][4], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '2' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        ##5
        movie.opacity=1
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=74:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)

        Qtext = update_pos(update_text(self.text, instructions['filler'][5], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '3' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        ##6
        movie.opacity=1
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=62:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)

        Qtext = update_pos(update_text(self.text, instructions['filler'][6], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '3' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        ##7
        movie.opacity=1
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=113:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)

        Qtext = update_pos(update_text(self.text, instructions['filler'][7], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '1' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        ##8
        movie.opacity=1
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=90:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)

        Qtext = update_pos(update_text(self.text, instructions['filler'][8], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '3' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        ##9
        movie.opacity=1
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=62:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)

        Qtext = update_pos(update_text(self.text, instructions['filler'][9], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '2' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        ##10
        movie.opacity=1
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=53:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)

        Qtext = update_pos(update_text(self.text, instructions['filler'][10], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '4' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        ##11
        movie.opacity=1
        movie.play()
        movieClock = core.Clock()
        while movieClock.getTime()<=60:
            movie.draw()
            win.flip()
        movie.pause()
        movie.opacity=0.5
        movie.draw()
        win.flip()
        core.wait(1)

        Qtext = update_pos(update_text(self.text, instructions['filler'][11], day=1), (0,-150))
        Qtime = core.Clock()
        finished = 0

        while finished == 0:
            if Qtime.getTime() <= 10:
                movie.draw()
                Itext.draw()
                Qtext.draw()
                win.flip()
                _=event.waitKeys(keyList=['1','2','3','4'])
                movie.draw()
                win.flip()
                finished = 1
            else:
                finished = 1


        time = Qtime.getTime()
        print('Answeringtime: ', time)

        if time <=10:
            if '2' in _:
                correct = correct + 1
            else:
                pass
        else:
            pass

        print('cumulative_correct: ', correct)

        correct_percent = (correct/11)*100
        print('correct_percent: ', correct_percent)


#### ABA/ABC (counterbalanced?) renewal set-up ####
#### Pavlovian component set-up ####

        ###################################################RUNNER##########################################################

class Runner:
    def __init__(self):
        pass
        
    def day1(self):

        white_win = visual.Window(
            units="pix",
            color=(1, 1, 1),
            allowGUI=False,
            fullscr=True
        )

        drawer1 = Drawer(white_win)
        task = Task(white_win, drawer1)
        win = task.window
        win.mouseVisible=True
        drawer1.draw_text(text=instructions['intro'], pos = (0,0), height = 50, wrap=2000)
        drawer1.draw_spacebar()
        core.wait(1)
        task.window.flip()
        _=event.waitKeys(keyList=['space'])

        house_list, paired_color, unpaired_color1, unpaired_color2, df = task.initial_liking_task()
        print(house_list, paired_color, unpaired_color1, unpaired_color2, df)
        win.mouseVisible=False

        n=0
        while n<8:
            if n == 2:
                drawer1.draw_town(house_list=template_house, opacity = .5)
                drawer1.draw_text(text=instructions['house_visiting'][n], pos = (0,0), height = 50, wrap=2000)
                drawer1.draw_spacebar(day=1)
                core.wait(1)
                task.window.flip()
                _=event.waitKeys(keyList=["space"])
                n=n+1
            elif n == 3:
                plusStim = update_pos(task.plusStim,(-200,-200))
                minusStim = update_pos(task.minusStim,(200,-200))
                drawer1.draw_inside(inside='template.png', size=(1920,1080), pos=(0,0), opacity=0.5, day=None)
                drawer1.draw_text(text=instructions['house_visiting'][n], pos = (0,200), height = 50, wrap=2000)
                task.plusStim.draw()
                task.minusStim.draw()
                drawer1.draw_spacebar(day=1)
                core.wait(1)
                task.window.flip()
                _=event.waitKeys(keyList=["space"])
                n=n+1
            elif n ==5:
                drawer1.draw_inside(inside='template.png', size=(1920,1080), pos=(0,0), opacity=0.5, day=None)
                drawer1.draw_text(text=instructions['house_visiting'][n], pos = (0,250), height = 50, wrap=2000)
                task.instStim.draw()
                core.wait(1)
                task.window.flip()
                _=event.waitKeys(keyList=["space"])
                n=n+1
            else:
                drawer1.draw_text(text=instructions['house_visiting'][n], pos = (0,0), height = 50, wrap=2000)
                drawer1.draw_spacebar(day=1)
                core.wait(1)
                task.window.flip()
                _=event.waitKeys(keyList=["space"])
                n=n+1

        # practice trial with no background
        df2 = pd.DataFrame(columns=['Id', 'Version', 'Condition','instrt', 'instreward'])
        drawer1.draw_town(house_list=template_house, opacity = 1)
        task.window.flip()
        core.wait(1)

        n=0
        while n<5:
            houseStim = visual.ImageStim(task.window, image = path['house'] + 'template.png', size = (550,500), pos = (0,0))
            insideStim = visual.ImageStim(task.window, image = path['inside'] + 'template.png', size = (1920,1080), pos = (0,0))
            instruction = visual.TextStim(task.window, 
                            height = 40,
                            pos=(0, 320), text=instructions['house_visiting'][8],
                            wrapWidth=2000,
                            bold=True,
                            anchorHoriz = 'center',
                            color=(-1,-1,-1))
            houseStim.draw()
            instruction.draw()
            task.window.flip()
            event.waitKeys(keyList=['space'])
            insideStim.draw()
            task.window.flip()
            core.wait(2)

            letter1 = number[np.random.randint(0,9)]
            letter2 = number[np.random.randint(0,9)]
            letter3 = number[np.random.randint(0,9)]

            wordStim = visual.TextStim(task.window,
                            height=50,
                            pos=(0,-50), text = letter1+letter2+letter3,
                            bold=True,
                            anchorHoriz = 'center',
                            colorSpace='rgb255',
                            color=(255,255,255))

            captured_string = ''

            instruction = '빨리 누르세요!'

            captured_string,df2 = task.instrumental_component(step='instruction', wordStim=wordStim, captured_string=captured_string, instruction = instruction, paired_color=paired_color,
                                                                insideStim='template.png', alphabetornumber=number, day=None, df1 = df2)
            
            n=n+1

            

        #conditioning stage instructions

        drawer1.draw_text(text=instructions['house_visiting'][10], pos = (0,0), height = 50, wrap=2000) #instruction regarding regularities in task
        drawer1.draw_spacebar(day=1)
        core.wait(1)
        task.window.flip()
        _=event.waitKeys(keyList=["space"])

        drawer1.draw_text(text=instructions['house_visiting'][9], pos = (0,0), height = 50, wrap=2000)
        drawer1.draw_spacebar(day=1)
        core.wait(1)
        task.window.flip()
        _=event.waitKeys(keyList=['space'])

        # Day 1 house-visit (reward for paired color, none for unpaired color)
        # independently construct image components for each house
        
        drawer1.draw_town(house_list=house_list, opacity = 1)

        task.window.flip()
        core.wait(1)
        
        clock1=core.Clock()

        shuffle(house_list)
        print(house_list)

        #20 TOUR BLOCKS
        df1 = pd.DataFrame(columns=['Id', 'Version', 'Condition','instrt', 'instreward'])
        block=0
        while block<20:
            n=0
            while n<9:
                insideStim = visual.ImageStim(task.window, image = path['inside'] + 'day_inside/' + house_list[n], size = (1920,1080), pos = (0,0))
                winsoundStim = sound.Sound(path['winsound'])
                
                drawer1.draw_image(image=path['house'] + house_list[n], size = (550,500), pos = (0,0))
                task.window.flip()
                clock1.reset(newT=0.0)
                event.waitKeys(keyList=['space'])
                rt = clock1.getTime()
                print(rt)
                task.window.flip()
                insideStim.draw()

                plusStim = task.plusStim
                minusStim = task.minusStim
                nullStim = task.nullStim
                update_pos(plusStim, (0,-350))
                update_pos(minusStim, (0,-350))
                update_pos(nullStim, (0,-350))

                task.window.flip()
                insideStim.draw()
                task.window.flip()
                core.wait(2)
                
                ###Instrumental component

                letter1 = number[np.random.randint(0,9)]
                letter2 = number[np.random.randint(0,9)]
                letter3 = number[np.random.randint(0,9)]

                wordStim = visual.TextStim(task.window,
                                height=50,
                                pos=(0,-50), text = letter1+letter2+letter3,
                                bold=True,
                                anchorHoriz = 'center',
                                colorSpace='rgb255',
                                color=(255,255,255))

                captured_string = ''
                instruction = ''

                captured_string, df1 = task.instrumental_component(step='conditioning', wordStim=wordStim, captured_string=captured_string, instruction= instruction,
                                                                    insideStim=house_list[n], alphabetornumber=number, day=1, paired_color=paired_color, df1=df1)

                n = n+1
            shuffle(house_list)
            block=block+1

        df1.to_csv("../house_visiting-C/data/day1/reward/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + "_" + "instreward" + ".csv")

        win.mouseVisible=True
        task.face_liking_task(txt_color=(-1,-1,-1), day=1)
        win.mouseVisible=False
        task.binary_choice(house_list=house_list, paired_color=paired_color, day=1)
        win.mouseVisible=True
        task.second_liking_task(df=df, day=1, paired_color=paired_color, house_list=house_list, txt_color=(-1,-1,-1))
        win.mouseVisible=False

        drawer1.draw_text(text=instructions['end'], pos = (0,0), height = 50, wrap=2000)
        core.wait(1)
        task.window.flip()
        _=event.waitKeys(keyList=["space"])

        task.window.close()
        print("Task complete.")
    
    def day2(self):

        white_win = visual.Window(
        units="pix",
        color=(1, 1, 1),
        allowGUI=False,
        fullscr=True
        )

        drawer = Drawer(white_win)
        task = Task(white_win, drawer)
        win = task.window

        df = pd.read_csv("../house_visiting-C/data/day1/liking/" + param["id"] + "_" + "Day1" + "_" + param['condition'] + "_" + "Liking" + ".csv")
        print (df)

        house_list = []

        for i in range(len(df)):
            if df.at[i, 'used'] == 1:
                print(df.at[i, 'Fractal'])
                house_list.append(df.at[i, 'Fractal'])
            else:
                pass

        print(house_list)

        df.set_index('Fractal',inplace=True)

        for house in house_list:
            if df.at[house,'paired'] == 1:
                if 'green' in house:
                    paired_color = 'green'
                elif 'red' in house:
                    paired_color = 'red'
                else:
                    paired_color = 'blue'
            else: 
                pass

        print(paired_color)
        
        #retrieval condition
        if param["condition"] == 'pR':
            text = update_text(task.text,instructions['retrieval'], day=1)
            text.draw()
            drawer.draw_spacebar(day=1)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])

            df1 = pd.DataFrame(columns=['Id', 'Version', 'Condition','instrt', 'instreward'])
            n=1
            while n<6:
                text = update_text(task.text, instructions['house_visiting'][n], day=1)
                text.draw()
                drawer.draw_spacebar(day=1)
                core.wait(1)
                win.flip()
                _=event.waitKeys(keyList=["space"])
                n=n+1

            text = update_text(task.text, instructions['house_visiting'][10], day=1)
            text.draw()
            drawer.draw_spacebar(day=1)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])

            text = update_text(task.text, instructions['house_visiting'][9], day=1)
            text.draw()
            drawer.draw_spacebar(day=1)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])

            drawer.draw_town(house_list=house_list)
            task.window.flip()
            core.wait(1)

            shuffle(house_list)

            paired_list = []

            for house in house_list:
                if paired_color in house:
                    paired_list.append(house)
            
            block=0
            while block<1:
                n=0
                while n<2:  # Use two of the stimuli
                    houseStim = visual.ImageStim(win, image = path['house'] + paired_list[n], size = (550,500), pos = (0,0))
                    insideStim = visual.ImageStim(win, image = path['inside'] + 'day_inside/' + paired_list[n], size = (1920,1080), pos = (0,0))
                    houseStim.draw()
                    win.flip()
                    event.waitKeys(keyList=['space'])
                    insideStim.draw()
                    core.wait(0.1)
                    win.flip()
                    insideStim.draw()
                    win.flip()
                    core.wait(2)
                    
                    ###Instrumental component

                    letter1 = number[np.random.randint(0,9)]
                    letter2 = number[np.random.randint(0,9)]
                    letter3 = number[np.random.randint(0,9)]

                    wordStim = visual.TextStim(win,
                                    height=50,
                                    pos=(0,-50), text = letter1+letter2+letter3,
                                    bold=True,
                                    anchorHoriz = 'center',
                                    colorSpace='rgb255',
                                    color=(255,255,255))

                    captured_string = ''
                    instruction = ''

                    task.instrumental_component(step='conditioning', wordStim=wordStim, captured_string=captured_string, instruction=instruction,
                                                insideStim=paired_list[n], paired_color=paired_color, alphabetornumber=number, day=1, df1=df1)
                    
                    n=n+1
                shuffle(paired_list)
                block = block+1

            block=0
            while block<2:
                n=0
                while n<2:  # Use two of the stimuli
                    houseStim = visual.ImageStim(win, image = path['house'] + paired_list[n], size = (550,500), pos = (0,0))
                    insideStim = visual.ImageStim(win, image = path['inside'] + 'day_inside/' + paired_list[n], size = (1920,1080), pos = (0,0))
                    houseStim.draw()
                    win.flip()
                    event.waitKeys(keyList=['space'])
                    insideStim.draw()
                    core.wait(0.1)
                    win.flip()
                    insideStim.draw()
                    win.flip()
                    core.wait(2)
                    
                    ###Instrumental component

                    letter1 = number[np.random.randint(0,9)]
                    letter2 = number[np.random.randint(0,9)]
                    letter3 = number[np.random.randint(0,9)]

                    wordStim = visual.TextStim(win,
                                    height=50,
                                    pos=(0,-50), text = letter1+letter2+letter3,
                                    bold=True,
                                    anchorHoriz = 'center',
                                    color=(1,1,1))

                    captured_string = ''
                    instruction = ''

                    task.instrumental_component(step='instruction', wordStim=wordStim, captured_string=captured_string, instruction=instruction,
                                                insideStim=paired_list[n], paired_color=paired_color, alphabetornumber=number, day=1, df1=df1)
                    
                    n=n+1
                shuffle(paired_list)
                block = block+1

            unused_CS = paired_list[2]
            print("Unused CS+: ", paired_list[2]) #Write down unused CS+!

        elif param["condition"] == 'NR':
            pass

        print("Unused CS+: ", paired_list[2])

        drawer.draw_text(text='연구자를 불러주십시오.', pos = (0,0), height = 50, wrap=2000, day=1)
        core.wait(1)
        win.flip()
        _=event.waitKeys(keyList=["a","z"]) #z for self-report, a to skip

        if 'z' in _:
            drawer.draw_text(text='self-report placeholder.', pos = (0,0), height = 50, wrap=2000, day=1) #baseline self-report
            win.flip()
            _=event.waitKeys(keyList=["a"])
        else:
            pass

        win.flip() #collect saliva and do SECPT
        _=event.waitKeys(keyList=["a","z"]) #z for self-report, a to skip

        if 'z' in _:
            drawer.draw_text(text='self-report placeholder.', pos = (0,0), height = 50, wrap=2000, day=1) #self-report after SECPT induction
            win.flip()
            _=event.waitKeys(keyList=["a"])
        else:
            pass

        drawer.draw_text(text='기다려주세요...', pos = (0,0), height = 50, wrap=2000, day=1)
        core.wait(1)
        win.flip()

        task.movie()

        drawer.draw_text(text='연구자를 불러주십시오.', pos = (0,0), height = 50, wrap=2000, day=1)
        core.wait(1)
        win.flip()
        _=event.waitKeys(keyList=["a"])
        win.flip() #collect saliva
        _=event.waitKeys(keyList=["a"])

        black_win = visual.Window(
        units="pix",
        color=(-1, -1, -1),
        allowGUI=False,
        fullscr=True
        )

        drawer = Drawer(black_win)
        task = Task(black_win, drawer)
        win = task.window

        #Counterconditioning
        n=0
        while n<3:
            text = update_pos(update_text(task.text, instructions['day2_house'][n], day=2), (0,0))
            text.draw()
            drawer.draw_spacebar(day=2)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])
            n=n+1

        drawer.draw_town(house_list=house_list)  
        win.flip()
        core.wait(1)

        df1 = pd.DataFrame(columns=['Id', 'Version', 'Condition','instrt', 'instreward'])
        clock1=core.Clock()
        block=0
        while block<20:
            n=0
            while n<9:
                houseStim = visual.ImageStim(win, image = path['house'] + house_list[n], size = (550,500), pos = (0,0))
                insideStim = visual.ImageStim(win, image = path['inside'] + 'night_inside/' + house_list[n], size = (1920,1080), pos = (0,0))

                houseStim.draw()
                win.flip()
                clock1.reset(newT=0.0)
                event.waitKeys(keyList=['space'])
                rt = clock1.getTime()
                print(rt)
                win.flip()
                insideStim.draw()

                win.flip()
                insideStim.draw()
                win.flip()
                core.wait(2)
                
                ###Instrumental component

                letter1 = number[np.random.randint(0,9)]
                letter2 = number[np.random.randint(0,9)]
                letter3 = number[np.random.randint(0,9)]

                wordStim = visual.TextStim(win,
                                height=50,
                                pos=(0,-50), text = letter1+letter2+letter3,
                                bold=True,
                                anchorHoriz = 'center',
                                colorSpace='rgb255',
                                color=(255,255,255))

                captured_string = ''
                instruction = ''

                captured_string, df1 = task.instrumental_component(step='counterconditioning', wordStim=wordStim, captured_string=captured_string, instruction=instruction,
                                                                    insideStim=house_list[n], paired_color=paired_color, alphabetornumber=number, day=2, df1=df1)
                
                n = n+1
            shuffle(house_list)
            block=block+1
        
        df1.to_csv("../house_visiting-C/data/day2/reward/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + "_" + "instreward" + ".csv")

        win.mouseVisible=True
        task.face_liking_task(txt_color=(1,1,1), day=2)
        win.mouseVisible=False
        task.binary_choice(house_list=house_list, paired_color=paired_color, day=2, unused=unused_CS)
        win.mouseVisible=True
        task.second_liking_task(df=df, day=2, paired_color=paired_color, house_list=house_list, txt_color=(1,1,1), unused=unused_CS)
        win.mouseVisible=False

        drawer.draw_text(text=instructions['end'], pos = (0,0), height = 50, wrap=2000, day=2)
        core.wait(1)
        win.flip()
        _=event.waitKeys(keyList=["space"])

        win.close()
        print("Task complete.")
    
    def day3(self):
        df = pd.read_csv("../house_visiting-C/data/day2/liking/" + param["id"] + "_" + "Day2" + "_" + param['condition'] + "_" + "Liking" + ".csv")
        print (df)


        house_list = []

        for i in range(len(df)):  # computer is ignoring these 'for' loops for some reason
            if df.at[i, 'used'] == 1:
                print(df.at[i, 'Fractal'])
                house_list.append(df.at[i, 'Fractal'])
            else:
                pass

        for i in range(len(df)):  # computer is ignoring these 'for' loops for some reason
            if df.at[i, 'Paired_Unused'] == 1:
                print(df.at[i, 'Fractal'])
                unused_CS = df.at[i, 'Fractal']
            else:
                pass

        print(house_list)

        df.set_index('Fractal',inplace=True)

        for house in house_list:
            if df.at[house,'paired'] == 1:
                if 'green' in house:
                    paired_color = 'green'
                elif 'red' in house:
                    paired_color = 'red'
                else:
                    paired_color = 'blue'
            else: 
                pass

        print(paired_color)

        ##########################counterbalance ABA/ABC order##################################

        if param["order"]=='ac': # ABA first
            ####ABA Renewal####
            white_win = visual.Window(
            units="pix",
            color=(1, 1, 1),
            allowGUI=False,
            fullscr=True
            )
            drawer = Drawer(white_win)
            task = Task(white_win, drawer)
            win = task.window
            win.mouseVisible=False
            text = update_text(task.text,instructions['renewal'][1], day=1)
            text.draw()
            drawer.draw_spacebar(day=1)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])

            #fake conditioning

            drawer.draw_town(house_list=house_list)  
            win.flip()
            core.wait(1)

            df2 = pd.DataFrame(columns=['Id', 'Version', 'Condition','instrt', 'instreward'])
            clock1=core.Clock()
            block=0
            while block<1:
                n=0
                while n<9:
                    houseStim = visual.ImageStim(win, image = path['house'] + house_list[n], size = (550,500), pos = (0,0))
                    insideStim = visual.ImageStim(win, image = path['inside'] + 'day_inside/' + house_list[n], size = (1920,1080), pos = (0,0))
                    
                    houseStim.draw()
                    win.flip()
                    clock1.reset(newT=0.0)
                    event.waitKeys(keyList=['space'])
                    rt = clock1.getTime()
                    print(rt)
                    win.flip()
                    insideStim.draw()
                    win.flip()

                    letter1 = number[np.random.randint(0,9)]
                    letter2 = number[np.random.randint(0,9)]
                    letter3 = number[np.random.randint(0,9)]

                    wordStim = visual.TextStim(win,
                                    height=50,
                                    pos=(0,-50), text = letter1+letter2+letter3,
                                    bold=True,
                                    anchorHoriz = 'center',
                                    colorSpace='rgb255',
                                    color=(255,255,255))

                    captured_string = ''
                    instruction = ''

                    captured_string, df2 = task.instrumental_component(step='instruction', wordStim=wordStim, captured_string=captured_string, instruction=instruction,
                                                                        insideStim=house_list[n], paired_color=paired_color, alphabetornumber=number, day=1, df1=df2)
                    
                    n = n+1
                shuffle(house_list)
                block=block+1
            df2.to_csv("../house_visiting-C/data/day3/renewal/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + "_" + "ABAinst" + ".csv")

            task.binary_choice(house_list=house_list, paired_color=paired_color, day=3, unused=unused_CS, renewal_type='aba')
            win.mouseVisible=True
            task.second_liking_task(df=df, day=3, paired_color=paired_color, house_list=house_list, txt_color=(-1,-1,-1), unused=unused_CS, renewal_type='aba')
            win.mouseVisible=False

            drawer.draw_text(text='1분 간 쉬겠습니다.', pos = (0,0), height = 50, wrap=2000)
            win.flip()
            core.wait(60)
            
            ####ABC Renewal####

            gray_win = visual.Window(
            units="pix",
            color=(0, 0, 0),
            allowGUI=False,
            fullscr=True
            )
            drawer = Drawer(gray_win)
            task = Task(gray_win, drawer)
            win = task.window
            win.mouseVisible=False
            text = update_text(task.text,instructions['renewal'][0], day=1)
            text.draw()
            drawer.draw_spacebar(day=1)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])

            #conditioning

            drawer.draw_town(house_list=house_list)  
            win.flip()
            core.wait(1)

            df1 = pd.DataFrame(columns=['Id', 'Version', 'Condition','instrt', 'instreward'])
            clock1=core.Clock()
            block=0
            while block<1:
                n=0
                while n<9:
                    houseStim = visual.ImageStim(win, image = path['house'] + house_list[n], size = (550,500), pos = (0,0))
                    insideStim = visual.ImageStim(win, image = path['inside'] + 'new_inside/' + house_list[n], size = (1920,1080), pos = (0,0))
                    
                    houseStim.draw()
                    win.flip()
                    clock1.reset(newT=0.0)
                    event.waitKeys(keyList=['space'])
                    rt = clock1.getTime()
                    print(rt)
                    win.flip()
                    insideStim.draw()
                    win.flip()

                    letter1 = number[np.random.randint(0,9)]
                    letter2 = number[np.random.randint(0,9)]
                    letter3 = number[np.random.randint(0,9)]

                    wordStim = visual.TextStim(win,
                                    height=50,
                                    pos=(0,-50), text = letter1+letter2+letter3,
                                    bold=True,
                                    anchorHoriz = 'center',
                                    colorSpace='rgb255',
                                    color=(255,255,255))

                    captured_string = ''
                    instruction = ''

                    captured_string, df1 = task.instrumental_component(step='instruction', wordStim=wordStim, captured_string=captured_string, instruction=instruction,
                                                                        insideStim=house_list[n], paired_color=paired_color, alphabetornumber=number, day=3, df1=df1)
                    
                    n = n+1
                shuffle(house_list)
                block=block+1
            df1.to_csv("../house_visiting-C/data/day3/renewal/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + "_" + "ABCinst" + ".csv")
            task.binary_choice(house_list=house_list, paired_color=paired_color, day=3, unused=unused_CS, renewal_type='abc')
            df.set_index('Fractal',inplace=True)
            win.mouseVisible=True
            task.second_liking_task(df=df, day=3, paired_color=paired_color, house_list=house_list, txt_color=(-1,-1,-1), unused=unused_CS, renewal_type='abc')
            win.mouseVisible=False
            drawer.draw_text(text=instructions['end'], pos = (0,0), height = 50, wrap=2000)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])

            win.close()
            print("Task complete.")

        elif param["order"]=='ca': # ABC first
            ####ABC Renewal####

            gray_win = visual.Window(
            units="pix",
            color=(0, 0, 0),
            allowGUI=False,
            fullscr=True
            )
            drawer = Drawer(gray_win)
            task = Task(gray_win, drawer)
            win = task.window
            win.mouseVisible=False
            text = update_text(task.text,instructions['renewal'][0], day=1)
            text.draw()
            drawer.draw_spacebar(day=1)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])

            #fake conditioning

            drawer.draw_town(house_list=house_list)  
            win.flip()
            core.wait(1)

            df1 = pd.DataFrame(columns=['Id', 'Version', 'Condition','instrt', 'instreward'])
            clock1=core.Clock()
            block=0
            while block<1:
                n=0
                while n<9:
                    houseStim = visual.ImageStim(win, image = path['house'] + house_list[n], size = (550,500), pos = (0,0))
                    insideStim = visual.ImageStim(win, image = path['inside'] + 'new_inside/' + house_list[n], size = (1920,1080), pos = (0,0))
                    
                    houseStim.draw()
                    win.flip()
                    clock1.reset(newT=0.0)
                    event.waitKeys(keyList=['space'])
                    rt = clock1.getTime()
                    print(rt)
                    win.flip()
                    insideStim.draw()
                    win.flip()

                    letter1 = number[np.random.randint(0,9)]
                    letter2 = number[np.random.randint(0,9)]
                    letter3 = number[np.random.randint(0,9)]

                    wordStim = visual.TextStim(win,
                                    height=50,
                                    pos=(0,-50), text = letter1+letter2+letter3,
                                    bold=True,
                                    anchorHoriz = 'center',
                                    colorSpace='rgb255',
                                    color=(255,255,255))

                    captured_string = ''
                    instruction = ''

                    captured_string, df1 = task.instrumental_component(step='instruction', wordStim=wordStim, captured_string=captured_string, instruction=instruction,
                                                                        insideStim=house_list[n], paired_color=paired_color, alphabetornumber=number, day=3, df1=df1)
                    
                    n = n+1
                shuffle(house_list)
                block=block+1
            df1.to_csv("../house_visiting-C/data/day3/renewal/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + "_" + "ABCinst" + ".csv")
            task.binary_choice(house_list=house_list, paired_color=paired_color, day=3, unused=unused_CS, renewal_type='abc')
            win.mouseVisible=True
            task.second_liking_task(df=df, day=3, paired_color=paired_color, house_list=house_list, txt_color=(-1,-1,-1), unused=unused_CS, renewal_type='abc')
            win.mouseVisible=False

            drawer.draw_text(text='1분 간 쉬겠습니다.', pos = (0,0), height = 50, wrap=2000)
            win.flip()
            core.wait(60)

            ####ABA Renewal####
            white_win = visual.Window(
            units="pix",
            color=(1, 1, 1),
            allowGUI=False,
            fullscr=True
            )
            drawer = Drawer(white_win)
            task = Task(white_win, drawer)
            win = task.window
            win.mouseVisible=False
            text = update_text(task.text,instructions['renewal'][1], day=1)
            text.draw()
            drawer.draw_spacebar(day=1)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])

            #fake conditioning

            drawer.draw_town(house_list=house_list)  
            win.flip()
            core.wait(1)

            df2 = pd.DataFrame(columns=['Id', 'Version', 'Condition','instrt', 'instreward'])
            clock1=core.Clock()
            block=0
            while block<1:
                n=0
                while n<9:
                    houseStim = visual.ImageStim(win, image = path['house'] + house_list[n], size = (550,500), pos = (0,0))
                    insideStim = visual.ImageStim(win, image = path['inside'] + 'day_inside/' + house_list[n], size = (1920,1080), pos = (0,0))
                    
                    houseStim.draw()
                    win.flip()
                    clock1.reset(newT=0.0)
                    event.waitKeys(keyList=['space'])
                    rt = clock1.getTime()
                    print(rt)
                    win.flip()
                    insideStim.draw()
                    win.flip()

                    letter1 = number[np.random.randint(0,9)]
                    letter2 = number[np.random.randint(0,9)]
                    letter3 = number[np.random.randint(0,9)]

                    wordStim = visual.TextStim(win,
                                    height=50,
                                    pos=(0,-50), text = letter1+letter2+letter3,
                                    bold=True,
                                    anchorHoriz = 'center',
                                    colorSpace='rgb255',
                                    color=(255,255,255))

                    captured_string = ''
                    instruction = ''

                    captured_string, df2 = task.instrumental_component(step='instruction', wordStim=wordStim, captured_string=captured_string, instruction=instruction,
                                                                        insideStim=house_list[n], paired_color=paired_color, alphabetornumber=number, day=1, df1=df2)
                    
                    n = n+1
                shuffle(house_list)
                block=block+1
            df2.to_csv("../house_visiting-C/data/day3/renewal/" + param["id"] + "_" + param["version"] + "_" + param['condition'] + "_" + "ABAinst" + ".csv")
            task.binary_choice(house_list=house_list, paired_color=paired_color, day=3, unused=unused_CS, renewal_type='aba')
            df.set_index('Fractal',inplace=True)
            win.mouseVisible=True
            task.second_liking_task(df=df, day=3, paired_color=paired_color, house_list=house_list, txt_color=(-1,-1,-1), unused=unused_CS, renewal_type='aba')
            win.mouseVisible=False

            drawer.draw_text(text=instructions['end'], pos = (0,0), height = 50, wrap=2000)
            core.wait(1)
            win.flip()
            _=event.waitKeys(keyList=["space"])

            win.close()
            print("Task complete.")
        else:
            print(param['order'])
            print("Order not specified")

########################################################DAY1####################################################

if param['version'] == 'Day1':

    runner=Runner()
    runner.day1()
 

        
########################################################DAY2#####################################################

elif param['version'] == 'Day2':
    
    runner=Runner()
    runner.day2()



########################################################DAY3######################################################

elif param['version'] == 'Day3':

    runner=Runner()
    runner.day3()