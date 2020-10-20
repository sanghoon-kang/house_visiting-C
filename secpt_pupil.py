import os
import yaml
import itertools
import random
import math
import socket  # for iMotions
import sys  # for iMotions
import win32gui
import win32con
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from psychopy import core, visual, event, data, gui

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

STUDY_CODE = 'HVT'

PATH_ROOT = Path(__file__).absolute().parent
PATH_DATA = PATH_ROOT / 'data/eye'

DURATION = 180
BREAK_DURATION = 30

duration = DURATION

COLUMNS_DATA = ['subjID', 'trial_number', 'stress', 'RT_stress']

class Pupil_Drawer:

    def __init__(self,
                 window: visual.Window,
                 size: float,
                 text_size: int = 50,
                 text_font: str = 'NanumGothic',
                 wrap_width: float = 2000,
                 n_rate: int = 11,
                 dist_interval: float = 115,
                 height_tick: float = 40,
                 text_margin: float = 40,
                 line_width: float = 220,
                 line_color: str = 'white'):


        self.window = window
        self.size = size
        self.text_size = text_size * size
        self.text_font = text_font
        self.wrap_width = wrap_width * size

        self.n_rate = n_rate
        self.dist_interval = dist_interval
        self.height_tick = height_tick
        self.text_margin = text_margin
        self.line_width = line_width
        self.line_color = line_color

        fn_inst = '../house_visiting-C/instructions_short.yml'
        with open(fn_inst, 'r', encoding='utf-8') as f:
            self.instructions = yaml.load(f, Loader=Loader)

    def draw_fixation(self):
        dot = visual.Circle(
            self.window,
            radius=0.4 * self.size,
            fillColor='white')
        dot.draw()

    def draw_bar(self, x=0, y=0, resp='STRESS'):
        bar_width = (self.n_rate - 1) * self.dist_interval
        line = visual.Line(
            self.window,
            start=(x + -bar_width / 2, y),
            end=(x + bar_width / 2, y),
            lineWidth=self.line_width,
            lineColor=self.line_color,
        )
        line.draw()

        for i in range(self.n_rate):
            pos_x = x + -bar_width / 2 + self.dist_interval * i
            line = visual.Line(
                self.window,
                start=(pos_x, self.height_tick / 2 + y),
                end=(pos_x, -self.height_tick / 2 + y),
                lineWidth=self.line_width,
                lineColor=self.line_color,
            )
            line.draw()

        low = self.instructions[f'response-{resp}'][1]
        text = visual.TextStim(
            self.window,
            text= low,
            font=self.text_font,
            height=self.text_size * 2 / 3,
            pos=(x - bar_width / 2, y - self.height_tick * 4)
        )
        text.size = self.text_size
        text.draw()

        high = self.instructions[f'response-{resp}'][2]
        text = visual.TextStim(
            self.window,
            text=high,
            font=self.text_font,
            height=self.text_size * 2 / 3,
            pos=(x + bar_width / 2, y - self.height_tick * 4)
        )
        text.size = self.text_size
        text.draw()

    def draw_pointer(self, v, x=0, y=0):
        assert 0 <= v < self.n_rate
        bar_width = (self.n_rate - 1) * self.dist_interval
        pos_x = -bar_width / 2 + self.dist_interval * v + x

        circ = visual.Circle(
            self.window,
            pos=(pos_x, y),
            radius=self.height_tick / 4,
            fillColor='red'
        )
        circ.draw()

    def draw_response_instructions(self, i, resp='STRESS'):
        txt = self.instructions[f'response-{resp}'][i]
        pos = (0, 2 * self.text_size)
        text = visual.TextStim(
            self.window,
            txt,
            font=self.text_font,
            pos=pos,
            bold=True,
            height=self.text_size,
            wrapWidth=self.wrap_width)
        text.draw()

    def draw(self, v, x=0, y=0, resp='STRESS'):
        self.draw_response_instructions(0, resp)
        self.draw_bar(x=x, y=y, resp=resp)
        self.draw_pointer(v, x=x, y=y)

    def draw_secpt_instructions(self, i):
        txt = self.instructions['secpt_instructions'][i]
        text = visual.TextStim(
            self.window,
            txt,
            font=self.text_font,
            pos=(0, 0),
            bold=True,
            height=self.text_size,
            wrapWidth=self.wrap_width)
        text.draw()

    def draw_secpt_control_instructions(self, i):
        txt = self.instructions['secpt_control_instructions'][i]
        text = visual.TextStim(
            self.window,
            txt,
            font=self.text_font,
            pos=(0, 0),
            bold=True,
            height=self.text_size,
            wrapWidth=self.wrap_width)
        text.draw()

    def draw_calibration_instructions(self, i):
        txt = self.instructions['calibration'][i]
        text = visual.TextStim(
            self.window,
            txt,
            font=self.text_font,
            pos=(0, 0),
            bold=True,
            height=self.text_size,
            wrapWidth=self.wrap_width,
            color=(1,1,1))
        text.draw()

    def draw_break(self):
        txt = self.instructions['break'][0]
        text = visual.TextStim(
            self.window,
            txt,
            font=self.text_font,
            pos=(0, 0),
            bold=True,
            height=self.text_size,
            wrapWidth=self.wrap_width)
        text.draw()

    def draw_calibration_error(self):
        txt = self.instructions['calibration_error'][0]
        text = visual.TextStim(
            self.window,
            txt,
            font=self.text_font,
            pos=(0, 0),
            bold=True,
            height=self.text_size,
            wrapWidth=self.wrap_width)
        text.draw()
    
    def draw_blank(self):
        text = visual.TextStim(
            self.window,
            ' ',
            font=self.text_font,
            pos=(0, 0),
            bold=True,
            height=self.text_size,
            wrapWidth=self.wrap_width)
        text.draw()        

