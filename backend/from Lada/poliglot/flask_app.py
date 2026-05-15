from flask import Flask, jsonify, request

from db import load_words, update_history_db, get_next_repeat_time
from _verification import verify_init_data


# Указываем: статические файлы лежат в ./static и доступны прямо по корню
app = Flask(
    __name__,
    static_folder='static',
    static_url_path=''   # -> /index.html, /main.js, /card-page.js и т.д.
)

# на корень отдаем просто файл index.html из static/
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    init_data = data.get("initData", "")
    user = verify_init_data(init_data)
    if not user:
        return jsonify({"error": "invalid signature"}), 403
    print(f"[AUTH] Пользователь вошёл: tg_id={user['id']}, имя={user.get('first_name')}")
    return jsonify({"tg_id": user["id"], "first_name": user.get("first_name")})

@app.route('/repeat', methods=['GET'])
def repeat():
    tg_id = request.args.get("tg_id", type=int)
    dict_id = request.args.get("dict_id", type=int)

    if not tg_id:
        return jsonify({"error": "tg_id обязателен"}), 400

    words = load_words(tg_id, dict_id, all_words=False)

    if not words:
        from db import get_next_repeat_time
        next_repeat = get_next_repeat_time(tg_id)
        return jsonify({"words": [], "next_repeat": next_repeat})

    return jsonify(words)

@app.route("/update_history", methods=["POST"])
def update_history():
    data = request.get_json()
    tg_id = data.get("tg_id")
    words = data.get("words", [])

    if not tg_id or not words:
        return jsonify({"error": "tg_id и words обязательны"}), 400

    update_history_db(tg_id, words)
    next_repeat = get_next_repeat_time(tg_id)
    print(next_repeat)

    return jsonify({"success": True, "next_repeat": next_repeat})


if __name__ == '__main__':
    app.run(debug=True)