from django.shortcuts import render

from django.http import HttpResponse

import sys
sys.path.append('/Users/behnam/Desktop/Behnam_Files/vwani_text_mining/RE_Behnam/Story-Miner/final_version_relex')
from ui_test_outputDf import *

def index(request):
    input_sentence = request.POST['comment'] if 'comment' in request.POST else ''
    df_res = get_random_df()
    return render(request, 'index.html', {"input_sentence": input_sentence, "df_res": df_res.to_html()})
    #return HttpResponse("Hello, world. You're at the polls index.")

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
