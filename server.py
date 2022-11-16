from flask_app import app
from flask_app.controllers import users, properties, mtg_rates

if __name__ == "__main__":
    app.run(debug=True)
