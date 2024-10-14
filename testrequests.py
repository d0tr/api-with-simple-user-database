import requests

BASE = 'http://127.0.0.1:5000/'

response = requests.put(BASE + 'user/1', {'user_id': '1', 'name': 'test_name', 'password':'test_password', 'email': 'test_email@gmail.com'}) #change accordingly to the request type and information needed
print("response text:", response.text)
print(response.json())
