import requests
url = "https://www.ebay.com/"

response = requests.get(url)

if response.status_code == 200:
    print("Successfully accessed eBay homepage")
else:
    print(f"Failed to access eBay homepage, status code: {response.status_code}")