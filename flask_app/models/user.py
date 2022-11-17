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
        self.score = data['score']
        self.down_payment = data['down_payment']

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s ;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result == ():
            return False
        else:
            return result[0]

    @classmethod
    def get_favorited_by_user(cls,id):
        data={
            "id": id
        }
        query = """
            SELECT * FROM properties
            LEFT JOIN users
            ON favorite = 1
            WHERE users.id = %(id)s
        """
        results =  connectToMySQL(cls.db).query_db(query, data)
        print("****RESULTSSSS***** ", results)
        for each in results:
            print("----****---- IDs----****: ", each['id'])
        return results


    @staticmethod
    def validate_reg(data, user_exists, pw_check):
        is_valid = True
        if user_exists:
            flash(
                "**This email is already registered. Please login or create a new account", "register")
            is_valid = False
        if (pw_check['password'] != pw_check['re_enter_password']):
            flash("**Passwords do not match. Please try again. ", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user_exists, user_login_data):
        is_valid = True
        if not user_exists:
            flash("**The entered E-mail does not exist. Please register", "login")
            is_valid = False
        elif not bcrypt.check_password_hash(user_exists['password'], user_login_data['password']):
            flash("** Incorrect password. Please try again. ", "login")
            is_valid = False
        return is_valid

    @staticmethod
    def get_max_price(data):
        n = 360
        r = ((avg_rate/12)+.01)
        P = int(data['P'])
        dn_pmt = int(data['down_payment'])
        max_loan = P*(((1+r)**n)-1) // (r*((1 + r)**n))
        max_price = int(max_loan + dn_pmt)
        if (max_loan > (0.95*(max_price))):
            max_price = int((dn_pmt * 20))
        return max_price
        # print("${:0,.0f}".format(max_price))