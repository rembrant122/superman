import asyncio
import threading

from app_flask.app_run import create_app
from superman.bots.bot_words import run_bot
from settings import HOST, PORT


def run_flask() -> None:
    app = create_app()
    app.run(host=HOST, port=PORT, debug=False)

async def main() -> None:
    await asyncio.gather(
        asyncio.to_thread(run_flask),
        run_bot(),
    )



if __name__ == "__main__":
    asyncio.run(main())
#12345
