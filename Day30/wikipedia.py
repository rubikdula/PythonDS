import requests
url="https://en.wikipedia.org/"

try:
    response=requests.get(url)
    response.raise_for_status()
    print("respone.text")
except requests.exceptions.RequestException as req_err:
    print(f"Request error: {req_err}")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error: {http_err}")

except requests.exceptions.time as conn_err:
    print(f"Connection error: {conn_err}")