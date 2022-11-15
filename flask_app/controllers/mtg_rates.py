import http.client
import json

conn = http.client.HTTPSConnection("realty-in-us.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "c05b87795bmsh798a906721c803ep1bb0e9jsn76bc358834d6",
    'X-RapidAPI-Host': "realty-in-us.p.rapidapi.com"
    }

conn.request("GET", "/mortgage/v2/check-rates?postal_code=94538", headers=headers)

res = conn.getresponse()
rates_data = res.read()

# print(rates_data.decode("utf-8"))

parse_json_rates = json.loads(rates_data)
# print("---***---PARSEJSONRATES---***---: ", parse_json_rates['data']['loan_analysis']['market']['mortgage_data']['average_rates'][0]['rate'])
avg_rate = parse_json_rates['data']['loan_analysis']['market']['mortgage_data']['average_rates'][0]['rate']

