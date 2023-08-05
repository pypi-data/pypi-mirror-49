server_address = '0.0.0.0'
server_port = 7777
mode = 'gui'
pwd = ''
account = 'Guest'
alive = True

ACTION = 'action'
TIME = 'time'
USER = 'user'

ALERT = 'alert'
ADD_CONTACT = 'add_contact'
DEL_CONTACT = 'del_contact'
ACCOUNT_NAME = 'account_name'
ACCOUNT_PASSWORD = 'account_password'
USER_LOGIN = 'user_login'
USER_ID = 'user_id'
RESPONSE = 'response'
ERROR = 'error'
PRESENCE = 'presence'
MSG = 'msg'
GET_CONTACTS = 'get_contacts'
TO = 'to'
FROM = 'from'
MESSAGE = 'message'
MAIN_CHANNEL = '#all'
SERVER = 'server'
EXIT = 'exit'
INT_CMD = 'internal command'

BASIC_NOTICE = 100
OK = 200
ACCEPTED = 202
WRONG_REQUEST = 400
SERVER_ERROR = 500
IMPORTANT_NOTICE = 101  # важное уведомление.
CREATED = 201  # объект создан;
NO_AUTH = 401  # не авторизован;
WRONG_PASSW = 402  # неправильный логин/пароль;
BANNED = 403  # (forbidden) — пользователь заблокирован;
NOT_FOUND = 404  # (not found) — пользователь/чат отсутствует на сервере;
CONFLICT = 409  # (conflict) — уже имеется подключение с указанным логином;
GONE = 410  # (gone) — адресат существует, но недоступен (offline).
INTERNAL_ERROR = 500  # ошибка сервера.
SHUTDOWN = 'shutdown'  # Выключение сервера
UNKNOWN_ERROR = 999  # Нестандартная ошибка

StandartServerCodes = BASIC_NOTICE, OK, ACCEPTED, WRONG_REQUEST, SERVER_ERROR, IMPORTANT_NOTICE, CREATED, NO_AUTH, WRONG_PASSW, BANNED, NOT_FOUND, GONE, INTERNAL_ERROR, SHUTDOWN


class UnknownCode(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return f'Неизвестный код ответа {self.code}'