class Pupil_Runner:

    def __init__(self, window, subj_id, drawer, duration, break_duration, path_data):
        self.window = window
        self.drawer = drawer
        self.subj_id = subj_id
        self.duration = duration
        self.break_duration = break_duration
        self.path_data = path_data
        self.data = pd.DataFrame(None, columns=COLUMNS_DATA)

        # initialize connection with iMotions
        self.socket_er = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_rc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST= 'localhost'
        self.PORT_RC = 8087
        self.PORT_ER = 8089

        self.timer = core.Clock()

        # For sleep time for various types of trials (before participant can choose; time in ms)
        self.T_BASE = self.duration  # For solo trials – time before red identifier appears and allows participant to make selection
        self.T_CPT = self.duration
        self.T_WAIT = 1
        self.T_BREAK = self.break_duration
    
    def open_connection(self):
        # connecting tcp client
        self.socket_rc.connect((self.HOST, self.PORT_RC)) # connect() is used from the client side, whereas bind() is used from the server side

    def close_connection(self):
        imessage ='E;1;OpenSesame;;;;;OpenSesameData;end;complete\r\n'
        self.socket_er.sendto(imessage.encode(), (self.HOST, self.PORT_ER)) #send utf-8 bytes to server

        cal_data = 0
        while cal_data == 0:
	        self.socket_rc.send('R;1;002;SLIDESHOWNEXT\r\n'.encode()) #send to client
	        data = self.socket_rc.recv(1024) # how big chunks of data do we want to receive - 1024 is pretty big
        self.socket_rc.close()

    def imotions_rc(self, imessage):
        self.socket_rc.send(imessage.encode())
        return self.socket_rc.recv(1024)

    def imotions_er(self, imessage):
        self.socket_er.sendto(imessage.encode(), (self.HOST, self.PORT_ER))        

    def gaze_cal(self):
        cal_data = 0
        while cal_data == 0:
            cal_data = self.imotions_rc(
                f'R;3;001;RUN;HVT;HVT{self.subj_id}_{sess};Gender=Male Age=1;NoPromptIgnoreWarnings\r\n')
        core.wait(34)

        self.minimize_iMotions_window()

    def process_calibration_data(self):
        # Check if Calibration was successful
        success = 0
        cal_data = 0
        while success == 0:
            cal_data = self.imotions_rc('R;1;001;STATUS\r\n')
            iRespond = cal_data.decode().split(';')
            print("iRespond[3]:\t", iRespond[3])
            if iRespond[3] != '':
                success = 1
            else:
                self.drawer.draw_calibration_error()
                self.window.flip()
                _ = event.waitKeys(keyList=['space', 'return'])
    
    def fixation_base(self, when):
        self.drawer.draw_fixation()
        self.window.flip()
        self.imotions_er(f'E;1;OpenSesame;;;;;OpenSesameData;0;{when}\r\n')
        core.wait(self.T_BASE)

        if when == 'AFTER':
            self.imotions_er('E;1;OpenSesame;;;;;OpenSesameData;0;END\r\n')
        
    def fixation_cpt(self):
        self.drawer.draw_fixation()
        self.window.flip()
        self.imotions_er('E;1;OpenSesame;;;;;OpenSesameData;0;CPT\r\n')
        core.wait(self.T_CPT)

    def get_response(self, i, resp='STRESS'):
        mid = (self.drawer.n_rate - 1) / 2
        p = mid
        n = 0

        self.imotions_er(f'E;1;OpenSesame;;;;;OpenSesameData;0;RATING_{resp}\r\n')
        while True:
            self.drawer.draw(p, resp=resp)
            self.window.flip()
            if n == 0:
                time1 = self.timer.getTime()
            keys = event.waitKeys(keyList=['left', 'return', 'right', 'space'])

            if keys[0] == 'left':
                p = max(0, p - 1)
            elif keys[0] == 'right':
                p = min(self.drawer.n_rate - 1, p + 1)
            else:
                time2 = self.timer.getTime()
                rt = time2 - time1             
                break

            n += 1
        
        # data coding
        p_record = p
        if resp == 'STRESS':
            t = 'stress'
        elif resp == 'DIFFICULTY':
            t = 'difficulty'
        elif resp == 'PAIN':
            t = 'pain'
        elif resp == 'UNPLEASANT':
            t = 'unpleasant'
        # save data
        row = pd.Series({
            'subjID': self.subj_id,
            'type' : t,
            'trial_number': i,
            'score': p_record,
            'RT_stress': round(rt * 1000)
        })

        self.data = self.data.append(row, ignore_index=True)
        self.data.to_csv(self.path_data, index=False, sep=',')

        self.imotions_er(f'E;1;OpenSesame;;;;;OpenSesameData;0;END_{resp}\r\n')

    def run_calibration_instructions(self, i):
        self.drawer.draw_calibration_instructions(i)
        self.window.flip()
        self.imotions_er('E;1;OpenSesame;;;;;OpenSesameData;0;calinstructions\r\n')
        _ = event.waitKeys(keyList=['space', 'return'])  

    def run_secpt_instructions(self, i):
        if i == 8 or i == 6:
            self.drawer.draw_secpt_instructions(i)
            self.window.flip()
            self.imotions_er('E;1;OpenSesame;;;;;OpenSesameData;0;secptinstructions\r\n')
            _ = event.waitKeys(keyList=['a']) 
        else:
            self.drawer.draw_secpt_instructions(i)
            self.window.flip()
            self.imotions_er('E;1;OpenSesame;;;;;OpenSesameData;0;secptinstructions\r\n')
            _ = event.waitKeys(keyList=['space', 'return']) 

    def run_secpt_control_instructions(self, i):
        if i == 7 or i == 5:
            self.drawer.draw_secpt_control_instructions(i)
            self.window.flip()
            self.imotions_er('E;1;OpenSesame;;;;;OpenSesameData;0;secptcontrolinstructions\r\n')
            _ = event.waitKeys(keyList=['a'])
        else:
            self.drawer.draw_secpt_control_instructions(i)
            self.window.flip()
            self.imotions_er('E;1;OpenSesame;;;;;OpenSesameData;0;secptcontrolinstructions\r\n')
            _ = event.waitKeys(keyList=['space', 'return']) 

    def run_instructions(self, i):
        self.drawer.draw_instructions(i)
        self.window.flip()
        self.imotions_er('E;1;OpenSesame;;;;;OpenSesameData;0;instructions\r\n')
        _ = event.waitKeys(keyList=['space', 'return'])  
    
    def run_break(self):
        self.drawer.draw_break()
        self.window.flip()
        self.imotions_er('E;1;OpenSesame;;;;;OpenSesameData;0;BREAK\r\n')
        core.wait(self.T_BREAK)

    # def set_foreground_window(self, name):  # 'iMotions (ccsl_del)', 'PsychoPy'
    #     do = 1
    #     while do:
    #         window = win32gui.FindWindow(None, name)
    #         do = (window == 0)
    #     win32gui.SetForegroundWindow(window)
    #     print(f"Foreground window set to {name}.")

    def minimize_iMotions_window(self):
        window_imo = win32gui.FindWindow(None, 'iMotions (ccsl_del)')
        win32gui.ShowWindow(window_imo, win32con.SW_MINIMIZE)


