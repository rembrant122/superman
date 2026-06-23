from datetime import datetime, timedelta, UTC

from superman.models.models_superman import Steps

STEP_MINUTES = {
    # 1:0,
    1:15,
    2:60,
    3:240,#4ч
    4:480,#8ч
    5:1440,#1д
    6:1440,#2д
    7:1440,#3д
    8:1440,#4д
    9:10080,#1н
    10:20160,#2н
    11:43200,#1м
    12:259200,#1/2г
}


def get_next_step_time(step_now:int, success:bool) -> Steps:

    if success:
        step_now+=1

        if step_now > 12:#последний шаг
            step_now=12

    else:

        if step_now>8:#если забыл на 2й день и далее=>повторить через день всёравно
            step_now=8
        #остаемся на том же шаге

    new_time = datetime.now(UTC) + timedelta(minutes=STEP_MINUTES.get(step_now, 1))

    step_next= Steps(step=step_now, new_date_time=new_time)

    return step_next
