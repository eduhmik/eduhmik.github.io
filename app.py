from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user

from mockdbhelper import MockDBHelper as DBHelper
from user import User
import config

DB = DBHelper()

app = Flask(__name__)
app.config.update(dict(
	SECRET_KEY = 'cPY7Cug/sUNI0C8BHtA+Gj3iHj2QhTk6hTJGQopC+NsX1C70Wq'
))

login_manager = LoginManager(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin', methods=["POST"])
def signin():
	email = request.form.get("email")
	password = request.form.get("password")
	user_password = DB.get_user(email)
	if user_password and user_password == password:
		user = User(email)
		login_user(user)
		return redirect(url_for('questions'))
	return index()

@app.route('/questions')
@login_required
def questions():
    return 'You are logged in!'


if __name__ == '__main__':
    app.run(debug=True)