from flask_app import app
from flask_app.controllers import users #properties   #* activate once we build a users or properties controller*

if __name__=="__main__":
    app.run(debug = True)