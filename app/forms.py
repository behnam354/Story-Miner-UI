from flask_wtf import Form
from wtforms import TextAreaField, BooleanField
from wtforms.validators import DataRequired

class InputForm(Form):
    text = TextAreaField('Text',
                         validators=[DataRequired()],
                         
                         )
    showDataFrame = BooleanField('showDataFrame', default=False)
