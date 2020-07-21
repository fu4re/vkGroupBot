from enum import Enum

class Command(Enum):
    showMails = ["showMails", "Почты преподавателей"]
    showNumbers = ["showNumbers", "Телефоны преподавателей"]
    sendMail = ["sendMail", "Отправить почту"]