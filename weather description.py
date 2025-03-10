import requests as req

url="https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
response = req.get(url+"?dataType=flw&lang=tc")
n=eval(response.text)
print(type(n))
print(n["generalSituation"])
print(n["updateTime"])