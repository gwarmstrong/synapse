#!/usr/bin/env python
# coding: utf-8

# In[4]:


import CliXO_Functions as CX

import pickle
import requests
import gzip
import os

import ddot
from ddot import Ontology

import numpy as np
import pandas as pd

import timeit as timeit


# In[5]:


path = os.path.dirname(os.getcwd()) + '/data/' # path to data directory in github synapse repo


# In[7]:


# # Download GO obo file
r = requests.get('http://purl.obolibrary.org/obo/go/go-basic.obo')
# can download smaller obo in future for benchmark

with open(path+'GO_all.obo', 'wb') as f:
    f.write(r.content)

# Parse OBO file
ddot.parse_obo(path+'GO_all.obo', 'go.tab', 'goID_2_name.tab', 'goID_2_namespace.tab', 'goID_2_alt_id.tab')

# Download gene-term annotations for human
r = requests.get('http://geneontology.org/gene-associations/goa_human.gaf.gz')
with open(path + 'goa_human.gaf.gz', 'wb') as f:
    f.write(r.content)
    
hierarchy = pd.read_table('go.tab',
                          sep='\t',
                          header=None,
                          names=['Parent', 'Child', 'Relation', 'Namespace'])
with gzip.open(path + 'goa_human.gaf.gz', 'rb') as f:
    mapping = ddot.parse_gaf(f)

ontGO = Ontology.from_table(
    table=hierarchy,
    parent='Parent',
    child='Child',
    mapping=mapping,
    mapping_child='DB Object ID',
    mapping_parent='GO ID',
    add_root_name='GO:00SUPER',
    ignore_orphan_terms=True)
ontGO.clear_node_attr()
ontGO.clear_edge_attr()

go_descriptions = pd.read_table('goID_2_name.tab',
                                header=None,
                                names=['Term', 'Term_Description'],
                                index_col=0)
ontGO.update_node_attr(go_descriptions)

ontGO = ontGO.collapse_ontology(method='mhkramer')

if 'GO:00SUPER' not in ontGO.terms: ontGO.add_root('GO:00SUPER', inplace=True)


go_branches = pd.read_table('goID_2_namespace.tab',
                                header=None,
                                names=['Term', 'Branch'],
                                index_col=0)
ontGO.update_node_attr(go_branches)


# In[8]:


# retrive all children of GO term 0055202
ontGO_synapse = ontGO.focus(branches = ['GO:0045202'])
# flatten hierarchy
sim_score,gene_name = ontGO_synapse.flatten()


# Create adjacency matrix, adjacency list, and ddot ont object pickle

# ddot pickle
with open(path + 'GO_synapse_ddot_object.pickle', 'wb') as f:
    pickle.dump(ontGO_synapse, f)

# adjacency matrix
synapse_semantic = pd.DataFrame(columns = gene_name, index = gene_name, data = sim_score)
synapse_semantic.to_csv(path + 'GO_synapse_semantic_similarity_matrix.csv')

# adjacency list
with open(path + 'GO_synapse_semantic_similarity_list.txt', 'w') as f:
    for row in range((sim_score.shape[0])):
        for column in range((sim_score.shape[1])):
            if column > row:
                f.write(gene_name[column] + '\t' + gene_name[row] + '\t' + str(sim_score[row,column]) + '\n')


# In[9]:


# Run CliXO on flattened hierarchy and time 
CX_File = 'GO_synapse_semantic_similarity_list.txt'

t0 = timeit.default_timer()
CX.RunCliXO(CX_File, a_ = 0.01,b_ = 0.5, M_ = 0.0001,z_ = 0.05)
t1 = timeit.default_timer()
print('time: {:.1f}'.format(t1-t0))


# In[14]:


# create ontology object from CliXO (useless for recreated, but similar code can be used in future for 
# creating an ontology object from CliXO output on real data)
CX_ONT = 'RUN_' + CX_File[0:-4] + 'ONT'
hierarchy,mapping = CX.CliXO_Parser(CX_ONT)
ont_CX = Ontology(hierarchy, mapping, ignore_orphan_terms=True)

