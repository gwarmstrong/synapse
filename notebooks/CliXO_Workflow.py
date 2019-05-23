#!/usr/bin/env python
# coding: utf-8

# A quick tutorial of how these scripts should run
# 
# CliXO Parameters as suggested by Yue
# alpha = between 0.01 and 0.1
# 
# beta = between 0.5 and 0.7
# 
# M = 0.0001 and up a bit
# 
# Z = 0.05 to 0.1

# In[1]:


import CliXO_Functions as CX
from ddot import Ontology
from pathlib import Path
import os


# Input file is tab separated adjacency list with edge weights as final column

# In[2]:


# path = os.path.dirname(os.getcwd()) + '/data/' # path to network file
file = 'EXAMPLE.txt'
# print(path)


# If the edge weights are not greater than 0

# In[3]:


CX_File = CX.ProcessCliXO(file)


# Run CliXO

# In[4]:


CX.RunCliXO(CX_File, a_ = 0.01,b_ = 0.5, M_ = 0.0001,z_ = 0.05)


# DDOT Ont object

# In[6]:


CX_ONT = 'RUN_' + CX_File[0:-4] + 'ONT'


# In[8]:


hierarchy,mapping = CX.CliXO_Parser(CX_ONT)
ont = Ontology(hierarchy, mapping, ignore_orphan_terms=True)

