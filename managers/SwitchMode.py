from managers.Commands import Command
from managers.Modes import Mode
from gmail_api.Gmail import Mail

from core.cfg import PREPOD_INFO

class SwitchManager:
    def __init__(self):
        self.current_mode = Mode.mainMode
        self.previous_mode = Mode.listenMode

        self.command = None
        self.last_answer = None

        self.mail = Mail('mai2019.group124@gmail.com', 'M301242019')

    def swap(self, mode):
        self.previous_mode = self.current_mode
        self.current_mode = mode

        self.last_answer = None

    def reception(self, message, attach=None):

        if message.startswith('/'):
            for mode in Mode:
                if message[1::] in mode.value:
                    self.swap(mode)
                    return self.current_mode.value[0]
            return 'Выбран неизвестный режим. Доступно: /send, /main'

        if self.current_mode == Mode.answer:
            self.last_answer = message
            self.current_mode = self.previous_mode
            return "Чтобы отправить письмо, нажми Отправить почту"

        if self.current_mode == Mode.mainMode:

            if message in Command.showMails.value:
                return PREPOD_INFO

            if message in Command.showNumbers.value:
                return "Тут мобасики будут"

        if self.current_mode == Mode.listenMode:

            if self.last_answer is None:

                self.swap(Mode.answer)
                self.command = message
                return "Следующим сообщением напишите то, что хотите отправить: "

            else:
                if message != 'Отправить почту':
                        return "Необходимо отправить почту или выйти из режима командой."

                self.mail.gmailCreateMsg('Test', 'fu4re1@gmail.com', self.last_answer)
                self.swap(Mode.mainMode)
                return "Почта отправлена!"

        return 'Я тебя не понимаю(пока что)...'











