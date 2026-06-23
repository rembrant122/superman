from get_tst_user import get_tst_user

from bots.web_app_url import memor_web_app
from tst_run_app import tst_run_app

def tst_get_words_for_memor():

    print('\n\nне забудь забилдить фронт!'
          '\n\nЗАПУСКАЕМ ПРИЛУ!'
          '\n\n')
    tst_run_app()
    print('берем юзера')
    U = get_tst_user()
    print('показываем для запомин ')

    TST_URL_WORDS_MEMOR = memor_web_app(U)
    print(TST_URL_WORDS_MEMOR)

    input("Нажми Enter для остановки...")

if __name__ == "__main__":
    tst_get_words_for_memor()#
