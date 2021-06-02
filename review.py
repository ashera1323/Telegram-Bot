from telegram.ext import Updater
import settings as s
import datetime
import models as m
import actions as a


def main():
    updater = Updater(s.TOKEN, use_context=True)
    for user in m.User:
        if user.date_start is not None and user.task.week.order <= user.access:
            #if user.task.order == datetime.date.today().weekday() + 1 and user.date_start <= datetime.date.today():
                updater.bot.send_message(chat_id=user.chat_id,
                                         text=f'Разбор задачи {user.task.name}:\n'
                                              f'{user.task.review}')
                if a.find_task(user.task.week, user.task.order + 1):
                    user.task = a.find_task(user.task.week, user.task.order + 1)
                    user.save()
                elif a.find_task(a.find_week(user.course, user.task.week.order + 1), 1):
                    user.task = a.find_task(a.find_week(user.course, user.task.week.order + 1), 1)
                    user.save()
                    if user.task.week.order <= user.access:
                        updater.bot.send_message(chat_id=user.chat_id,
                                            text=f'Новая задача на следующей неделе.')
                    else:
                        updater.bot.send_message(chat_id=user.chat_id,
                                                 text=f'Подписка заканчивается на этой неделе.')
                else:
                    updater.bot.send_message(chat_id=user.chat_id,
                                             text=f'Вы закончили курс.')
                    user.delete_instance()

if __name__ == '__main__':
    main()