from flask_app import app
from flask_app.config.mysqlconnectin import connectToMySQL
from flask import flash
from flask_app.controllers.mtg_rates import avg_rate
import http.client
import _json
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "users_properties_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.salary = data['salary']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, salary) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(salary)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @staticmethod
    def get_max_price(data):
        n = 360
        r = (avg_rate/12)
        P = int(data['P'])
        dn_pmt = int(data['down_payment'])
        max_loan = P*(((1+r)**n)-1) // (r*((1 + r)**n))
        max_price = int(max_loan + dn_pmt)
        if (max_loan > (0.95*(max_price))):
            max_price = int((dn_pmt * 20))
        return max_price
        
        # print("---***---HERE IS MAX LOAN AMT ---*** --- : ", max_loan)
        # print("---***---HERE IS MAX PRICE ---*** --- : ", max_price)
        # print("${:0,.0f}".format(max_price))


