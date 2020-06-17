#!/usr/bin/env python
# coding: utf-8

# In[43]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, help="input csv name", required=True)
parser.add_argument("-o", type=str, help="output png name", required=True)
# In[44]:

df = pd.read_csv(parser.parse_args().i, header=None)
df.columns = ["Time", "Days", "Susceptible", "Exposed", "Infectious", "Recovered", "Dead"]
index = [i/750 for i in range(len(df["Time"]))]
df["index"] = index


# In[58]:


# multiple line plot
plt.plot( 'index', 'Susceptible', data=df, marker='', color='blue')
plt.plot( 'index', 'Exposed', data=df, marker='', color='pink')
plt.plot( 'index', 'Infectious', data=df, marker='', color='red')
plt.plot( 'index', 'Recovered', data=df, marker='', color='green')
plt.plot( 'index', 'Dead', data=df, marker='', c="black")
#plt.xlim()
plt.xlabel("day")
plt.ylabel("num")
plt.legend()
plt.savefig(parser.parse_args().o)
plt.show()


# In[ ]:





# In[ ]:




