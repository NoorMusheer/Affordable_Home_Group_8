from flask_app import app
from flask_app.controllers import users, properties, mtg_rates, rand_zips, api_requests

if __name__ == "__main__":
    app.run(debug=True)
