#!/usr/bin/env python
# coding: utf-8

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
import Analysis_Functions as AF


# In[2]:


import pandas as pd
import subprocess
from ddot import Ontology
import networkx as nx


# Input file is tab separated adjacency list with edge weights as final column

# In[3]:


path = 'data/toy_data/'
file = 'CliXO_pub_example.txt'


# If the edge weights are not between [0,1]

# In[4]:


CX_File = CX.ProcessCliXO(path, file, scaling = True, absolute = True, writeFile = True)


# Run CliXO

# In[5]:


CXOutput = 'RUN_' + CX_File[:-4]
CX_ONT = CXOutput + 'ONT'
CXE = "/cellar/users/hmbaghdassarian/Software/CliXO-master/clixo"



CX.RunCliXO(path,CX_File,CXOutput,CX_ONT, a_ = 0.01,b_ = 0.5, M_ = 0.0001,z_ = 0.05, 
             CliXOExecutable = CXE)


# DDOT Ont object

# In[6]:


hierarchy,mapping = CX.CliXO_Parser(path,CX_ONT)
ont = Ontology(hierarchy, mapping, ignore_orphan_terms=True)


# In[14]:


n_layersCX,flowCX = AF.EnumeratePaths(ont)


# In[ ]:




