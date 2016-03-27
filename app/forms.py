from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, RadioField
from wtforms.validators import DataRequired


class LoginForm(Form):
    myfield = RadioField('Label', choices=[('10','10'),('100','100')])
