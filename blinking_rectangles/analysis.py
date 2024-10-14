import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

print('hello world')

data_dir = 'data/'
files = os.listdir(data_dir)

def accept_file(filename):
    if 'VLCollect' in filename:
        return True

    return False

valid_files = [f for f in files if accept_file(f)]

print(valid_files)

df = None

for file in valid_files:
    dfc = pd.read_csv(data_dir+file)
    if df is None:
        df = dfc
    else:
        df = pd.concat([df,dfc],ignore_index=True)


by_gap = {}

for row in df.iterrows():
    gap = row[1]['gap']
    in_out = row[1]['in_out']
    in_out_num = int(in_out == 'in')

    if gap in by_gap:
        by_gap[gap].append(in_out_num)
    else:
        by_gap[gap] = [in_out_num]

xpts = []
ypts = []
spts = []

for gap in by_gap:
    meanval = sum(by_gap[gap]) / len(by_gap[gap])
    stdval = np.std(by_gap[gap])

    xpts.append(gap)
    ypts.append(meanval)
    spts.append(stdval)

fig = plt.figure()
ax = fig.add_subplot()

ax.errorbar(xpts,ypts,spts,linestyle='none',marker='^')
ax.set_xlim([-0.005,0.02])

plt.show()