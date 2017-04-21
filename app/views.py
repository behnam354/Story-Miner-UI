from app import app
from flask import render_template, redirect
from .forms import InputForm
import pandas as pd


import sys
import os

path = 'app/Story-Miner-master/Story-Miner-master/final_version_relex/'
data_dir = "app/Story-Miner-master/data/"

sys.path.insert(0, path + 'base-codes')
sys.path.insert(0, path + 'data-specific-codes')
sys.path.insert(0, path + 'utility-codes')

from init import *
from main_functions import *
from utility_functions import *

'''
PARAMETERS
'''
SEPARATE_SENT = False 
SHOW_DP_PLOTS = False
SHOW_REL_EXTRACTIONS = False
NODE_SELECTION = False
MAX_ITERATION = 4 #-1 -> to try all
SAVE_GEFX = False
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


@app.route('/' , methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'] )
def index():
    form = InputForm()
    if form.validate_on_submit():
        output = getOutput(form.text.data, form.showDataFrame.data)
        return render_template('index.html',
                               form = form,
                               table = output)    
    return render_template('index.html',
                           form = form)


def getOutput(text, checkbox):
    if SET_INOUT_LOC_FROM_PYTHON_ARGS:
        file_input_arg = str(sys.argv[1])
        output_dir_arg = str(sys.argv[2])
        input_fname = os.path.basename(file_input_arg)
        input_fname = str(input_fname.split(".")[0])
        output_prefix = output_dir_arg + input_fname
    else:
        if LOAD_ANNOTATIONS:
            input_fname = 'sents_1_relations_4'#'sents_1'
            file_input_arg = '/Users/behnam/Desktop/Behnam_Files/vwani_text_mining/RE_Behnam/data/Tweets/'+input_fname+'.csv'
            output_dir_arg = '/Users/behnam/Desktop/Behnam_Files/vwani_text_mining/RE_Behnam/data/Tweets/'
        else:
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
                                                         LOAD_ANNOTATIONS
                                                        )   
                                                                                                            
    end_time = time.time()
    print "Relation Extraction Time: ", end_time-start_time , "(seconds) - ", (end_time-start_time)/60, "(min)"
    print "Total number of extracted relations: ", len(all_rels_str)
    print_top_relations(all_rels_str,top_num=-1) 
    df_rels = pd.DataFrame(all_rels)
    df_output = pd.DataFrame(output)

    print df_rels
    return df_rels[['arg1', 'rel', 'arg2']].to_html(classes='table table-bordered table-striped table-hover table-condensed table-responsive')
