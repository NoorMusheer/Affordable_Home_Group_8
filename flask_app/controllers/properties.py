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
    prop_data = property.Property.get_listings_by_max_price(home_data_input)
    print ("***PROP DATA*** : ", prop_data)
    for each in prop_data:
        addr_data = {
            "street_address":each['address_new']['line'],
            "city":each['address_new']['city'],
            "state":each['address_new']['state_code'],
            "zip_code":each['address_new']['postal_code'],
            "type":each['prop_type'],
            "size":each['sqft_raw'],
            "price":int((each['price']).strip('$').replace(",","")),
            "photo":each['photo'],
            "web":each['rdc_web_url'],
            "beds":each['beds'],
            "baths":each['baths'],
            "buyer_id":session['id']
            }
        property.Property.add_to_properties_list(addr_data)
    addresses = property.Property.get_all_properties()
    print("**** ADDRESSES *** :", addresses)
    return render_template('results.html', addresses = addresses)

@app.route ('/dashboard_practice')
def user_dashboard():
    return render_template('practice_user_input.html')

@app.route('/save/<int:id>')
def save_prop(id):
    property.Property.favorited(id)
    addresses = property.Property.get_all_properties()
    return render_template('results.html', addresses = addresses)
