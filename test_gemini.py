import requests

API_KEY = "AIzaSyDPfG5-gjeGyvuC7e0W6rLUvSNOhjDT7nE"

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

data = requests.get(url).json()

for model in data["models"]:
    print(model["name"])