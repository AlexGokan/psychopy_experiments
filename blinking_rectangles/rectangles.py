

from psychopy import core,visual,event,data,gui
import numpy as np
from itertools import product as iter_product

#<--base parameters-->

minus_plus = +1
if minus_plus < 0:
    wave_amp = 0.8
else:
    wave_amp = 1.1

anim_speed = 10
#--------------------

def exit_program():
    window.close()
    Fout.close()
    core.quit()

def LM_S_to_RGB(LM,S,Lum):
    Ltd = Lum*LM
    Mtd = Lum-Ltd
    Std = Lum*S

    R = Ltd * 0.0794 + Mtd * (-0.1286) + Std * 0.0020
    G = Ltd * (-0.0106) + Mtd * 0.0553 + Std * (-0.0020)
    B = Ltd * (-0.0001) + Mtd * (-0.0047) + Std * 0.0118
    #turn this into a matmul later

    return np.array([R,G,B])

def gamma_corr(v):
    gammag = 0.46
    return np.power(v,gammag)


def get_color_s(t):
    wave = np.sin(t)
    wave *= wave_amp
    wave *= 0.5
    if minus_plus>0:
        wave = wave + (wave_amp/2)
    else:
        wave = wave - (wave_amp/2)
    
    c1 = LM_S_to_RGB(0.657,0.993+wave,40)
    return c1

bg1 = gamma_corr(get_color_s(np.pi/2))
bg2 = gamma_corr(get_color_s(3*np.pi/2))

window = visual.Window((1920,1080),allowGUI=False,monitor='testMonitor',units='deg')

#<--get participant info-->
participant_info = {'id_num':'test','exp_num':0}
participant_info['datestr'] = data.getDateStr()

dlg = gui.DlgFromDict(participant_info,title='fill out your info',fixed=['datestr'])

#<--generate csv file-->
base_path = 'C:/src/psychopy_experiments/blinking_rectangles/data/'

filename = base_path + participant_info['id_num'] + participant_info['datestr']
Fout = open(filename+'.csv','w')
Fout.write('plus_minus_s,gap,height,in_out\n')


#<--show instructions-->
txt_size = 0.5
msg1 = visual.TextStim(window,pos=[0,2],height=txt_size,text="You will see a set of blinking rectangles, one on each side of the screen")
msg2 = visual.TextStim(window,pos=[0,0],height=txt_size,text="Press Y if they are blinking in phase (at the same time)")
msg3 = visual.TextStim(window,pos=[0,-1],height=txt_size,text="Press N if they are blinking out of phase (at different times)")
msg4 = visual.TextStim(window,pos=[0,-2],height=txt_size,text="Press Q or esc at any time to quit")
msg5 = visual.TextStim(window,pos=[0,-4],height=txt_size,text="Press any key to continue")

msg1.draw()
msg2.draw()
msg3.draw()
msg4.draw()
msg5.draw()
window.flip()
event.waitKeys()

#<--construct all possible pairs of the other variable parameters-->
possible_spacing = [0,1/60,2/60,4/60,8/60,32/60]#1/60 deg = 1 arcmin
possible_heights = 5+np.array([0,1/60,2/60,4/60,8/60,16/60,64/60])

param_combinations = list(iter_product(possible_spacing,possible_heights))
np.random.shuffle(param_combinations)
print(param_combinations)
print('==========================')

#-------------------------




left_blinker = visual.Rect(window,size=[1,5],ori=0,pos=[-4,0],fillColor=[.5,.5,0])
right_blinker = visual.Rect(window,size=[1,5],ori=0,pos=[+4,0],fillColor=[.5,.5,0])

ll_flanker = visual.Rect(window,size=[1,5],pos=[-5,0],fillColor=bg1)
lr_flanker = visual.Rect(window,size=[1,5],pos=[-3,0],fillColor=bg1)

rl_flanker = visual.Rect(window,size=[1,5],pos=[3,0],fillColor=bg2)
rr_flanker = visual.Rect(window,size=[1,5],pos=[5,0],fillColor=bg2)

bg_l_rect = visual.Rect(window,size=[20,30],pos=[-10,0],fillColor=bg2)
bg_r_rect = visual.Rect(window,size=[20,30],pos=[+10,0],fillColor=bg1)


#parameter space
"""
2. vertical height of flankers
3. flanker gap
"""




ll_flanker.fillColor = bg1
lr_flanker.fillColor = bg1

rl_flanker.fillColor = bg2
rr_flanker.fillColor = bg2

bg_l_rect.fillColor = bg2
bg_r_rect.fillColor = bg1

trial_clock = core.Clock()
t = 0


def run_one_frame(t):
    kp = event.getKeys(["left","right","q","esc"])
    if len(kp)>0 and kp[0] in ['q','esc']:
        exit_program()
    if 'left' in kp:
        return 'left'
    if 'right' in kp:
        return 'right'


    left_color = gamma_corr(get_color_s(t*anim_speed))
    right_color = gamma_corr(get_color_s(t*anim_speed))

    color_offset = np.sin(t)*0.5
    left_blinker.fillColor = left_color
    right_blinker.fillColor = right_color

    bg_l_rect.draw()
    bg_r_rect.draw()

    left_blinker.draw()
    right_blinker.draw()

    ll_flanker.draw()
    lr_flanker.draw()

    rl_flanker.draw()
    rr_flanker.draw()


    window.flip()

    return None

for trial_params in param_combinations:
    spacing = trial_params[0]
    height = trial_params[1]

    print(spacing,height)
    print(ll_flanker.pos)

    ll_flanker.size = [1,height]#modify the height
    lr_flanker.size = [1,height]
    rr_flanker.size = [1,height]
    rl_flanker.size = [1,height]

    ll_flanker.pos = (-5-spacing,0)
    lr_flanker.pos = (-3+spacing,0)
    rr_flanker.pos = (5+spacing,0)
    rl_flanker.pos = (3-spacing,0)

    print(ll_flanker.pos)
    print('---------------')

    res = None
    while res is None:
        t = trial_clock.getTime()
        res = run_one_frame(t)
    
    if res == 'left':
        print('out of phase')
        Fout.write('+1,%f,%i,out\n'%(spacing,height))
    elif res == 'right':
        print('in phase')
        Fout.write('+1,%f,%i,in\n'%(spacing,height))

    #Fout.write('plus_minus_s,gap,height,in_out\n')
    

exit_program()