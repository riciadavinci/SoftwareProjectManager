from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField
from wtforms.validators import InputRequired, Email, Length, EqualTo
import email_validator

class LoginForm(FlaskForm):
    """
    """
    email_id = EmailField("E-Mail Id", validators=[InputRequired(), Length(max=250), Email(message="Invalid EMail Address", granular_message=True)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=50)])
    remember = BooleanField("Remember me")
