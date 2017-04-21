from init import *
from utility_functions import *

from collections import Counter

def word_to_node_id(word, annotation):
    if word == "ROOT":
        return "ROOT-NNP-0"
    w_ind = annotation['words'].index(word)
    return word+"-"+annotation['pos'][w_ind][1]+"-"+str(w_ind+1) 

def word_id_get_index(word_id):
    return int(word_id.split('-')[2])

def word_id_get_pos(word_id):
    # word_id syntax : (NAME-POS-INDEX ex. test-nnp-3)
    return word_id.split('-')[1]

def word_id_get_word(word_id):
    return word_id.split('-')[0]

def sort_word_ids(word_ids, head_word_ind):
    word_sorted_str = ""
    word_with_pos_sorted_str = ""
    
    word_ids_tuple = map(lambda x: (word_id_get_index(x),x), word_ids)
    word_ids_tuple.sort(key = lambda x: x[0]) #sort based on the first element - which is word's index
    for w in word_ids_tuple:
        if int(w[0]) == int(head_word_ind):
            word_sorted_str += "{" + word_id_get_word(w[1]) + "}" + " "
            word_with_pos_sorted_str += w[1] + " "            
        else:
            word_sorted_str += word_id_get_word(w[1]) + " "
            word_with_pos_sorted_str += w[1] + " "
        
    # removing the extra space at the end
    return word_sorted_str.strip(), word_with_pos_sorted_str.strip()

def expand_rel(rel, g_dir, annotation):
    '''
    Expands arguments by adding extra related words, such as nn, amod, and so on. 
    Expands relations by adding extra related words, such as adverbs, and so on.
    Returns the expanded relation.
    Input: 
    '''
    arg1 = rel['arg1']
    arg2 = rel['arg2']
    r = rel['rel']
    
    arg_expand_list = ['nn', 'amod', 'det', 'neg', 'prep_of', 'num', 'quantmod']
    arg_expand_non_nnp_list = ['infmod', 'partmod', 'ref', 'prepc_of'] #'rcmod' -> it's alwasys connected to nsubj
    rel_expand_list = ['advmod', 'mod', 'aux', 'auxpass', 'cop', 'prt','neg']
    rel_expand_non_SVO_list = ['dobj', 'iobj']
    
    arguments_names = ['arg1', 'arg2']
    '''
    EXPAND ARGUMENTS
    '''
    arg_extra_ids = defaultdict(list)
    arg_head_ind = defaultdict(list)
    for ind, arg_name in enumerate(arguments_names):
        arg = rel[arg_name]
        # add current argument to the extended version
        arg_extra_ids[arg_name].append(arg)
        arg_head_ind[arg_name] = word_id_get_index(arg)
        v_arg_id = arg
        # if it is not a proper noun -> expand more to cover rcmod, infmod, and so on.        
        if word_id_get_pos(v_arg_id) != "NNP": 
            arg_expand_list_final = arg_expand_list + arg_expand_non_nnp_list
        else:
            arg_expand_list_final = arg_expand_list

        g_dir_v = None
        try:
            g_dir_v = g_dir[v_arg_id]
        except:
            print "Faild to get adjacency network of ", v_arg_id, " while expanding it."
            continue
        for word_id, e in g_dir_v.iteritems():
            if e["rel"] in arg_expand_list_final:
                arg_extra_ids[arg_name].append(word_id) 
    
    '''
    EXPAND THE RELATIONSHIP
    '''
    rel_extra_ids = []
    v_rel_id = r
    rel_extra_ids.append(v_rel_id)
    rel_head_ind = word_id_get_index(v_rel_id)
    if rel["type"] != "SVO":
        rel_expand_list_final = rel_expand_list + rel_expand_non_SVO_list
    else:
        rel_expand_list_final = rel_expand_list
    g_dir_v = None
    try:
        g_dir_v = g_dir[v_rel_id]
    except:
        print "Faild to get adjacency network of ", v_rel_id, " while expanding it."
    if g_dir_v is not None:
        for word_id, e in g_dir_v.iteritems():
            if e["rel"] in rel_expand_list_final:
                rel_extra_ids.append(word_id)
    
    arg1_final_word_str, arg1_final_with_pos_str = sort_word_ids(arg_extra_ids[arguments_names[0]], arg_head_ind[arguments_names[0]])
    arg2_final_word_str, arg2_final_with_pos_str = sort_word_ids(arg_extra_ids[arguments_names[1]], arg_head_ind[arguments_names[1]])
    rel_final_word_str, rel_final_with_pos_str = sort_word_ids(rel_extra_ids, rel_head_ind)
    
    
    rel_expanded = rel
    rel_expanded['arg1'] = arg1_final_word_str
    rel_expanded['arg2'] = arg2_final_word_str
    rel_expanded['rel'] = rel_final_word_str
    
    rel_expanded['arg1_with_pos'] = arg1_final_with_pos_str
    rel_expanded['arg2_with_pos'] = arg2_final_with_pos_str
    rel_expanded['rel_with_pos'] = rel_final_with_pos_str
    
    return rel_expanded
    
    
