#encoding=utf-8
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, SelectField, BooleanField, DateField
from wtforms.validators import InputRequired

class IndexForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    date = DateField("Datum", validators=[InputRequired()])
    offer = StringField("Essensliste", validators=[InputRequired()])
    submit = SubmitField('Erstellen')

class WurstOrderForm(FlaskForm):
    mycount = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    name = StringField('Name', validators=[InputRequired()])
    bratwurst = SelectField('Bratwurst: 1€', choices=mycount, validators=[InputRequired()])
    schinkengriller = SelectField('Schinkengriller: 1,50€', choices=mycount, validators=[InputRequired()])
    broetchen = BooleanField("Willste Brötchen?", default=True, validators=[InputRequired()])
    selbstversorger = BooleanField('Bringe selber etwas!', default=False, validators=[InputRequired()])
    submit = SubmitField('Bestellen')
    
    
class DeleteOrderForm(FlaskForm):
    delete_secret = StringField('Parole', validators=[InputRequired()])
    confirm_delete = BooleanField('Ich weiß was ich tue und will das löschen!', default=False, validators=[InputRequired()])
    submit = SubmitField('Löschen!')

