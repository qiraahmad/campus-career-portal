from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, StringField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo, ValidationError
import phonenumbers


## login and registration

class LoginForm(FlaskForm):
    email = TextField    ('Email', id='email_login'   , validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateRecruiterForm(FlaskForm):
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    full_name = TextField('FullName'     , id='fullname_create' , validators=[DataRequired()])
    company_name = TextField('CompanyName'     , id='companyname_create' , validators=[DataRequired()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    contact_number = StringField('Phone', validators=[DataRequired()])

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
    
