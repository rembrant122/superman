from bots.web_app_url import repeat_web_app, memor_web_app
from backend.tests.get_tst_user import get_tst_user

U=get_tst_user()
TST_URL_WORDS_MEMOR=memor_web_app(U)
if __name__ == "__main__":
    print(TST_URL_WORDS_MEMOR)
