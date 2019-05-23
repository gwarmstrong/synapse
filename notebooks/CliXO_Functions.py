#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import subprocess
from ddot import Ontology
import networkx as nx


# In[13]:


def ProcessCliXO(inputNetworkPathName, inputNetworkFileName, scaling = True, absolute = True, writeFile = True):

    DF = pd.read_csv(inputNetworkPathName+inputNetworkFileName, sep="\t",header=None)

    # convert scores to float
    if DF[2].dtype != 'float64':
        DF[2] = pd.to_numeric(DF[2])

    # various processing of scores (especially for negative values)
    if absolute == True and scaling == False:
        DF[2] = DF[2].abs()

    elif scaling == True and absolute == True:
        DF[2] = (DF[2]-DF[2].min())/(DF[2].max()-DF[2].min())

    elif scaling == True and  absolute == False:
        DF[2] = (2*((DF[2]-DF[2].min())/(DF[2].max()-DF[2].min())))-1

    outputFileName = 'pCX_' + inputNetworkFileName

    if writeFile == True:
        DF.to_csv(path_or_buf = inputNetworkPathName+outputFileName, sep='\t', index=False, header=False)

    return outputFileName


# In[28]:


def RunCliXO(pathName,CliXOadjList_,CliXOOutput_,CliXOoutputONT_, a_ = 0.01,b_ = 0.5, M_ = 0.0001,z_ = 0.05, 
             CliXOExecutable = "/cellar/users/hmbaghdassarian/Software/CliXO-master/clixo"):


    subprocess.call('{} -i {} -a {} [-b {}] [-M {}] [-z {}] > {}'.format(CliXOExecutable,pathName+CliXOadjList_,a_,b_,M_,z_,pathName+CliXOOutput_),shell = True)
    subprocess.call("grep -v '#' {} > {}".format(pathName+CliXOOutput_,pathName + CliXOoutputONT_),shell=True)
    
    
    


# In[32]:


def CliXO_Parser(pathName = '',fileName = ''):
    DF = pd.read_table(pathName+fileName, names = ['parent','child','category','score'])
    DF_hierarchy = DF[DF['category'] != 'gene']
    DF_hierarchy['parent'] = DF_hierarchy['parent'].astype(str)
    parent_hierarchy = DF_hierarchy['parent'].tolist()
    child_hierarchy = DF_hierarchy['child'].tolist()
    hierarchy = list(zip(child_hierarchy,parent_hierarchy))

    DF_mapping = DF[DF['category'] == 'gene']
    DF_mapping['parent'] = DF_mapping['parent'].astype(str)
    parent_mapping = DF_mapping['parent'].tolist()
    child_mapping = DF_mapping['child'].tolist()
    mapping = list(zip(child_mapping,parent_mapping))

    return hierarchy,mapping

