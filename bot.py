import datetime
import settings as s
from telegram import Update
from telegram.ext import *
import actions as a


def add_users(update: Update, context: CallbackContext) -> None:
    if not (update.effective_user.username in s.admins):
        update.message.reply_text('Недостаточно прав.')
        return

    mes = update.message.text.split('\n')
    course_name = ''
    req = mes[0].split('/add_users ')
    for i in req:
        if len(i) > 0:
            course_name += i

    if not (a.find_course(course_name)):
        update.message.reply_text(f'Курс {course_name} не найден.')
        return

    course = a.find_course(course_name)
    trouble = []
    for i in range(1, len(mes)):
        data = mes[i].split(' ')
        try:
            if a.find_user(data[0]):
                user = a.find_user(data[0])
                user.access = data[1]
                user.save()
            else:
                a.add_user(data[0], course, data[1])
        except:
            trouble.append(data[0])

    if len(trouble) == 0:
        update.message.reply_text(f'Все пользователи успешно добавлены.')

    if len(trouble) > 0:
        ans = 'Ошибка добавления следующих пользователей:\n'
        for i in trouble:
            ans += i + '\n'
        update.message.reply_text(ans)


def add_course(update: Update, context: CallbackContext) -> None:
    if not (update.effective_user.username in s.admins):
        update.message.reply_text('Недостаточно прав.')
        return
    mes = update.message.text.split('\n')
    req = mes[0].split()
    course_name = ''
    for i in range(1, len(req)):
        if req[i][0] == '#':
            break
        course_name += req[i] + ' '

    if not (a.add_course(course_name, mes[0].split('#')[1])):
        update.message.reply_text(f'Курс {course_name} уже существует.')
        return

    course = a.find_course(course_name)

    ok = []
    trouble = []
    for line in mes:
        req = line.split()
        if req[0] == 'week':
            week_name = ''
            announcement = line.split('#')[1]
            for i in range(2, len(req)):
                if len(req[i]) > 0 and req[i][0] == '#':
                    break
                week_name += req[i] + ' '
            try:
                if a.add_week(course, req[1], week_name, announcement):
                    week = a.find_week(course, req[1])
                else:
                    update.message.reply_text(f'Неделя {week_name} уже существует.')
            except:
                update.message.reply_text(f'Ошибка добавления недели {week_name} .')

        if req[0] == 'task':
            task_name =''
            for i in range(2, len(req) - 2):
                task_name += req[i] + ' '

            try:
                if a.add_task(week, req[1], task_name, req[len(req) - 2], req[len(req) - 1]):
                    ok.append(task_name)
                else:
                    update.message.reply_text(f'Задача {task_name} уже существует.')
            except:
                trouble.append(task_name)

    if len(trouble) == 0:
        update.message.reply_text(f'Курс {course_name} успешно доавблен.')
    else:
        update.message.reply_text(f'Курс {course_name} не добавлен.')
        a.delete_course(course_name)
        ans = ''
        for i in trouble:
            ans += i + '\n'
        update.message.reply_text(f'Ошибка добавления следующих задач: \n {ans}')


def show_courses(update: Update, context: CallbackContext) -> None:
    if not (update.effective_user.username in s.admins):
        update.message.reply_text('Недостаточно прав.')
        return
    update.message.reply_text(a.show_courses())


def print_course(update: Update, context: CallbackContext) -> None:
    if not (update.effective_user.username in s.admins):
        update.message.reply_text('Недостаточно прав.')
        return
    req = update.message.text.split()
    course_name = ''
    for i in range(1,len(req)):
        course_name += req[i] + ' '
    update.message.reply_text(a.print_course(course_name))


def delete_course(update: Update, context: CallbackContext) -> None:
    if not (update.effective_user.username in s.admins):
        update.message.reply_text('Недостаточно прав.')
        return
    req = update.message.text.split()
    course_name = ''
    for i in range(1,len(req)):
        course_name += req[i] + ' '
    if a.find_course(course_name):
        a.delete_course(course_name)
        update.message.reply_text(f'Курс {course_name} удален.')
    else:
        update.message.reply_text(f'Курса {course_name} не существует.')


def help(update: Update, context: CallbackContext) -> None:
    if not (update.effective_user.username in s.admins):
        update.message.reply_text(s.help_user)
        return
    update.message.reply_text(s.help_admin)


def question(update: Update, context: CallbackContext) -> None:
    if s.get_question_chat_id() != 0:
        Updater(s.TOKEN, use_context=True).bot.forwardMessage(chat_id=s.get_question_chat_id(),
                                                              from_chat_id=update.message.chat_id,
                                                              message_id=update.message.message_id)


def set_question_chat_id(update: Update, context: CallbackContext) -> None:
    s.set_question_chat_id(update.message.chat_id)


