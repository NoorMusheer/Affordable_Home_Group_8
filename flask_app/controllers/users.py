from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login_page.html')

@app.route('/reg_page')
def send_to_reg_page():
    return render_template('register_page.html')

@app.route('/register', methods=['POST'])
def register_user():
    data ={
        "first_name":request.form['first_name'], 
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password']),
    }
    pw_check = {
        "password":request.form['password'],
        "re_enter_password":request.form['re_enter_password']
    }
    user_exists = user.User.get_user_by_email(data)
    if not user.User.validate_reg(data, user_exists, pw_check):
        return redirect ('/reg_page')
    user.User.create_user(data)
    return redirect ('/')

@app.route('/logged_in', methods=['POST'])
def logged_in_user():
    user_login_data = {
        "email":request.form['email'],
        "password":request.form['password']
        }
    user_exists = user.User.get_user_by_email(user_login_data)
    if not user.User.validate_login(user_exists, user_login_data):
        return redirect('/')
    return redirect('/dashboard')


@app.route('/dashboard')
def main_page():
    return render_template('dashboard.html')
