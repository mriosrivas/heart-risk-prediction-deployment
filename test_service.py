import requests
import json

user = {'bmi': 23.78,
 'smoking': "yes",
 'alcoholdrinking': "yes",
 'stroke': "yes",
 'physicalhealth': 0.0,
 'mentalhealth': 0.0,
 'diffwalking': "yes",
 'sex': "female",
 'agecategory': "80 or older",
 'race': "black",
 'diabetic': "yes",
 'physicalactivity': "no",
 'genhealth': "good",
 'sleeptime': 7.0,
 'asthma': "no",
 'kidneydisease': "no",
 'skincancer': "no"}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=user)
result = response.json()

print(json.dumps(result, indent=2))