def create_node_attributes(n, annotation):
    '''
    This function takes a node (node_id) and returns its attributes 
    '''
    if n is None:
        return None
    # ROOT does not appear in the tree
    n_att = {}
    if n == "ROOT-NNP-0":
        n_word = "ROOT"
        n_att["word"] = n_word
        n_att["id"] = "ROOT-NNP-0"
        return n_att
    try:
        # extract attributes
        n_word, n_pos, n_ind = n.split('-')[0], n.split('-')[1], n.split('-')[2]        
        n_ind = int(n_ind) - 1 # make it 0 base - ROOT becomes "-1"
    except:
        print error_msg(error_type="tokenizer")
        return None
    #n_pos = annotation['pos'][n_ind][1]
    
    n_att["word"] = n_word
    n_att["ind"] = n_ind
    n_att["pos"] = n_pos
    n_att["id"] = n
    
    return n_att

def dp_str_to_node_id(w_ind_str,pos):
    if w_ind_str == "ROOT-0":
        return "ROOT-NNP-0"
    word = w_ind_str.split('-')[0]
    try:
        word_ind = int(w_ind_str.split('-')[1])-1
        res = word+"-" + pos[word_ind][1] + "-" + str(word_ind+1)
    except:
        print error_msg(error_type="tokenizer")
        return
    return res
    

def create_dep_graph(annotation):
    print " in create_dep_graph function and this is the annotation: ", annotation
    dep_parse = annotation['dep_parse']
    if dep_parse == '':
        return None
    dp_list = dep_parse.split('\n')
    #print dp_list
    pattern = re.compile(r'.+?\((.+?), (.+?)\)')    
    #g = nx.Graph()
    g_dir = nx.DiGraph()
    for dep in dp_list:
        m = pattern.search(dep)
        n1 = dp_str_to_node_id(m.group(1),annotation['pos'])
        n2 = dp_str_to_node_id(m.group(2),annotation['pos'])
        n1_att = create_node_attributes(n1, annotation)
        n2_att = create_node_attributes(n2, annotation)
        if n1_att is None or n2_att is None:
            return None
        
        g_dir.add_node(n1, n1_att)
        g_dir.add_node(n2, n2_att)
        e_rel = dep[:dep.find("(")]
        #edges.append(e)
        g_dir.add_edge(n1, n2, {'rel' : e_rel}, label = e_rel)
    return g_dir

def get_simp_rel(rel, option = "SVO", dataset='mothering'):
    # add options later
    '''
    Lower case, Strip
    '''
    arg1 = word_id_get_word(rel['arg1']).lower().strip()
    arg2 = word_id_get_word(rel['arg2']).lower().strip()
    r = word_id_get_word(rel['rel']).lower().strip()

    '''
    Mapping:
    (I,You,We -> Parents)
    '''    
    if dataset == "mothering":
        parent_list = ["i","you","we","us"]
        if arg1 in parent_list:
            arg1 = "parent"
        if arg2 in parent_list:
            arg2 = "parent"

        child_list = ["child","children","kid","kids","son", "sons","daughter","daughters","toddler","toddlres","boy"]
        if arg1 in child_list:
            arg1 = "child"
        if arg2 in child_list:
            arg2 = "child"    
    '''
    Stemming
    '''
    stemmer = SnowballStemmer("english")
    arg1 = stemmer.stem(arg1) 
    arg2 = stemmer.stem(arg2)
    r = stemmer.stem(r)
    
    rel_simp = rel.copy()
    rel_simp['arg1'] = arg1
    rel_simp['arg2'] = arg2
    rel_simp['rel'] = r
    return rel_simp



