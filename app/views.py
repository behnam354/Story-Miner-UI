from app import app
from flask import render_template, redirect, jsonify
from .forms import InputForm
import pandas as pd
from networkx.readwrite.json_graph import node_link_data
import sys
import os

import json

pd.set_option('display.max_colwidth', -1)
path = 'app/Story-Miner/final_version_relex/'
data_dir = "app/Story-Miner/data/"

sys.path.insert(0, path + 'base-codes')
sys.path.insert(0, path + 'data-specific-codes')
sys.path.insert(0, path + 'utility-codes')

from init import *
from main_functions import *
from utility_functions import *




@app.route('/' , methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'] )
def index():
    form = InputForm()
    if form.validate_on_submit():
        try:
            tables, titles, graph, graphTitle = getOutput(form.text.data, form.showDataFrame.data)
            return render_template('index.html',
                                        form = form,
                                        tables = tables,
                                        titles = titles,
                                        graph = graph,
                                        graphTitle = graphTitle
                                        )    
        except:
           return render_template('index.html', form = form)

    return render_template('index.html', form = form)


def get_top_rels(all_rels,top_num=-1):
    df = pd.DataFrame(columns = ['rel', 'count'])
    cnt = Counter()
    for r in all_rels:
        cnt[r] += 1
    if top_num == -1: # means print all
        print "Frequent relations:"
        for letter,count in cnt.most_common():
            print letter, ": ", count
            df.loc[len(df)] = [letter, count]
    else:
        print "top ", top_num, " frequent relations:"
        for letter,count in cnt.most_common(top_num):
            print letter, ": ", count
            df.loc[len(df)] = [letter, count]
    
    return df

def count_entities(entities,top_num=-1):
    df = pd.DataFrame(columns = ['entity', 'count'])
    cnt = Counter()
    for r in entities:
        cnt[r] += 1
    if top_num == -1: # means print all   
        print "Frequent entities:"
        for letter,count in cnt.most_common():
            print letter, ": ", count
            df.loc[len(df)] = [letter, count]
    else:
        print "top ", top_num, " frequent entities:"
        for letter,count in cnt.most_common(top_num):
            print letter, ": ", count
            df.loc[len(df)] = [letter, count]


    return df

def getOutput(text, checkbox):
    '''
    PARAMETERS
    '''
    SEPARATE_SENT = True 
    SHOW_DP_PLOTS = False
    SHOW_REL_EXTRACTIONS = False
    NODE_SELECTION = False
    MAX_ITERATION = -1 #-> to try all
    SAVE_GEFX = True
    SAVE_PAIRWISE_RELS = True
    SAVE_ALL_RELS = False 
    CLEAN_SENTENCES = False
    SET_INOUT_LOC_FROM_PYTHON_ARGS = False
    SHOW_ARGUMENT_GRAPH = False
    EXTRACT_NESTED_PREPOSITIONS_RELS = False
    DATA_SET = "sentence_only"
    INPUT_DELIMITER = "\n"
    SAVE_ANNOTATIONS_TO_FILE = False
    LOAD_ANNOTATIONS = False
    

    print text
    if '\r\n' in text:
        texts = text.split('\r\n')
    elif '\n' in text:
        texts = text.split('\n')
    else:
        texts = [text]
    print texts

    input_fname = 'tweets_textOnly_sample.txt'
    file_input_arg = data_dir + input_fname
    output_dir_arg = data_dir
    start_time = time.time()

    all_rels_str, all_rels, output = text_corpus_to_rels(file_input_arg,
                                                         DATA_SET,
                                                         INPUT_DELIMITER,
                                                         input_fname,
                                                         output_dir_arg,
                                                         MAX_ITERATION,
                                                         CLEAN_SENTENCES,
                                                         SEPARATE_SENT,
                                                         SHOW_DP_PLOTS,
                                                         SHOW_REL_EXTRACTIONS,
                                                         SAVE_ALL_RELS,
                                                         EXTRACT_NESTED_PREPOSITIONS_RELS,
                                                         SAVE_ANNOTATIONS_TO_FILE,
                                                         LOAD_ANNOTATIONS,
                                                         texts = texts
                                                        )   
                                                                                                            
    end_time = time.time()
    print "Relation Extraction Time: ", end_time-start_time , "(seconds) - ", (end_time-start_time)/60, "(min)"
    print "Total number of extracted relations: ", len(all_rels_str)
    df_top = get_top_rels(all_rels_str,top_num=-1) 
    df_rels = pd.DataFrame(all_rels)
    df_output = pd.DataFrame(output)
    print df_rels


    g_arg = rels_to_network(df_rels,
                            input_fname,
                            output_dir_arg,
                            MAX_ITERATION,
                            NODE_SELECTION,
                            DATA_SET,
                            SAVE_GEFX,
                            SAVE_PAIRWISE_RELS,
                            SHOW_ARGUMENT_GRAPH
                           )
    
    
    if len(df_rels):
        entities = list(df_rels['arg1']) + list(df_rels['arg2'])
        df_entities = count_entities(entities,top_num=-1) 
        classes = 'table table-bordered table-hover table-striped '
        return [df_rels[['arg1', 'rel', 'arg2']].to_html(classes=classes),
            df_top.to_html(classes=classes),
            df_entities.to_html(classes=classes)
            ], ["Extracted Relationships",
                "Ranking of the Extractions",
                "Ranking of the Entities"], json.dumps(node_link_data(g_arg)), 'Graph'
    else:
        return ["No relations achieved."]
        
        
