
# coding: utf-8

# In[49]:

import pandas as pd
from collections import defaultdict
import re
import numpy as np

get_ipython().magic(u"run -i 'parameters'")
get_ipython().magic(u"run -i 'main_functions'")
get_ipython().magic(u"run -i 'utility_functions'")


def read_df_rel():
    based_dir = '../data/'
    file_input_name = 'output_relations_child_exemption_svo.csv'
    file_input = based_dir + file_input_name    
    ff = open(file_input)
    delim=","
    df = pd.read_csv(file_input,delimiter=delim,header=0)        
    return df

df_rels = read_df_rel()
entity_versions = get_entity_versions("mothering")
#df_simp = get_simp_df(df_rels.copy(),entity_versions)
ent_medicals = entity_versions['medical prof']

for entity in entity_versions:
    print "-------------------------"
    print "       ", entity
    print "-------------------------"    
    for ent_one_version in entity_versions[entity]:
        print "\n\n**** ", ent_one_version, " ****"
        df_all_versions = defaultdict(list)
        df_one_version = df_rels[np.logical_or(df_rels['arg1'].str.contains(ent_one_version),df_rels['arg2'].str.contains(ent_one_version))]
        list_one_version = df_one_version['rel'].tolist()
        print_top_relations(list_one_version,top_num=-1) 
        #print df_med_version['rel']



# In[53]:

ent_one_version = "vaccines"
df_tmp = df_rels[np.logical_or(df_rels['arg1'].str.contains(ent_one_version),df_rels['arg2'].str.contains(ent_one_version))]
df_tmp


# In[ ]:



