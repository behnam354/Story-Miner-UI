from init import *
from main_functions import *
from utility_functions import *
import sys
import os

SEPARATE_SENT = False 
SHOW_DP_PLOTS = False
SHOW_REL_EXTRACTIONS = False
NODE_SELECTION = True
MAX_ITERATION = -1 #-1 -> to try all
SAVE_GEFX = True
SAVE_PAIRWISE_RELS = True
SAVE_ALL_RELS = False 
CLEAN_SENTENCES = False


#nltk.data.path.append("/media/data5/behnam/nltk_data");

annotator = Annotator()

data_dir = "../../data/"
file_input_arg = str(sys.argv[1])
output_dir_arg = str(sys.argv[2])


input_fname = os.path.basename(file_input_arg)
input_fname = str(input_fname.split(".")[0])

print input_fname

f_rel = open(output_dir_arg+input_fname+"_"+"relations_" + str(MAX_ITERATION) +".csv", "w")

header = ['sentence','arg1','rel','arg2','type','pattern','arg1_with_pos','rel_with_pos','arg2_with_pos','arg1_prepositions', 'rel_prepositions', 'arg2_prepositions']
dict_writer = csv.DictWriter(f_rel, header)
dict_writer.writeheader()#writerow(header)


'''
PARAMETERS
'''
DATA_SET = "mothering"
texts = []

if DATA_SET == "twitter":
    based_dir = data_dir+ 'Tweets/'
    file_input_name = 'sample.csv'
    file_input = based_dir + file_input_name      
    df = read_data(file_input,"twitter",",")#read the input sentences
    texts = df['main_tweet'].tolist()
    
elif DATA_SET == "mothering":
    based_dir = data_dir + 'Vaccination/'
    file_input_name = 'sents.txt'
    #file_input_name = 'sent_cdb_child_exemption.txt'
    file_input = based_dir + file_input_name
    # file_input is extra - should be removed later
    df = read_data(file_input_arg,"mothering","\n")#read the input sentences
    texts = df['text'].tolist()
    #print len(texts)
    #print texts[0:1]



'''
A few sample test cases:
#texts = ["the Church told all Catholic parents not to let their child get the MMR."]
#texts = ["Why Samsung Pay could gain an early lead in mobile payments."]
#texts = ["You would keep your child 's shot records at home and NOT submit that to the school...only your exemption from all shots ."]
#texts = ["Parents may use their philosophical beliefs exemption for ANY vaccine they choose to do so ; you may selectively vaccinate your child and exempt them out of other vaccines ; you may also exempt out of any and all vaccines and use your exemption that way , as well ."]
#texts = ["Here is the Hawaii immunization brochure , which states the exemption forms can also be obtained from the school : Immunization and TB code : Surprisingly , I do n't see anything about religiously exempting a child from the TB screening requirement in the code ."]
#texts.insert(0,"I like this product and I also like the other product.") ! Strange dep res -> prep_like
#texts.insert(0,"A medical exemption is out of the question - you 'd have to first find a doctor willing to exempt your child from all shots - not going to happen - and then have the medical exemption renewed every year . ") -> tokenizer failure
#texts.insert(0,"A state exemption is only to exempt a child from state requirements ; while in the states , the only time an exemption would come up is when using DODs schools or daycare in the states--the OP is going to Japan . ")
#texts.insert(0,"Even if the Church told all Catholic parents not to let their child get the MMR for instance , most parents would have to still be required to submit a religous exemption which would exempt all vaccines .")
'''
#texts.insert(0,"He doesn't like to buy food.")
all_rels_str = []
all_rels = []
output = []

