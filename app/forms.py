from flask_wtf import Form
from wtforms import TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

class InputForm(Form):
    text = TextAreaField('Text',
                         #validators=[DataRequired()],
                         #validators=[Length(max=500)],
                         default='''UCLA Big Data Group introduces Strands. Strands automatically extracts narratives from social media. This demo page shows relationships extracted by Strands. In this demo relationships are in form of (subject, verb, object).

Given the text available in this box as input; automatically Strands extracts narratives. The contents get separated into sentences.
'''
                         
)
    showRels = BooleanField('show relationships', default=True)
    rankRels = BooleanField('rank relationships', default=True)
    rankEntities = BooleanField('rank entities', default=True)
    showGraph = BooleanField('show graph', default=True)
    entityMapping = TextAreaField('entityMapping',
                         #validators=[DataRequired()],
                         #validators=[Length(max=500)],
                         )


    
