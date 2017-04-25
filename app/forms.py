from flask_wtf import Form
from wtforms import TextAreaField, BooleanField
from wtforms.validators import DataRequired

class InputForm(Form):
    text = TextAreaField('Text',
                         validators=[DataRequired()],
                         default='''Obama is the president of US.
Obama wins the election.
Why Samsung Pay could gain an early lead in mobile payments
Why Samsung Pay could gain an early lead in mobile payments
Why Samsung Pay could gain an early lead in mobile payments
Mobile payment processes that can literally be brought in a back pocket to a customer site will help to keep all payments in the same place
Why Samsung Pay could gain an early lead in mobile payments
yes very much appreciated. I think when you have the correct resolution, Apple Pay live (with no payment limit) (1/2)
'''
                         
)
    showDataFrame = BooleanField('showDataFrame', default=False)
