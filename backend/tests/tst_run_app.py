import threading

from main import run_flask


def tst_run_app() -> None:
    threading.Thread(
        target=run_flask,
        daemon=True,
    ).start()
