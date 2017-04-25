import pandas as pd
import csv
from collections import defaultdict
import nltk
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

csv.field_size_limit(sys.maxsize)   

def get_entity_versions(dataset="mothering"):
    entity_versions = defaultdict(list)
    if dataset=="mothering":
        entity_versions['parents'] = ['parents', 'parent', 'i', 'we' , 'us', 'you']
        entity_versions['children'] = ['child', 'kid', 'kids', 'children', 'daughter', 'daughters',
                                       'son', 'sons', 'toddler',
                                       'toddlers', 'kiddo', 'boy','dd','ds']
        entity_versions['medicalProf'] = ['doctor', 'doctors', 'pediatrician', 
                                           'pediatricians', 'nurse', 'nurses', 'ped', 'md', 'dr']
        entity_versions['government'] = ['government', 'cdc', 'federal', 'feds',
                                         'center for disease control', 'officials',
                                         'politician', 'official', 'law']
        entity_versions['religousInst'] = ['faith', 'religion', 'pastor', 'pastors',
                                            'parish', 'parishes', 'church', 'churches',
                                            'congregation', 'congregations', 'clergy']
        entity_versions['schools'] = ['teacher', 'teachers', 'preschools', 'preschool', 
                                      'school', 'schools', 'class', 
                                      'daycare', 'daycares', 'classes']
        entity_versions['vaccines'] = ['vaccines', 'vax', 'vaccine', 'vaccination', 
                                       'vaccinations', 'shots', 'shot', 'vaxed',
                                       'unvax', 'unvaxed', 'nonvaxed', 'vaccinate',
                                       'vaccinated', 'vaxes', 'vaxing', 'vaccinating',
                                       'substances', 'ingredients']
        entity_versions['exemptions'] = ['exemption', 'exempt']
        entity_versions['VPDs'] = ['varicella', 'chickenpox', 
                                   'flu', 'whooping cough', 'tetanus', 'pertussis', 
                                   'hepatitis', 'polio', 'mumps', 'measles', 'diphtheria']
        entity_versions['adverseEffects'] = ['autism', 'autistic', 'fever', 'fevers',
                                              'reaction', 'reactions', 'infection', 'infections', 'inflammation', 'inflammations',
                                              'pain', 'pains', 'bleeding', 'bruising', 'diarrhea', 'diarrhoea']

    return entity_versions
        

def create_context_names(entity_versions):
    entities = entity_versions.keys()
    contexts = []
    for ind1, ent1 in enumerate(entities):
        for ind2, ent2 in enumerate(entities):
            if ind2 > ind1:
                contexts.append(ent1+"_"+ent2)
    return contexts

def create_file_writer_array(entity_versions, header):
    file_writer = defaultdict()
    entities = entity_versions.keys()
    for ind1, ent1 in enumerate(entities):
        for ind2, ent2 in enumerate(entities):
            if ind2 > ind1:
                file_name = ent1 + "_" + ent2 + ".csv"
                f = open('../../data/Vaccination/mothering_contexts/'+file_name, 'w') 
                file_writer[file_name] = csv.writer(f)
                file_writer[file_name].writerow(header)
    return file_writer

def add_to_context_files(entity_versions, sent, line_to_store):
    sent = sent.decode('utf-8')
    sent = sent.lower()
    words = nltk.word_tokenize(sent)
    entities = entity_versions.keys()
    for ind1, ent1 in enumerate(entities):
        ent1_exist = False
        ent1_versions = entity_versions[ent1]
        for v in ent1_versions:
            if v in words:
                #print "sent: ", sent, "\n\n" , "ent1: ", ent1, " version: ", v, " words: ", words
                ent1_exist = True
                break
        if ent1_exist:
            for ind2, ent2 in enumerate(entities):
                if ind2 > ind1:
                    ent2_exist = False
                    ent2_versions = entity_versions[ent2]
                    for v in ent2_versions:
                        if v in words:
                            #print "sent: ", sent, "\n\n" "ent2: ", ent2, " version: ", v, " words: ", words
                            ent2_exist = True
                            break
                    if ent2_exist:
                        #print sent, " ---- " , ent1 , " " , ent2 
                        file_name = ent1 + "_" + ent2 + ".csv"
                        file_writer[file_name].writerow(line_to_store)



entity_versions = get_entity_versions("mothering")
context_names = create_context_names(entity_versions)
#with open("../../data/Vaccination/mothering_chunks/res/rel_all_cat.csv") as f:
with open("../../data/Vaccination/hoffman_output/exp_3_clean_sep/res_all_cat_clean.csv") as f:
    csv_reader = csv.reader(f, delimiter=',')
    for ind, line in enumerate(csv_reader):
        if ind == 0: #skip the header
            # 0: sent, 1,2,3 -> arg1,rel,arg2, 9,10,11 -> arg1,rel,arg2 prepositions
            file_writer = create_file_writer_array(entity_versions, [line[i] for i in [0,1,2,3,9,10,11]])
            continue
        else:
            try:
                add_to_context_files(entity_versions, line[0], [line[i] for i in [0,1,2,3,9,10,11]])
                if ind % 10000 == 0 :
                    print ind ,  "/" , "689391"#"227660"
            except:
                print "Error in line : ", ind, "\n" , line, " \n --- \n " 


