from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user

from mockdbhelper import MockDBHelper as DBHelper
from user import User
from passwordhelper import PasswordHelper
import config

DB = DBHelper()
PH = PasswordHelper()

app = Flask(__name__)
app.config.update(dict(
	SECRET_KEY = 'cPY7Cug/sUNI0C8BHtA+Gj3iHj2QhTk6hTJGQopC+NsX1C70Wq'
))

login_manager = LoginManager(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods = ["GET", "POST"])
def signup():
	username = request.form.get("username")
	email = request.form.get("email")
	pwd1 = request.form.get("password")
	pwd2 = request.form.get("password2")
	if not pwd1 == pwd2 and DB.get_user(email):
		return redirect(url_for('signup'))
	salt = PH.get_salt()
	hashed = PH.get_hash(str(pwd1) + str(salt))
	DB.add_user(username, email, salt, hashed)
	return render_template('signup.html')
@app.route('/signin', methods= ['GET','POST'])
def signin():
	if request.method == 'POST':
		return render_template('signin.html')
	email = request.form.get("email")
	password = request.form.get("password")
	stored_user = DB.get_user(email)
	user_password = DB.get_user(email)
	if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
		user = User(email)
		login_user(user, remember=True)
		return redirect(url_for('questions'))
	return render_template('signin.html')

@login_manager.user_loader
def load_user(user_id):
	user_password = DB.get_user(user_id)
	if user_password:
		return User(user_id)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/questions')

def questions():
    return render_template('questions.html')


if __name__ == '__main__':
    app.run(debug=True)