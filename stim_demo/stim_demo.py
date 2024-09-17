

from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy, random

def get_l_r_blocking():
    resp = None
    while resp is None:
        all_keys = event.waitKeys()
        for k in all_keys:
            if k == 'left':
                return -1
            if k == 'right':
                return 1
            if k in ['q','escape']:
                return None
        event.clearEvents()

try:
    exp_info = fromFile('lastParams.pickle')
except:
    exp_info = {'observer':'ag01','orientation':0}

exp_info['datestr'] = data.getDateStr()

base_path = 'C:/src/psychopy_experiments/stim_demo/'

dlg = gui.DlgFromDict(exp_info,title='fill out your info',fixed=['datestr'])
if dlg.OK:
    toFile(base_path + 'lastParams.pickle',exp_info)
else:
    core.quit()

filename = base_path + exp_info['observer'] + exp_info['datestr']
Fout = open(filename+'.csv','w')
Fout.write('targetSide,oriIncrement,correct\n')


staircase = data.StairHandler(startVal=20.0,stepType='db',stepSize=[8,4,4,2],nUp=1,nDown=3,nTrials=1)

window = visual.Window([800,600],allowGUI=True,
                       monitor='testMonitor',units='deg')

foil = visual.GratingStim(window,sf=1,size=4,mask='gauss',ori=exp_info['orientation'])
target = visual.GratingStim(window,sf=1,size=4,mask='gauss',ori=exp_info['orientation'])
fixation = visual.GratingStim(window,color=-1,colorSpace='rgb',tex=None,mask='circle',size=0.2)

global_clock = core.Clock()
trial_clock = core.Clock()

msg1 = visual.TextStim(window,pos=[0,3],text='hit any key when ready')
msg2 = visual.TextStim(window,pos=[0,-3],text='then press L or R to identify the probe')

msg1.draw()
msg2.draw()
fixation.draw()

window.flip()#show the new stimuli

event.waitKeys()


for inc in staircase:
    target_side = random.choice([-1,1])
    foil.setPos([5*target_side,0])
    target.setPos([-5*target_side,0])

    foil.setOri(exp_info['orientation']+inc)

    foil.draw()
    target.draw()
    fixation.draw()
    window.flip()

    #core.wait(0.5)

    l_r = get_l_r_blocking()
    
    if l_r is None:
        core.quit()

    correct = int(target_side*l_r == 1)
    correct = -1 if correct == 0 else 1#make it -1 and +1
    print(target_side,l_r,correct)

    staircase.addData(correct)
    Fout.write('%i,%.3f,%i\n'%(target_side,inc,correct))    

print('hello world')

Fout.close()