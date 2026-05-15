from datetime import datetime, timedelta

from models import Steps

STEP_MINUTES = {
    1:0,
    2:15,
    3:60,
    4:240,#4ч
    5:480,#8ч
    6:1440,#1д
    7:1440,#2д
    8:1440,#3д
    9:1440,#4д
    10:10080,#1н
    11:20160,#2н
    12:43200,#1м
    13:259200,#1/2г
}


def get_next_step_time(step_now:int, success:bool) -> Steps:

    if success:
        step_now+=1

        if step_now > 13:#последний шаг
            step_now=13

    else:
        if step_now>9:#если забыл на 2й день и далее=>повторить через день всёравно
            step_now=9
        #остаемся на том же шаге

    new_time = datetime.now() + timedelta(minutes=STEP_MINUTES.get(step_now, 0))

    step_next= Steps(step=step_now, new_date_time=new_time)

    return step_next