def answer(update: Update, context: CallbackContext) -> None:

    user = a.find_user(update.message.reply_to_message.forward_from.username)
    print(user.alias)
    Updater(s.TOKEN, use_context=True).bot.forwardMessage(chat_id=user.chat_id,
                                                          from_chat_id=s.get_question_chat_id(),
                                                          message_id=update.message.reply_to_message.message_id)
    Updater(s.TOKEN, use_context=True).bot.send_message(chat_id=user.chat_id, text=update.message.text)


def start(update: Update, context: CallbackContext) -> None:
    if a.find_user(update.effective_user.username):
        user = a.find_user(update.effective_user.username)
        if len(user.name) == 0:
            user.name = update.effective_user.first_name
            user.surname = update.effective_user.last_name
            user.chat_id = update.message.chat_id
            user.date_start = datetime.date.today() + datetime.timedelta((7 - datetime.date.today().weekday()) % 7)
            user.save()

            update.message.reply_text(f'Привет {user.name}!\n'
                                      f'Добро пожаловать на курс {user.course.name}\n'
                                      f'Первый урок {user.date_start}')


def info(update: Update, context: CallbackContext) -> None:
    if not (update.effective_user.username in s.admins) and (str(update.message.chat_id) != s.get_question_chat_id()):
        update.message.reply_text('Недостаточно прав.')
        return
    req = update.message.text.split()

    if req[1] == 'add_users':
        update.message.reply_text('Добавление пользователей.\n'
                                  'В первой строке необходимо ввести название курса, '
                                  'в который добавляем пользователей.\n'
                                  'В следующих строках необходимо ввести алиас и кол-во купленных недель.\n'
                                  'Например:\n'
                                  '/add_users Введение в программирование\n'
                                  'first_alias 4\n'
                                  'second_alias 3\n\n'
                                  'Для простоты можно все сделать в Excel, а потом просто скопировать и отправить боту.')

    if req[1] == 'add_course':
        update.message.reply_text('Добавление курса.\n'
                                  'В певрой строке необходимо указать имя курса, а также его описание. '
                                  'Описание начинаетсяс символа #.\n'
                                  'В следующей строке необходимо указать week, если идет добавление недели '
                                  'или task, если добавление задачи.\n'
                                  'Чтобы добавить неделю - нужно указать очередность недели в курсе,'
                                  ' имя недели и ее описание.'
                                  'Описание начинаетсяс символа #.\n'
                                  'Чтобы добавить задачу - нужно укзаать порядок задачи в неделе, '
                                  'ее имя и ссылки на контест и разбор.\n'
                                  'Задача будет связана с последней добавленной неделей.\n'
                                  'Например:\n'
                                  '/add_course Введение в программирование #Изучаем основы. Ссылка на вводный урок.\n'
                                  'week 1 Простейшие операции #Изучаем простые операции\n'
                                  'task 1 A+B http://contest_url1 http://review_url1\n'
                                  'task 2 A*B http://contest_url2 http://review_url2\n'
                                  'week 2 Что-то посложнее #Функции\n'
                                  'task 1 Факториал http://contest_url1 http://review_url1\n\n'
                                  'Для простоты можно все сделать в Excel, а потом просто скопировать и отправить боту.')

    if req[1] == 'show_courses':
        update.message.reply_text('Показывает все существующие курсы. Никаких параметров не надо.\n'
                                  '/show_courses')
    if req[1] == 'print_course':
        update.message.reply_text('Показывает подробности определенного курса. Необходимо ввести имя курса.\n'
                                  'Например:\n'
                                  '/print_course Введение в программирование')

    if req[1] == 'delete_course':
        update.message.reply_text('Удаляет определенный курс. Необходимо ввести имя курса.\n'
                                  'Например:\n'
                                  '/delete_course Введение в программирование')

    if req[1] == 'set_question_chat_id':
        update.message.reply_text('Бот будет пересылать все вопросы от учеников в чат, где прописана эта команда.\n'
                                  'Для использования необходимо добавить бота в этот чат.\n'
                                  '/set_question_chat_id')

    if req[1] == 'answer':
        update.message.reply_text('Чтобы ответ на вопрос пришел участнику, необходимо переслать сообщение в чат для вопросов'
                                  ' и добавить ответ в виде /answer Ответ на вопрос\n')


def main():
    updater = Updater(s.TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('add_users', add_users))
    dp.add_handler(CommandHandler('add_course', add_course))
    dp.add_handler(CommandHandler('show_courses', show_courses))
    dp.add_handler(CommandHandler('print_course', print_course))
    dp.add_handler(CommandHandler('delete_course', delete_course))
    dp.add_handler(CommandHandler('set_question_chat_id', set_question_chat_id))
    dp.add_handler(CommandHandler('answer', answer))
    dp.add_handler(CommandHandler('info', info))

    dp.add_handler(CommandHandler('question', question))
    dp.add_handler(CommandHandler('help', help))

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()