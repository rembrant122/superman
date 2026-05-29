import requests
import json

URL = "http://localhost:8000/get_list_words_for_repeat"
HEADERS = {"Authorization": "Bearer TOKEN"}

response = requests.post(URL, headers=HEADERS)

with open("word_model.json", "w", encoding="utf-8") as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=2)
