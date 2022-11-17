import http.client
import json
from flask_app.controllers.rand_zips import get_random_zip


headers = {
        'X-RapidAPI-Key': "c05b87795bmsh798a906721c803ep1bb0e9jsn76bc358834d6",
        'X-RapidAPI-Host': "realty-in-us.p.rapidapi.com"
    }
conn = http.client.HTTPSConnection("realty-in-us.p.rapidapi.com")


def get_featured_homes():
    zip = get_random_zip()
    conn.request("GET", "/properties/list-for-sale?state_code=_&city=_&offset=0&limit=6&postal_code=" + str(zip) +"&sort=relevance&radius=50", headers=headers)
    res = conn.getresponse()
    data = res.read()
    parse_json = json.loads(data)
    featured_homes = parse_json['listings']
    return featured_homes

print (get_featured_homes())