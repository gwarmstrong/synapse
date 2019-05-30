#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pathlib import Path
import os
import pickle
from tqdm import trange
import timeit as timeit

import CliXO_Functions as CX
from ddot import Ontology
import ddot

import pandas as pd


# In[20]:


def precision_recall(ont_I, ont_G):
    """Return the precision and recall as defined by CliXO paper given ontology objects of inteferred ontology ont_I
    (CliXO) and gold standard ontology ont_G (GO)"""
    
    ALN = ont_I.align(ont_G)
    ALN = ALN[(ALN['FDR']<0.05)&(ALN['Similarity']>=0.1)]
    
    A = ALN.shape[0]
    I = len(set(ont_I.terms))
    G = len(set(ont_G.terms))
    
    precision = (A/I)
    recall = (A/G)
    
    return precision, recall


# In[2]:


path = os.path.dirname(os.getcwd()) + '/data/' # path to data
scores = pd.read_csv(path + 'similarity_score_predictions_draft_1.csv', header = None)


# In[3]:


# Remove self edges (CliXO probably can't handle)
index = scores[scores[0] != scores[1]].index
scores = scores.loc[index,:]
scores.reset_index(inplace = True, drop = True)

# Generate tab separated adjacency list text file that can be run through CliXO
scores.to_csv(path_or_buf = path+'pCX_similarity_score_predictions_draft_1.txt', 
              sep='\t', index=False, header=False)
    


# In[5]:


# Load GO Synapse ontology object
with open(path + "GO_synapse_ddot_object.pickle", "rb") as f:
    ontGO_synapse = pickle.load(f)

# Assign tab separated adjacency list text file name to variable CX_File, 
# assign ONT file name that will be generated after running CliXO to variable CX_ONT
CX_File = 'pCX_similarity_score_predictions_draft_1.txt'
CX_ONT = 'RUN_' + CX_File[0:-4] + 'ONT'


# In[7]:


pc = pd.DataFrame(columns=['alpha', 'precision', 'recall'])
index = 0

alphas = [0.5,1,0.05,2,1.5,3,0.2]

for alpha in alphas:
    try:
        # run CliXO with specified alpha
        CX.RunCliXO(CX_File, a_ = alpha,b_ = 0.5, M_ = 0.0001,z_ = 0.05)
        t1 = timeit.default_timer()
        print('time: {:.1f}'.format(t1-t0))

        # generate ontology object from generated CliXO ontology
        hierarchy,mapping = CX.CliXO_Parser(CX_ONT)
        ontCX_synapse = Ontology(hierarchy, mapping, ignore_orphan_terms=True)

        # calculate precision recall and 
        precision, recall = precision_recall(ontCX_synapse, ontGO_synapse)
        row = [alpha, precision, recall]
        pc.loc[index, :] = row
        pc.to_csv(path + 'precision_recall_draft_1.csv', sep = '\t')
        index += 1
    except:
        pass