def secpt(window, pupil_drawer, pupil_runner):

    # Open a window
    window = window

    # Initialize a drawer and a runner
    drawer = pupil_drawer
    runner = pupil_runner

    if param['condition'] == 'PRS' or param['condition'] == 'NRS':

        cpt_clock = core.Clock()

        # collect saliva
        runner.imotions_er(f'E;1;OpenSesame;;;;;OpenSesameData;0;BEFORESALIVA\r\n')
        runner.run_secpt_instructions(6)

        # Eyeblink: CPT
        runner.run_secpt_instructions(4)
        runner.get_response(0, resp='STRESS')
        runner.run_secpt_instructions(0)
        runner.run_secpt_instructions(1)
        runner.run_secpt_instructions(2)
        runner.run_secpt_instructions(3)
        runner.run_secpt_instructions(7)
        runner.run_secpt_instructions(8)
        stress_onset = core.Clock()
        runner.fixation_cpt()

        runner.run_secpt_instructions(5)
        runner.get_response(1, resp='STRESS')
        runner.get_response(2, resp='PAIN')
        runner.get_response(3, resp='DIFFICULTY')

        # collect saliva
        runner.imotions_er(f'E;1;OpenSesame;;;;;OpenSesameData;0;AFTER1SALIVA\r\n')
        runner.run_secpt_instructions(6)
        cpt_time = cpt_clock.getTime()
        stress_onset = stress_onset.getTime()
        return cpt_time, stress_onset


    elif param['condition'] == 'PRN' or param['condition'] == 'NRN':

        cpt_clock = core.Clock()
        # collect saliva
        runner.imotions_er(f'E;1;OpenSesame;;;;;OpenSesameData;0;BEFORESALIVA\r\n')
        runner.run_secpt_control_instructions(5)

        # Eyeblink: CPT
        runner.run_secpt_control_instructions(3)
        runner.get_response(0, resp='STRESS')
        
        runner.run_secpt_control_instructions(0)
        runner.run_secpt_control_instructions(1)
        runner.run_secpt_control_instructions(2)
        runner.run_secpt_control_instructions(6)
        runner.run_secpt_control_instructions(7)
        stress_onset = core.Clock()
        runner.fixation_cpt()

        runner.run_secpt_control_instructions(4)
        runner.get_response(1, resp='STRESS')
        runner.get_response(2, resp='PAIN')
        runner.get_response(3, resp='DIFFICULTY')

        # collect saliva
        runner.imotions_er(f'E;1;OpenSesame;;;;;OpenSesameData;0;AFTER1SALIVA\r\n')
        runner.run_secpt_control_instructions(5)
        cpt_time = cpt_clock.getTime()
        stress_onset = stress_onset.getTime()
        return cpt_time, stress_onset