# Работа с БД
import sqlite3

DatabaseName = 'reminder.db'
# Соединяемся с бд. Второй аргумент решает ошибку с потоками
SqlConnect = sqlite3.connect(DatabaseName, check_same_thread=False)
SqlCursor = SqlConnect.cursor()


# Добавить пользователя
def add_user(user_id, user_lang):
    print(str(user_id) + " - " + str(user_lang))
    SqlCursor.execute("INSERT INTO users (user_id, user_lang)"
                      "VALUES ('%s','%s')" % (user_id, user_lang))
    SqlConnect.commit()


# Добавить напоминание
def add_remind(user_id, remind_text, remind_time):
    SqlCursor.execute("INSERT INTO remind (user_id, remind_text, remind_time)"
                      "VALUES ('%s','%s','%s')" % (user_id, remind_text, remind_time))
    SqlConnect.commit()


def select_userID(user_id):
    with SqlConnect:
        SqlCursor.execute("SELECT user_id FROM users where user_id = ('%s')" % user_id)
        rows = SqlCursor.fetchone()
        if rows is None:
            return None
        else:
            # Возвращаем id пользователя
            return rows[0]
