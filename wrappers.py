import functools
import utils


def check_admin_exist(storage):
    from main import bot

    def decorator(func):
        @functools.wraps(func)
        def wrapped(message):
            if not storage.admin_exist(message.chat.id):
                bot.send_message(chat_id=message.chat.id,
                                 text='You are not admin. This accident will be reported.')
                for admin_id in storage:
                    bot.send_message(chat_id=admin_id, text='Func usage attempt from @{}'
                                                            .format(message.from_user.username))
                return
            return func(message)
        return wrapped
    return decorator


def check_user_exist(storage):
    from main import bot

    def decorator(func):
        @functools.wraps(func)
        def wrapped(message):
            if not storage.user_exist(message.chat.id):
                bot.send_message(chat_id=message.chat.id,
                                 text='✨ Вас нет в базе данных, нажмите /start для регистрации')
                return
            return func(message)
        return wrapped
    return decorator


def get_log_filename():
    now = utils.get_msk_time()
    return '{0}_{1}_{2}_commands_log.txt'.format(str(now.year), str(now.month), str(now.day))


def logger(func):
    @functools.wraps(func)
    def wrapped(message):
        from database import users_db
        user_id = message.chat.id
        user_name = message.from_user.username
        group = users_db.get_users_group(message.chat.id)
        with open('./logs/' + get_log_filename(), 'a') as file:
            print(utils.get_msk_time(), user_id, user_name, group, message.text, file=file)
        return func(message)

    return wrapped
