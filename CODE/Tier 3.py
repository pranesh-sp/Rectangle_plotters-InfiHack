#!/usr/bin/env python
# coding: utf-8

# In[127]:


import pandas as pd
df = pd.read_csv('E:\\SW-VLSI\\Input-Dataset\\tier_III\\3_dataset2.csv')


# In[128]:


df


# In[129]:


try:
    smtg = df['Dir (wrt entire design)']
    s = 'Dir (wrt entire design)'
except:
    s = 'Dir (wrt design)'


# In[130]:


import math
sq = math.sqrt(max(df[df[s]=='Any']['Area_of_each_block (mm^2)']))


# In[131]:


df.insert(6, "Priority", [0]*df.shape[0], True)


# In[132]:


df


# In[133]:


for i in range(df.shape[0]):
    tem = df.iloc[i]
    if tem[s] == 'Any':
        j = tem['Group']
        if 'Top' in df[df['Group']==j][s].tolist():
            df.set_value(i, 'Priority', -1)
        if 'Bottom' in df[df['Group']==j][s].tolist():
            df.set_value(i, 'Priority', 1)


# In[134]:


df


# In[135]:


df = df.sort_values(['Priority'])


# In[136]:


df


# In[137]:


Any = df[df[s]=='Any']
blocks = Any['Block_Count'].tolist()
areas = Any['Area_of_each_block (mm^2)'].tolist()
types = Any['Block_Type'].tolist()


# In[138]:


names = []


# In[139]:


plot = []
cur = 0
for i in range(len(blocks)):
    for j in range(blocks[i]):
        plot.append([0, cur])
        cur+=areas[i]/sq
        plot[-1]+=[sq, cur]
        plot[-1]=tuple(plot[-1])
        names.append(types[i])
width = sq


# In[140]:


Right = df[df[s]=='Right']
blocks = Right['Block_Count'].tolist()
areas = Right['Area_of_each_block (mm^2)'].tolist()
types = Right['Block_Type'].tolist()


# In[141]:


AnyHeight = plot[-1][-1]
step = sum(areas[i]*blocks[i] for i in range(len(blocks)))/AnyHeight
cur = 0
for i in range(len(blocks)):
    for j in range(blocks[i]):
        plot.append([sq, cur])
        cur+=areas[i]/step
        plot[-1]+=[sq+step, cur]
        plot[-1] = tuple(plot[-1])
        names.append(types[i])
width+=step


# In[142]:


Left = df[df[s]=='Left']
blocks = Left['Block_Count'].tolist()
areas = Left['Area_of_each_block (mm^2)'].tolist()
types = Left['Block_Type'].tolist()


# In[143]:


step = sum(areas[i]*blocks[i] for i in range(len(blocks)))/AnyHeight
cur = 0
for i in range(len(blocks)):
    for j in range(blocks[i]):
        plot.append([-step, cur])
        cur+=areas[i]/step
        plot[-1]+=[0, cur]
        plot[-1] = tuple(plot[-1])
        names.append(types[i])
width+=step


# In[144]:


Top = df[df[s]=='Top']
blocks = Top['Block_Count'].tolist()
areas = Top['Area_of_each_block (mm^2)'].tolist()
types = Top['Block_Type'].tolist()


# In[145]:


step = sum(areas[i]*blocks[i] for i in range(len(blocks)))/width
leftmost = plot[-1][0]
cur = plot[-1][0]
for i in range(len(blocks)):
    for j in range(blocks[i]):
        plot.append([cur, -step])
        cur+=areas[i]/step
        plot[-1]+=[cur, 0]
        plot[-1] = tuple(plot[-1])
        names.append(types[i])


# In[146]:


Bottom = df[df[s]=='Bottom']
blocks = Bottom['Block_Count'].tolist()
areas = Bottom['Area_of_each_block (mm^2)'].tolist()
types = Bottom['Block_Type'].tolist()


# In[147]:


step = sum(areas[i]*blocks[i] for i in range(len(blocks)))/width
cur = leftmost
for i in range(len(blocks)):
    for j in range(blocks[i]):
        plot.append([cur, AnyHeight])
        cur+=areas[i]/step
        plot[-1]+=[cur, AnyHeight+step]
        plot[-1] = tuple(plot[-1])
        names.append(types[i])


# In[148]:


x = min(min(i[0] for i in plot), min(i[2] for i in plot))
y = min(min(i[1] for i in plot), min(i[3] for i in plot))
x, y


# In[149]:


plot = [(i[0]-x, i[1]-y, i[2]-x, i[3]-y) for i in plot]


# In[150]:


for i in range(len(names)):
    names[i] = names[i]+str(i+1)
    


# In[154]:


positions = []
for i in plot:
    positions.append([])
    for j in i:
        positions[-1].append(41*j)


# In[155]:


lengths = []
breadths = []
area = []
aspect_ratio = []
for i in plot:
    lengths.append(i[2]-i[0])
    breadths.append(i[3]-i[1])
    area.append((i[2]-i[0])*(i[3]-i[1]))
    aspect_ratio.append((i[3]-i[1])/(i[2]-i[0]))


# In[156]:


import rpack
from tkinter import *
import pandas as pd
from tkinter.ttk import *
# positions = [(j*100 for j in i) for i in plot]
root  = Tk()
root.geometry("1000x1000")
myCanvas = Canvas(root, bg="white", height=800, width=800)
# myCanvas.create_rectangle(25, 25, cs[0]+25, cs[1]+25, outline = "#636e72", fill = "#2d3436", width = 5)
for i in range(len(plot)):
    myCanvas.create_rectangle(positions[i][0]+50, positions[i][1]+50, positions[i][2]+50, positions[i][3]+50, outline = "#636e72", fill = "#ffeaa7", width = 1)
    mylabel = myCanvas.create_text((positions[i][2]+positions[i][0])/2 + 50, (positions[i][1]+positions[i][3])/2 + 50, text=names[i].split("_")[1])
mylabel = myCanvas.create_text(350,700, text=" Area= " + str(sum(area)) + " mm^2")
myCanvas.pack()
root.mainloop()


# In[ ]:




