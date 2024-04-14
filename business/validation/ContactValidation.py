from wtforms import Form, BooleanField, StringField, PasswordField, validators



class ContactForm(Form):
    fname = StringField('First Name', [validators.DataRequired()])
    lname = StringField('Last Name', [validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    comment = StringField('Comment', [validators.Length(max=240)])