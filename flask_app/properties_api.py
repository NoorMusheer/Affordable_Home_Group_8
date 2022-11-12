import http.client

conn = http.client.HTTPSConnection("realty-in-us.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "c05b87795bmsh798a906721c803ep1bb0e9jsn76bc358834d6",
    'X-RapidAPI-Host': "realty-in-us.p.rapidapi.com"
    }

conn.request("GET", "/properties/list-for-sale?state_code=NY&city=New%20York%20City&offset=0&limit=10&sort=relevance", headers=headers)

res = conn.getresponse()
data = res.read()

# print(data.decode("utf-8"))

print(data)