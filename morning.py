from telegram.ext import Updater
import settings as s
import datetime
import models as m


def main():
    updater = Updater(s.TOKEN, use_context=True)
    for user in m.User:
        if user.date_start is not None :
            #if user.task.order == datetime.date.today().weekday() + 1 and user.date_start <= datetime.date.today():
                updater.bot.send_message(chat_id=user.chat_id,
                                         text=f'Доброе утро.\n'
                                              f'Сегодняшняя задача: {user.task.name}\n'
                                              f'Ссылка на задачу: {user.task.contest}\n'
                                              f'Задачу необходимо сдать до {s.deadline}')

if __name__ == '__main__':
    main()