start_time = time.time()
for ind, t_orig in enumerate(texts):
    if MAX_ITERATION >= 0:
        if ind > MAX_ITERATION:
            break
    t_sentences = []
    try:
        if CLEAN_SENTENCES:
            t_orig = clean_sent(t_orig)
        if SEPARATE_SENT:
            t_sentences = sent_tokenize(t_orig)
        else:
            t_sentences = [t_orig]
    except:
        print "Error in sentence tokenizer! - ", t_orig
    #print "number of sentences: ", len(t_sentences)
    for t in t_sentences:
        try:
            t_annotated = annotator.getAnnotations(t, dep_parse=True)
        except:
            print "Error in sentence annotation"
            continue
        try:
            g_dir = create_dep_graph(t_annotated)
            if g_dir is None:
                print "No extraction found"
                continue
            if SHOW_DP_PLOTS:
                plot_dep(g_dir,t)
            g_undir = g_dir.to_undirected()
        except:
            print "Unexpected error while extracting relations:", sys.exc_info()[0]
            continue
        rels_pure, rels_simp = get_relations(g_dir, t_annotated, option="SVO")
        rels = rels_pure#rels_simp
        if SHOW_REL_EXTRACTIONS:
            print ind, t, "\n"
            print "Simplifided Version:"
            print_relations(rels)
            print "More detailed Version:"
            print_relations(rels_pure)
        else:
            print ind,
        all_rels_str = all_rels_str + get_rels_str(rels) #For simply counting the exact strings
        all_rels = all_rels + rels # to later create a dataframe
        for r in rels:
            output_row = defaultdict(list)
            output_row = r.copy()
            #output_row["original_text"] = t_orig
            output_row["sentence"] = t
            output.append(output_row)
            #print " output is : ", output
            #output_subset = dict((k,output[k]) for k in header)
            dict_writer.writerow(output_row)


end_time = time.time()
print "Relation Extraction Time: ", end_time-start_time , "(seconds) - ", (end_time-start_time)/60, "(min)"
print "***************STATISTICS***************"
print "Total number of input records (posts): ", len(texts)
print "Total number of extracted relations: ", len(all_rels_str)
print_top_relations(all_rels_str,top_num=-1) 

df_rels = pd.DataFrame(all_rels)
df_output = pd.DataFrame(output)
print df_output

if SAVE_ALL_RELS:
    columns = ['sentence','arg1','rel','arg2','type','pattern','arg1_with_pos','rel_with_pos','arg2_with_pos']
    df_output.to_csv(output_dir_arg + input_fname + "_" + "output_relations.csv",sep=',', encoding='utf-8',header=True, columns=columns)
    #save_df_rels(df_rels)


#'''
if NODE_SELECTION:
    # get the list of different versions of an entity. Example : parents,parent,i,we -> parents
    entity_versions = get_entity_versions(DATA_SET)    
    df_simp = get_simp_df(df_rels.copy(),entity_versions)  
    selected_nodes = entity_versions.keys()
    df_rels_selected = filter_nodes(df_simp.copy(),source='arg1',target='arg2',selected_nodes = selected_nodes)
    g_arg = create_argument_multiGraph(df_rels_selected.copy(),source='arg1',target='arg2',edge_attr = 'rel')
    if SAVE_GEFX:
        nx.write_gexf(g_arg, output_dir_arg + input_fname + "_" + "g_arg_selected_"+str(MAX_ITERATION)+"_"+str(time.time())+".gexf")
    plot_argument_graph(g_arg)
    if SAVE_PAIRWISE_RELS:
        file_loc = output_dir_arg + input_fname + "_" + "pairwise_rels_selected_"+str(MAX_ITERATION)+"_"+DATA_SET+".txt"
        save_pairwise_rels(file_loc,g_arg,print_option=True)      

g_arg = create_argument_multiGraph(df_rels.copy(),source='arg1',target='arg2',edge_attr = 'rel')
if SAVE_GEFX:
    nx.write_gexf(g_arg, output_dir_arg + input_fname + "_" + "g_arg_"+str(MAX_ITERATION)+"_"+str(time.time())+".gexf")
plot_argument_graph(g_arg)
if SAVE_PAIRWISE_RELS:
    file_loc = output_dir_arg + input_fname + "_"  + "pairwise_rels_"+str(MAX_ITERATION)+"_"+DATA_SET+".txt"
    save_pairwise_rels(file_loc,g_arg,print_option=True)    
    
#if __name__ == "__main__":
#    main(sys.argv[1:])
#'''

'''
# In[68]:

entity = "government"
df_simp[np.logical_and(df_simp['arg1']==entity,df_simp['arg2']==entity)]


# In[74]:

selected_nodes = entity_versions.keys()
df_rels_selected = filter_nodes(df_simp.copy(),source='arg1',target='arg2',selected_nodes = selected_nodes)
g_arg = create_argument_multiGraph(df_rels_selected.copy(),source='arg1',target='arg2',edge_attr = 'rel')
if SAVE_GEFX:
    nx.write_gexf(g_arg, "../gephi_data/g_arg_selected_2_"+str(MAX_ITERATION)+"_"+str(time.time())+".gexf")
plot_argument_graph(g_arg)
if SAVE_PAIRWISE_RELS:
    file_loc = "../data/pairwise_rels_selected_2_"+str(MAX_ITERATION)+"_"+DATA_SET+".txt"
    save_pairwise_rels(file_loc,g_arg,print_option=True)  


# In[72]:

df_rels_selected


<<<<<<< HEAD
# In[4]:

#t_orig = "Fortunately MN does not have a complicated exemption process when you do need one : If a notarized statement signed by the minor child 's parent or by the emancipated person is submitted to the person having supervision of the school or child care facility stating that the person has not been immunized as prescribed because of the conscientiously held beliefs of the parent of the minor child or of the emancipated person , the immunizations specified in the statement shall not be required ."
from nltk.tokenize import sent_tokenize
from practnlptools.tools import Annotator
annotator = Annotator()
t_orig = "OUR RELIGION FORBIDS INJECTIONS AND WE WILL SUE YOU IF YOU DO NOT RESPECT THAT."# and we just submitted a religious exemption to the school she will be attending this fall ."#"The principal opposition parties boycotted the polls after accusations of vote-rigging , and the only other name on the ballot was a little-known challenger from a marginal political party."
=======
# In[6]:

#t_orig = "Fortunately MN does not have a complicated exemption process when you do need one : If a notarized statement signed by the minor child 's parent or by the emancipated person is submitted to the person having supervision of the school or child care facility stating that the person has not been immunized as prescribed because of the conscientiously held beliefs of the parent of the minor child or of the emancipated person , the immunizations specified in the statement shall not be required ."
t_orig = "I 'd have to put it on my own words though or I d never remember what to say ~ laughs ~ ... how about...  Although vaccinations are required by law to attend school , there are simple , legal , ways to exempt your child from that requirement... in Colorado you can get an exemption for medical , religious , or even philisophical reasons .# and we just submitted a religious exemption to the school she will be attending this fall ."#"The principal opposition parties boycotted the polls after accusations of vote-rigging , and the only other name on the ballot was a little-known challenger from a marginal political party."
>>>>>>> 2a590baaf7cacdffd51ad85f31ca0576e25d798c
t_orig = t_orig.replace("-"," ")
t_sentences = sent_tokenize(t_orig)
for t in t_sentences:
    print t
    t_annotated = annotator.getAnnotations(t, dep_parse=True)
    print t_annotated
    dep = t_annotated['dep_parse']
    g_dir = create_dep_graph(t_annotated)
    if g_dir is None:
        print "No extraction found"
        continue
    #if SHOW_DP_PLOTS:
    plot_dep(g_dir,t)
    g_undir = g_dir.to_undirected()
    rels_pure, rels_simp = get_relations(g_dir, t_annotated, option="SVO")
    print rels_pure
    print "simplified"
    print rels_simp


# In[ ]:

2+2


# In[20]:

t_annotated['srl']


# In[24]:

df_rels


# In[ ]:

'''

