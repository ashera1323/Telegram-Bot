import models as m


def convert(str):
    newstr = ''
    str = str.lower()
    alp = ' ,.?!\n'
    for i in str:
        if not (i in alp):
            newstr += i
    return newstr


def add_course(name, announcement):
    if find_course(convert(name)):
        return False
    course = m.Course(name=name,
                      text=convert(name),
                      announcement=announcement)
    course.save()
    return True


def find_course(name):
    try:
        course = m.Course.get(m.Course.text == convert(name))
        return course
    except:
        return False


def print_course(name):
    course = find_course(name)
    ans = f'Курс {course.name}\n' \
          f'Описание курса {course.announcement}\n'
    i = 1
    while find_week(course, i):
        week = find_week(course, i)
        ans += f'   Неделя {week.order} {week.name} \n' \
               f'   Описание недели {week.announcement}:\n'
        j = 1
        while find_task(week, j):
            task = find_task(week, j)
            ans += f'       Задача {task.order} {task.name} контест - {task.contest}  разбор - {task.review}\n'
            j += 1
        i += 1
    return ans


def delete_course(name):
    course = find_course(name)
    for i in range(1, 5):
        week = find_week(course, i)
        for j in range(1, 8):
            task = find_task(week, j)
            for user in m.User:
                if user.task == task:
                    user.delete_instance()
            if find_task(week, j):
                task.delete_instance()
        if find_week(course, i):
            week.delete_instance()
    if find_course(name):
        course.delete_instance()


def show_courses():
    ans = 'Все курсы:\n'
    for course in m.Course:
        ans += course.name + '\n'
    return ans


def add_week(course, order, name, announcement):
    if find_week(course, order):
        return False
    week = m.Week(course=course,
                  order=order,
                  name=name,
                  announcement=announcement)
    week.save()
    return True


def find_week(course, order):
    try:
        week = m.Week.get(m.Week.course == course, m.Week.order == order)
        return week
    except:
        return False


def add_task(week, order, name, contest, review):
    if find_task(week, order):
        return False
    task = m.Task(name=name,
                  week=week,
                  order=order,
                  contest=contest,
                  review=review)
    task.save()
    return True


def find_task(week, order):
    try:
        task = m.Task.get(m.Task.week == week, m.Task.order == order)
        return task
    except:
        return False


def add_user(alias, course, access):
    if find_user(alias):
        return False
    week = find_week(course, 1)
    user = m.User(alias=alias,
                  access=access,
                  task=m.Task.get(m.Task.week == week, m.Task.order == 1),
                  course=course,
                  name='')
    user.save()
    return True


def find_user(alias):
    try:
        user = m.User.get(m.User.alias == alias)
        return user
    except:
        return False


def delete_user(alias):
    user = find_user(alias)
    user.delete_instance()


def update_user(user, name, surname, date_start, char_id):
    user.name = name
    user.surname = surname
    user.date_start = date_start
    user.chat_id = char_id

    user.save()
