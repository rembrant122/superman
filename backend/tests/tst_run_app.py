from pathlib import Path
import sys
import threading

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from main import run_flask


def tst_run_app() -> None:
    threading.Thread(
        target=run_flask,
        daemon=True,
    ).start()