def get_relations(g_dir, annotation, option="SVO"):
    relations = []
    '''
    Simplified relations:
    meaning that we only keep head words, do stemming, map words to their actual actor ( I,we,you -> parents)
    '''
    relations_simp = [] 
    if option == "SVO":
        t_verbs = annotation['verbs']
        for v in t_verbs:
            v_id = word_to_node_id(v,annotation)
            try:
                g_dir_v = g_dir[v_id] #adjacency of v_id
            except:
                print v_id, " does not appeared as a separate node in parsing tree."
                continue
            nsubj_list = []
            dobj_list = []
            for word_id, e in g_dir_v.iteritems():
                if e["rel"] == "nsubj":
                    nsubj_list.append(word_id)
                if e["rel"] == "dobj":
                    dobj_list.append(word_id)
            if len(nsubj_list) > 0 and len(dobj_list) > 0:
                for s in nsubj_list:
                    for o in dobj_list:
                        rel = {}
                        rel["rel"] = v_id
                        rel["arg1"] = s#s.split("-")[0]
                        rel["arg2"] = o#o.split("-")[0]
                        rel["type"] = option
                        rel["pattern"] = "(nsubj, verb, dobj)"
                        rel_expanded = expand_rel(rel, g_dir, annotation)
                        relations.append(rel_expanded.copy())
                        rel_simp = get_simp_rel(rel_expanded.copy(),option)
                        relations_simp.append(rel_simp)
    return relations, relations_simp

def create_argument_graph(df, source, target, edge_attr=None, graph_type="directed"):
    ''' Return a graph from Pandas DataFrame.
    Modified version of "from_pandas_dataframe" function.
    '''
    if graph_type == "undirected":
        g = nx.Graph()
    elif graph_type == "directed":
        g = nx.DiGraph()
    else:
        g = nx.MultiGraph()
    
    src_i = df.columns.get_loc(source)
    tar_i = df.columns.get_loc(target)
    label_i = df.columns.get_loc(edge_attr)
    if edge_attr:
        # If all additional columns requested, build up a list of tuples
        # [(name, index),...]
        if edge_attr is True:
            # Create a list of all columns indices, ignore nodes
            edge_i = []
            for i, col in enumerate(df.columns):
                if col is not source and col is not target:
                    edge_i.append((col, i))
        # If a list or tuple of name is requested
        elif isinstance(edge_attr, (list, tuple)):
            edge_i = [(i, df.columns.get_loc(i)) for i in edge_attr]
        # If a string or int is passed
        else:
            edge_i = [(edge_attr, df.columns.get_loc(edge_attr)),]

        # Iteration on values returns the rows as Numpy arrays
        for row in df.values:
            g.add_edge(row[src_i], row[tar_i], label = row[label_i])#{i:row[j] for i, j in edge_i},label=row[label_i])
    
    # If no column names are given, then just return the edges.
    else:
        for row in df.values:
            g.add_edge(row[src_i], row[tar_i])

    return g

def create_argument_multiGraph(df, source, target,edge_attr):

    src_i = df.columns.get_loc(source)
    tar_i = df.columns.get_loc(target)
    label_i = df.columns.get_loc(edge_attr)
    
    g = nx.MultiDiGraph()
    nodes = set()
    nodes = list(nodes.union(df[source],df[target]))
    for n in nodes:
        g.add_node(n)
        ''' Get dataframe in which n is the source'''
        df_n = df[df[source] == n]
        cnt = Counter()
        for row in df_n.values:
            cnt[(row[label_i],row[tar_i])] += 1
        for k,v in cnt.most_common():
            #print n,k,v
            label_rel_freq = str(k[0])+"-"+str(v)
            g.add_edge(n,str(k[1]),label=label_rel_freq)
    return g

def filter_nodes(df,source,target, selected_nodes):
    df_filtered = df[np.logical_and(df[source].isin(selected_nodes), df[target].isin(selected_nodes))]
    return df_filtered

def glob_version(entity, entity_versions):
    '''
    Extraction part -> arg or rel
    Take an argument or relation entry, with a list of the main actors and different versions of the main actors.
    Return the global name for the main actor.
    '''
    entity_new = ""
    entity_new = entity
    entity_new = entity_new.lower()
    entity_head = re.search(r'\{(.*)\}', entity_new).group(1)
    for ent_glob_name, ent_version_list in entity_versions.iteritems():
        if entity_head in ent_version_list:
            entity_new = ent_glob_name
            break
    return entity_new
    
def get_simp_df(df,entity_versions):
    for index, row in df.iterrows():
        # lower case the letters
        arg1_new = glob_version(row['arg1'],entity_versions)
        arg2_new = glob_version(row['arg2'],entity_versions)
        #row['arg1'] = arg1_new
        #row['arg2'] = arg2_new
        df.loc[index,'arg1'] = arg1_new
        df.loc[index,'arg2'] = arg2_new    
    return df


# In[ ]:



