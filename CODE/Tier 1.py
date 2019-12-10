#!/usr/bin/env python
# coding: utf-8

# In[8]:


import rpack
from tkinter import *
import pandas as pd
from tkinter.ttk import *

data = pd.read_csv("E:/SW-VLSI/Input-Dataset/tier_I/1_dataset2.csv")
print(data)


# In[9]:


list_w = list(data["Width"])
list_h = list(data["Height"])
sizes = []
for i in range(len(list_w)):
    sizes.append((list_w[i],list_h[i]))
    
print(sizes)



# In[10]:


b = '0'*len(sizes)
num = int(b)
Areas = {}
Positions = {}
Sizes = {}
for i in range(2**len(sizes)):
    temp = [list(i) for i in sizes]
    s = bin(num)[2:].zfill(len(sizes))
    for j in range(len(sizes)):
        if s[j]=='1':
            temp[j][1], temp[j][0] = temp[j][0], temp[j][1]
    temp = [tuple(j) for j in temp]
    positions = rpack.pack(temp)
    t = rpack.enclosing_size(temp, positions)
    Areas[s] = t[0]*t[1]
    Positions[s] = positions
    Sizes[s] = temp
    num += 1
mArea = min(Areas.values())
for k, v in Areas.items():
    if v==mArea:
        positions = Positions[k]
        sizes = Sizes[k]
        break
positions


# In[11]:


positions


# In[12]:


sizes


# In[13]:


cs = rpack.enclosing_size(sizes, positions)
root  = Tk()
a = sum(data['Width'])
b = sum(data['Height'])
root.geometry(str(b)+'x'+str(a))
myCanvas = Canvas(root, bg="white", height=cs[1]+50, width=cs[0]+50)
myCanvas.create_rectangle(25, 25, cs[0]+25, cs[1]+25, outline = "#636e72", fill = "#2d3436", width = 5)
for i in range(len(positions)):
    myCanvas.create_rectangle(positions[i][0]+25, positions[i][1]+25, positions[i][0] + sizes[i][0]+25, positions[i][1] + sizes[i][1]+25, outline = "#636e72", fill = "#ffeaa7", width = 1)
    mylabel = myCanvas.create_text((positions[i][0] + (sizes[i][0]/2)+25,positions[i][1] + (sizes[i][1]/2)+25), text=data["Block_Type"][i].split("_")[1])
mylabel = myCanvas.create_text(cs[0]/2 + 25,cs[1]+40, text="Length =" + str(cs[0]) + "  Breadth=" + str(cs[1]) + " Area= " + str(cs[0]*cs[1]) + " mm^2")
myCanvas.pack()
root.mainloop()


# In[ ]:





# In[ ]:




