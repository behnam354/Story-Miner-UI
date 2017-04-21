from init import *

NODE_SELECTION = True
SAVE_GEFX = True
SAVE_PAIRWISE_RELS = True

DATA_SET = "mothering"

def load_df_rels(file_input):
    df = pd.read_csv(file_input,delimiter=',',header=1)        
    return df
    

if NODE_SELECTION:
    # get the list of different versions of an entity. Example : parents,parent,i,we -> parents
    entity_versions = get_entity_versions(DATA_SET)  
    df_rels = load_df_rels("../../data/Vaccination/mothering_chunks/res/rel_all_cat.csv")
    print df_rels.ix[:5, :10]
    exit(0)
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
