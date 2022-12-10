import http.client
import json
from flask_app.controllers import api_requests

conn = http.client.HTTPSConnection("realty-in-us.p.rapidapi.com")

headers = api_requests.headers

conn.request("GET", "/finance/rates?loc=94538", headers=headers)

res = conn.getresponse()
rates_data = res.read()

# print("**********MTG RATES LINE 14**********", rates_data.decode("utf-8"))

parse_json_rates = json.loads(rates_data)
print ("****PARSE JSON RATES ****", parse_json_rates)
print("---***---PARSEJSONRATES---***---: ", parse_json_rates['rates']['average_rate_30_year'])
avg_rate = (float(parse_json_rates['rates']['average_rate_30_year']))*.01

