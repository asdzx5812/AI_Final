#!/usr/bin/env python
# coding: utf-8

# In[43]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
df = pd.read_csv("out1.csv", header=None)


# In[44]:


df.columns = ["Time", "Days", "Susceptible", "Exposed", "Infectious", "Recovered", "Dead"]
df
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
plt.savefig("SIER.png")
plt.show()


# In[ ]:





# In[ ]:




