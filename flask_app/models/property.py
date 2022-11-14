from flask_app import app
from flask_app.config.mysqlconnectin import connectToMySQL
from flask import flash
import http.client
import json


class Property:
    DB = "users_properties_schema"

    def __init__(self, p_data):
        self.id = p_data['id']
        self.street_address = p_data['street_address']
        self.city = p_data['city']
        self.zip_code = p_data['zip_code']
        self.propertiescol = p_data['propertiescol']
        self.size = p_data['size']
        self.price = p_data['price']
        self.created_at = p_data['created_at']
        self.updated_at = p_data['updated_at']
        self.buyer_id = p_data['buyer_id']

    @classmethod
    def get_all_properties(cls):
        query = "SELECT * FROM properties;"
        results = connectToMySQL(cls.DB).query_db(query)
        properties = []
        for row in properties:
            properties.append(cls(row))
        return properties

    @classmethod
    def add_to_properties_list(cls, prop_data):
        query = "INSERT INTO properties (street_address, city, state, zip_code, type, price, created_at, updated_at, buyer_id) VALUES (%(street_address)s, %(city)s, %(state)s, %(zip_code)s, %(type)s, %(price)s, NOW(), NOW(), %(buyer_id)s);"
        return connectToMySQL(cls.DB).query_db(query, prop_data)


    @staticmethod
    def get_listings_by_max_price(home_data_input):
        print("___MAX PRICE IS ____:", home_data_input['max_price'])
        conn = http.client.HTTPSConnection("realty-in-us.p.rapidapi.com")
        headers = {
            'X-RapidAPI-Key': "",
            'X-RapidAPI-Host': "realty-in-us.p.rapidapi.com"
            }
        conn.request("GET", "/properties/list-for-sale?state_code=" + str(home_data_input['state']) +"&city=" + str(home_data_input['city']) + "&offset=0&limit=3&sort=relevance&radius="+ str(home_data_input['radius']) + "&price_max=" + str(home_data_input['max_price']) + "", headers=headers)

        res = conn.getresponse()
        data = res.read()
        parse_json = json.loads(data)
        prop_data = parse_json['listings']
        print ("---***---PROP DATA ---***--- :", data)
        addresses = []
        for each in prop_data:
            addr_data = {
                "street_address":each['address_new']['line'],
                "city":each['address_new']['city'],
                "state":each['address_new']['state_code'],
                "zip_code":each['address_new']['postal_code'],
                "type":each['prop_type'],
                "price":int((each['price']).strip('$').replace(",","")),
                "web_url":each['rdc_web_url'],
                "photo_url":each['photo'],
                "buyer_id":1
            }
            Property.add_to_properties_list(addr_data)
            addresses.append(addr_data)
        return addresses

    
