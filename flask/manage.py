from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    name = StringField(label='username', validators=[DataRequired('username cannt be empty'), Length(min=4, max=20)])
    password = PasswordField(label='password', validators=[DataRequired('password cannt be empty')])
    submit = SubmitField(label='submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mrsoft'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    data = {}
    if form.validate_on_submit():
        data['name'] = form.name.data
        data['password'] = form.password.data

    return render_template('login.html', form=form, data=data)


if __name__ == '__main__':
    app.run(debug=True)
