import webbrowser

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "11d1377d87e3c5ab37e1d8c6a1102eb8"


def build_url(app: str, repeat: bool) -> str:
    return f"{BASE_URL}?app={app}&repeat={str(repeat).lower()}&token={TOKEN}"


if __name__ == "__main__":
    # выбери что открыть
    # webbrowser.open(build_url("eng_words", True))   # repeat words
    webbrowser.open(build_url("eng_words", False))  # memor words
    # webbrowser.open(build_url("skills", True))      # repeat skills
    # webbrowser.open(build_url("skills", False))     # memor skills
