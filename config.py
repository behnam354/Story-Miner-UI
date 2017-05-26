# Config must be UPPERCASE!!!

# security
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# local
LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 5000

# serve
SERVE_HOST = '0.0.0.0'
SERVE_PORT = 5000

# backend default path
MAIN_FUNCTIONS_DIR_DEFAULT = 'Story-Miner/final_version_relex/base-codes/'
DATA_DIR_DEFAULT = 'Story-Miner/data/'



# replace default path with new absolute path
MAIN_FUNCTIONS_DIR_NEW = '' 
DATA_DIR_NEW = ''


# parameters
SEPARATE_SENT = True 
SHOW_DP_PLOTS = False
SHOW_REL_EXTRACTIONS = False
NODE_SELECTION = False
MAX_ITERATION = -1 #-> to try all
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
