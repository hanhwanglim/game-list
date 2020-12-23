from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, \
    BooleanField, SubmitField
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    """
    A class that validates sign up form

    Fields:
        email:      Email of the registering user
        username:   Username of the registering user
        password:   Password of the registering user
        confirm:    Repeated password of the registering user
        accept_tos: Checkbox for accepting terms of service
        submit:     Button to submit form
        
    Validation:
        email:      Input required
                    Email must be between 6 to 35 characters
                    Email must be legitimate
        username:   Input required
                    Username must be between 4 to 35 characters
        password:   Input required
                    Password must be minimum 6 characters
                    Password must be same as repeated password
        confirm:    Input required
        accept_tos: Must be checked
    """
    # Labels
    email_label = "Email"
    username_label = "Username"
    password_label = "Enter password"
    confirm_label = "Confirm password"
    tos_label = "I accept the Term of Service and Privacy Policy"
    submit_label = "Create account"

    # Error messages
    email_error = "Invalid email address."
    username_error = "Username must be between 4 and 25 characters long"
    password_error_1 = "Password must be longer than 6 characters."
    password_error_2 = "Passwords must match"

    # Validators
    email_validator = [validators.DataRequired(),
                       validators.Length(min=6, max=35,
                                         message=email_error),
                       validators.Email(message=email_error)]
    username_validator = [validators.DataRequired(),
                          validators.Length(min=4, max=25,
                                            message=username_error)]
    password_validator = [validators.DataRequired(),
                          validators.Length(min=6,
                                            message=password_error_1),
                          validators.EqualTo('confirm',
                                             message=password_error_2)]
    confirm_validator = [validators.DataRequired()]
    tos_validator = [validators.InputRequired()]

    # Render style
    render_email = {'class': 'form-control',
                    'placeholder': "Email address", 'autofocus': ''}
    render_username = {'class': 'form-control',
                       'placeholder': "Username"}
    render_password = {'class': 'form-control',
                       'placeholder': "Password"}
    render_confirm = {'class': 'form-control',
                      'placeholder': "Confirm password"}
    render_submit = {'class': 'w-100 btn btn-lg btn-primary'}

    # Fields
    email = EmailField(email_label, email_validator,
                       render_kw=render_email)
    username = StringField(username_label, username_validator,
                           render_kw=render_username)
    password = PasswordField(password_label, password_validator,
                             render_kw=render_password)
    confirm = PasswordField(confirm_label, confirm_validator,
                            render_kw=render_confirm)
    accept_tos = BooleanField(tos_label, tos_validator)
    submit = SubmitField(submit_label, render_kw=render_submit)


class LoginForm(FlaskForm):
    """ 
    A class that validates login form 
    
    Fields:
        username:   Username of the user
        password:   Password of the user
        remember:   Checkbox to remember user's session
        submit:     Button to submit form
        
    Validation:
        username:   Input required
                    Username must be between 4 to 35 characters
        password:   Input required
    """
    # Labels
    username_label = "Username"
    password_label = "Enter password"
    remember_label = "Remember me?"
    submit_label = "Login"

    # Error messages
    username_error = "Username must be between 4 and 25 characters long."

    # Validators
    username_validator = [validators.DataRequired(),
                          validators.Length(min=4, max=25,
                                            message=username_error)]
    password_validator = [validators.DataRequired()]

    # Render style
    render_username = {'class': 'form-control',
                       'placeholder': username_label, 'autofocus': ''}
    render_password = {'class': 'form-control',
                       'placeholder': "Password"}
    render_submit = {'class': 'w-100 btn btn-lg btn-primary'}

    # Fields
    username = StringField(username_label, username_validator,
                           render_kw=render_username)
    password = PasswordField(password_label, password_validator,
                             render_kw=render_password)
    remember = BooleanField(remember_label)
    submit = SubmitField(submit_label, render_kw=render_submit)


class PasswordForm(FlaskForm):
    """
    A class that validates password when the user changes password
    
    Fields:
        old_password:   Old password for the user
        password:       New password for the user
        confirm:        Repeated new password for the user
        
    Validation:
        old_password:   Input required
        password:       Input required
                        Password must be minimum 6 characters
                        Password must be same as repeated password
        confirm:        Input required
    """
    # Labels
    old_password_label = "Enter old password"
    password_label = "Enter new password"
    confirm_label = "Confirm password"
    submit_label = "Change password"
    # Error messages
    password_error_1 = "Passwords must match."
    password_error_2 = "Password must be longer than 6 characters."

    # Validators
    old_password_validator = [validators.DataRequired()]
    password_validator = [validators.DataRequired(),
                          validators.Length(min=6,
                                            message=password_error_2),
                          validators.EqualTo('confirm',
                                             message=password_error_1)]
    confirm_validator = [validators.DataRequired()]

    # Render style
    render_old_password = {'class': 'form-control',
                           'placeholder': old_password_label,
                           'autofocus': ''}
    render_password = {'class': 'form-control',
                       'placeholder': password_label}
    render_confirm = {'class': 'form-control',
                      'placeholder': confirm_label}
    render_submit = {'class': 'w-100 btn btn-lg btn-primary'}

    # Fields
    old_password = PasswordField(old_password_label,
                                 old_password_validator,
                                 render_kw=render_old_password)
    password = PasswordField(password_label, password_validator,
                             render_kw=render_password)
    confirm = PasswordField(confirm_label, confirm_validator,
                            render_kw=render_confirm)
    submit = SubmitField(submit_label, render_kw=render_submit)
