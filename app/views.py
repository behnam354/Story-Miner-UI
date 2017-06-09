from app import app
from flask import render_template, redirect, jsonify, abort
from .forms import InputForm
import numpy as np
import pandas as pd
from networkx.readwrite.json_graph import node_link_data
import sys
import os
import os.path
import time
import json

pd.set_option('display.max_colwidth', -1)
curdir = os.path.dirname(__file__)
main_functions_dir = None
data_dir = None
if not app.config['USE_NEW_PATH'] \
   or 'MAIN_FUNCTIONS_DIR_NEW' not in app.config \
   or 'DATA_DIR_NEW' not in app.config \
   or not app.config['MAIN_FUNCTIONS_DIR_NEW'] \
   or not app.config['DATA_DIR_NEW']:

	print "main_function_dir_default"
	main_functions_dir = os.path.join(curdir, app.config['MAIN_FUNCTIONS_DIR_DEFAULT'])
	print "data_dir_default"
	data_dir = os.path.join(curdir, app.config['DATA_DIR_DEFAULT'])


else:
	print "main_function_dir_new"
	main_functions_dir = app.config['MAIN_FUNCTIONS_DIR_NEW']
	print "main_function_dir_new"
	data_dir = app.config['DATA_DIR_NEW']


	
sys.path.insert(0, main_functions_dir)
from main_functions import *

'''
PARAMETERS
'''
SEPARATE_SENT = app.config['SEPARATE_SENT']
SHOW_DP_PLOTS = app.config['SHOW_DP_PLOTS']
SHOW_REL_EXTRACTIONS = app.config['SHOW_REL_EXTRACTIONS']
NODE_SELECTION = app.config['NODE_SELECTION']
MAX_ITERATION = app.config['MAX_ITERATION']
SAVE_GEFX = app.config['SAVE_GEFX']
SAVE_PAIRWISE_RELS = app.config['SAVE_PAIRWISE_RELS']
SAVE_ALL_RELS = app.config['SAVE_ALL_RELS']
CLEAN_SENTENCES = app.config['CLEAN_SENTENCES']
SET_INOUT_LOC_FROM_PYTHON_ARGS = app.config['SET_INOUT_LOC_FROM_PYTHON_ARGS']
SHOW_ARGUMENT_GRAPH = app.config['SHOW_ARGUMENT_GRAPH']
EXTRACT_NESTED_PREPOSITIONS_RELS = app.config['EXTRACT_NESTED_PREPOSITIONS_RELS']
DATA_SET = app.config['DATA_SET']
INPUT_DELIMITER = app.config['INPUT_DELIMITER']
SAVE_ANNOTATIONS_TO_FILE = app.config['SAVE_ANNOTATIONS_TO_FILE']
LOAD_ANNOTATIONS = app.config['LOAD_ANNOTATIONS']



@app.route('/' , methods=['GET', 'POST'])

def index():
	form = InputForm()
	if form.validate_on_submit():
		#try:
			tables = None
			titles = None
			graph = None
			graphTitle = None
			state = None
			checkTable = [form.showRels.data,
						form.rankRels.data,
						form.rankEntities.data]
			checkGraph = form.showGraph.data
			
			output = getOutput(form.text.data)
			if output:
				tables, titles, graph, graphTitle = output
				tables = [tables[i] for i, v in enumerate(checkTable) if v == True]
				titles = [titles[i] for i, v in enumerate(checkTable) if v == True]
				if not checkGraph:
					graph = None
					graphTitle = None
				state = "Succeeded!"
			else:
				state = "No relationships extracted." 
			return render_template('index.html',
                                                form = form,
                                                tables = tables,
                                                titles = titles,
                                                graph = graph,
                                                graphTitle = graphTitle,
                                                state = state
                                                )	
		#except:
		#   return abort(500)

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

	df["count"] = df["count"].astype(np.int64)
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

	df["count"] = df["count"].astype(np.int64)
	return df

def getDistinctRels(df_rels):
        if len(df_rels) <= 0:
            return df_rels

        df_keep = df_rels[['arg1', 'arg2','rel']].groupby(['arg1', 'arg2']).agg(lambda x: x.value_counts().index[0])
        df_keep.reset_index(inplace = 1)
        df_keep = df_keep.reindex(columns = ['arg1', 'arg2','rel'])
        keep = df_keep.values.tolist()

        for index, row in df_rels.iterrows():
            if [row['arg1'], row['arg2'], row['rel']] not in keep:
                df_rels.drop(index, inplace = 1)
        return df_rels


def getOutput(text):
	text = text.encode('utf8')
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
	#df_output = pd.DataFrame(output)
	
        print "**************** df_rels ****************"
	print df_rels

	if len(df_rels):
		print len(df_rels)
		df_rels_distinct = getDistinctRels(df_rels)
		print "**************** df_rels_distinct ****************"
		print df_rels_distinct
		g_arg = rels_to_network(df_rels_distinct,
                                        input_fname,
                                        output_dir_arg,
                                        MAX_ITERATION,
                                        NODE_SELECTION,
                                        DATA_SET,
                                        SAVE_GEFX,
                                        SAVE_PAIRWISE_RELS,
                                        SHOW_ARGUMENT_GRAPH   
                                   )

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
		return None




@app.errorhandler(500)

def page_not_found(e):
	return render_template('500.html'), 500   

@app.errorhandler(404)

def page_not_found(e):
	return render_template('404.html'), 404   
