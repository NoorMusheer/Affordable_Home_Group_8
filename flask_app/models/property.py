from flask_app import app
from flask_app.config.mysqlconnectin import connectToMySQL
from flask_app.controllers import api_requests
from flask import flash
import http.client
import json


class Property:
    db = "users_properties_schema"

    def __init__(self, p_data):
        self.id = p_data['id']
        self.street_address = p_data['street_address']
        self.city = p_data['city']
        self.state = p_data['state']
        self.zip_code = p_data['zip_code']
        self.type = p_data['type']
        self.size = p_data['size']
        self.price = p_data['price']
        self.favorite = p_data['favorite']
        self.photo = p_data['photo']
        self.web = p_data['web']
        self.beds = p_data['beds']
        self.baths = p_data['baths']
        self.lot_size = p_data['lot_size']
        self.created_at = p_data['created_at']
        self.updated_at = p_data['updated_at']
        self.buyer_id = p_data['buyer_id']

    @classmethod
    def get_all_properties(cls):
        query = "SELECT * FROM properties WHERE favorite IS NULL;"
        results = connectToMySQL(cls.db).query_db(query)
        properties = []
        for row in results:
            properties.append(row)
        return properties


# sss

    @classmethod
    def add_to_properties_list(cls, prop_data):
        query = "INSERT INTO properties (street_address, city, state, zip_code, type, size, price, photo, web, beds, baths, created_at, updated_at, buyer_id) VALUES (%(street_address)s, %(city)s, %(state)s, %(zip_code)s, %(type)s, %(size)s, %(price)s, %(photo)s, %(web)s, %(beds)s, %(baths)s, NOW(), NOW(), %(buyer_id)s);"
        return connectToMySQL(cls.db).query_db(query, prop_data)

    @classmethod
    def delete_prev_results(cls):
        query = "DELETE FROM properties WHERE favorite IS NULL;"
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def favorited(cls, save_data):
        query = """
            UPDATE properties
            SET favorite = 1, buyer_id = %(user_id)s
            WHERE id = %(prop_id)s;
            """
        return connectToMySQL(cls.db).query_db(query, save_data)

    @classmethod
    def remove_fav(cls, id):
        data={
            "id":id
        }
        query = """
            UPDATE properties
            SET favorite = 0
            WHERE id = %(id)s
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def get_listings_by_max_price(home_data_input):
        Property.delete_prev_results()
        conn = http.client.HTTPSConnection("realty-in-us.p.rapidapi.com")

        headers = api_requests.headers
        
        conn.request("GET", "/properties/list-for-sale?state_code=" + str(home_data_input['state']) + "&city=" + str(
            home_data_input['city']) + "&offset=0&limit=25&sort=relevance&radius=" + str(home_data_input['radius']) + "&price_max=" + str(home_data_input['max_price']) + "", headers=headers)

        res = conn.getresponse()
        data = res.read()
        parse_json = json.loads(data)
        prop_data = parse_json['listings']
        return prop_data

