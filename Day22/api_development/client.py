import requests

api_url = "http://127.0.0.1:8000/create_person/"

person_data = {
    "name": "John Doe",
    "age": 30
}

response = requests.post(api_url, json=person_data)
print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())