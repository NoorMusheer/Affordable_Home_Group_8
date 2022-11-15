from flask_app import app
from flask_app.models import user, property
from flask_app.controllers.mtg_rates import avg_rate
from flask import render_template, redirect, session, request

@app.route('/params', methods = ['POST'])
def user_parameters ():
    mtg_data_input = {
        "credit_score":request.form['credit_score'],
        "down_payment":request.form['down_payment'],
        "P": request.form['max_monthly'],
    }
    max_price = user.User.get_max_price(mtg_data_input)
    frmtd_city = (request.form['city']).replace(" ", "_")

    home_data_input = {
        "city":frmtd_city,
        "state":request.form['state'],
        "radius":request.form['radius'],
        "max_price" : max_price
    }
    addresses = property.Property.get_listings_by_max_price(home_data_input)
    return render_template('practice_user_results.html', addresses = addresses)

@app.route ('/dashboard_practice')
def user_dashboard():
    return render_template('practice_user_input.html')