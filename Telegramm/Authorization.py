from reminder_DB import SQL_requests


# Есть ли id в базе?
def check_user(id):
    try:
        user = SQL_requests.select_userID(str(id))
        if user is not None:
            return user
        else:
            return None
    except:
        print("Исключение при авторизации")
