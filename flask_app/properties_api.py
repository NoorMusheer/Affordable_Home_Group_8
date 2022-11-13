import http.client
import json
import price

conn = http.client.HTTPSConnection("realty-in-us.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "",
    'X-RapidAPI-Host': "realty-in-us.p.rapidapi.com"
    }

conn.request("GET", "/properties/list-for-sale?state_code=CA&city=Fremont&offset=0&limit=3&sort=relevance&price_max=" + str(price.max_price) + "", headers=headers)

res = conn.getresponse()
data = res.read()

# print(data.decode("utf-8"))

parse_json = json.loads(data)

prop_data = parse_json['listings']
for each in prop_data:
    print(each['address'])
    print(each['price'])


