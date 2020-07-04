from datetime import datetime


def log_message(message):
    file = open("logs.log", "a")
    file.write("################################################################\n")
    file.write(datetime.now().strftime("%d-%m-%Y: %H-%M-%S\n"))
    file.write(f'Сообщение от пользователя {message.from_user.first_name} {message.from_user.last_name}'
               f'(id = {message.from_user.id})\n{message.text}\n')
    file.write("################################################################\n\n")
    file.close()


def log_exception(exception):
    file = open("logs.log", "a")
    file.write("################################################################\n")
    file.write(f'[ОШИБКА] {type(exception).__name__}: {exception}\n')
    file.write("################################################################\n\n")
    file.close()
