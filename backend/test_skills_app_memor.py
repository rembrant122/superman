from tsts.get_tst_user import get_tst_user

from tsts.tst_run_app import tst_run_app
from web_app_url import memor_web_app, memor_web_app_skill


def tst_get_skill_for_memor():

    print('\n\nне забудь забилдить фронт!'
          '\n\nЗАПУСКАЕМ ПРИЛУ!'
          '\n\n')
    tst_run_app()
    print('берем юзера')
    U = get_tst_user()
    print('показываем для запомин ')

    TST_URL_WORDS_MEMOR = memor_web_app_skill(U)
    print(TST_URL_WORDS_MEMOR)

    input("Нажми Enter для остановки...")

if __name__ == "__main__":
    tst_get_skill_for_memor()#
