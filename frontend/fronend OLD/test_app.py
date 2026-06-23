from __future__ import annotations

from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent


TEST_DICTIONARY: dict[str, Any] = {
    "id": 1,
    "name": "Тестовый словарь",
    "words": [
        {"id": 1, "word": "apple", "translate": "яблоко", "transcription": "[ˈæpəl]", "context": None},
        {"id": 2, "word": "house", "translate": "дом", "transcription": "[haʊs]", "context": None},
        {"id": 3, "word": "water", "translate": "вода", "transcription": "[ˈwɔːtə]", "context": None},
        {"id": 4, "word": "sun", "translate": "солнце", "transcription": "[sʌn]", "context": None},
    ],
}


@app.get("/")
def index():
    return send_file(BASE_DIR / "index.html")


@app.get("/api/dictionary")
def get_dictionary():
    return jsonify(TEST_DICTIONARY)


@app.post("/api/repeat-result")
def save_repeat_result():
    data: list[dict[str, Any]] = request.get_json(force=True)

    print("\n=== РЕЗУЛЬТАТЫ ===")
    for item in data:
        print(item)

    return jsonify({"status": "ok", "count": len(data)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)