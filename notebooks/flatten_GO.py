#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append('/cellar/users/hmbaghdassarian/Data/Network_Comparison')

import CliXO_Functions as CX
import InfoMap_Functions as IM
import Analysis_Functions as AF


# In[33]:


import requests
import gzip
import numpy as np
import pandas as pd
import networkx as nx
import sys
import pickle
import ddot
from ddot import Ontology
# from goatools import obo_parser
import subprocess

import timeit as timeit


# In[3]:


# # Download GO obo file
r = requests.get('http://purl.obolibrary.org/obo/go/go-basic.obo')
# can download smaller obo in future for benchmark
path = '/cellar/users/hmbaghdassarian/Data/Network_Comparison/Synapse_Final/data/'
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


# In[28]:


ontGO_synapse = ontGO.focus(branches = ['GO:0045202'])
sim_score,gene_name = ontGO_synapse.flatten()

with open(path + 'GO_synapse_ddot_object.pickle', 'wb') as f:
    pickle.dump(ontGO_synapse, f)

synapse_semantic = pd.DataFrame(columns = gene_name, index = gene_name, data = sim_score)
synapse_semantic.to_csv(path + 'GO_synapse_semantic_similarity_matrix.csv')


with open(path + 'GO_synapse_semantic_similarity_list.txt', 'w') as f:
    for row in range((sim_score.shape[0])):
        for column in range((sim_score.shape[1])):
            if column > row:
                f.write(gene_name[column] + '\t' + gene_name[row] + '\t' + str(sim_score[row,column]) + '\n')


# In[77]:


CX_File = 'GO_synapse_semantic_similarity_list.txt'
CXOutput = 'RUN_' + CX_File[:-4]
CX_ONT = CXOutput + 'ONT'
CXE = "/cellar/users/hmbaghdassarian/Software/CliXO-master/clixo"

t0 = timeit.default_timer()
CX.RunCliXO(path,CX_File,CXOutput,CX_ONT, a_ = 5,b_ = 0.1, M_ = 0.0001,z_ = 0.05, 
             CliXOExecutable = CXE)
t1 = timeit.default_timer()
print('time: {:.1f}'.format(t1-t0))


# In[44]:


t = pd.read_csv(path + CX_ONT, sep = '\t', header = None)


# In[64]:


t.head()


# In[66]:


t.loc[20,1]


# In[69]:


import seaborn as sns


# In[76]:


t.groupby(0).agg({'returns' : [np.mean]})


# In[ ]:





# In[ ]:




