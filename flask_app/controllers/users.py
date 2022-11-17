from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('login_page.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/reg_page')
def send_to_reg_page():
    return render_template('register_page.html')

@app.route("/register", methods = ["POST"])
def register_user():
    if not user.User.validate_registration(request.form):
        return redirect("/reg_page")

    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : bcrypt.generate_password_hash(request.form["password"]), 
    }
    session["buyer_id"] = user.User.create_user(data) 
    return redirect("/")


# @app.route('/logged_in', methods=['POST'])
# def logged_in_user():
#     user_login_data = {
#         "email": request.form['email'],
#         "password": request.form['password']
#     }
#     user_exists = user.User.get_user_by_email(user_login_data)
#     if not user.User.validate_login(user_exists, user_login_data):
#         return redirect('/')
#     session['id'] = user_exists['id']
#     session['first_name'] = user_exists['first_name']
#     return redirect('/affordablehomes/home')

@app.route('/logged_in', methods=['POST'])
def logged_in_user():
    user_login_data = {
        "email": request.form['email'],
        "password": request.form['password']
    }
    user_exists = user.User.get_user_by_email(user_login_data)
    if not user.User.validate_login(user_exists, user_login_data):
        return redirect('/')
    session['id'] = user_exists['id']
    session['first_name'] = user_exists['first_name']
    return redirect('/affordablehomes/home')

@app.route('/affordablehomes/profile/<int:id>')
def profile_page(id):
    favorites = user.User.get_favorited_by_user(id)
    return render_template('profile_page.html', favorites = favorites)

@app.route('/affordablehomes/condo')
def condo_page():
    return render_template('dashboard_condos.html')


@app.route('/affordablehomes/estimate')
def estimate_page():
    user_info = user.User.get_user_by_id(session['id'])
    return render_template('estimate_page.html', user_info = user_info)
