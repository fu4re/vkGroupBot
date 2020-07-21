import configparser
import logging

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from managers.SwitchMode import SwitchManager


class Bot:
    config = configparser.ConfigParser()
    config.read("bot.ini")

    def __init__(self, token):
        self.users = {}

        self.session = vk_api.VkApi(token=token)
        self.longpoll_start = VkBotLongPoll(self.session, '186665465', wait=30)
        self.api = self.session.get_api()

        logging.basicConfig(level=logging.INFO, filename=self.config.get("Filenames", "LOG_FILENAME"),
                            format='%(asctime)s %(levelname)s:%(message)s')

    def get_userName(self, user_id):
        return self.api.users.get(user_id=user_id)[0]['first_name']

    def get_LongPollHistory(self, event):
        return self.api.messages.getHistory(offset=0, count=1, user_id=event.user_id, peer_id=event.peer_id)

    def sendMessage(self, id, message):
        return self.api.messages.send(peer_id=id,
                                      random_id=get_random_id(),
                                      message=message,
                                      keyboard=open(self.config.get("Filenames", "KEYBOARD_FILENAME"), "r",
                                                    encoding="UTF-8").read()
                                      )

    def start(self):
        logging.info("Бот успешно запущен! Id рабочей группы: " + self.config.get("Data", "API_GROUP_ID"))
        for event in self.longpoll_start.listen():

            if event.type == VkBotEventType.MESSAGE_NEW:
                username = self.get_userName(event.object.from_id)

                if event.object.from_id not in self.users:
                    self.users[event.object.from_id] = SwitchManager()

                    logging.info(
                        "Новый ивент от: " +
                        f"{username}, " +
                        f"{event.object.from_id}, Сообщение: " +
                        f"{event.object.text}")

                event.object.
                if event.type == VkBotEventType.MESSAGE_NEW:
                    self.sendMessage(event.object.from_id,
                                     self.users[event.object.from_id].reception(event.object.text)
                                    )

                    logging.info(self.api.messages.getHistory(offset=0, count=1,
                                                              peer_id=event.object.from_id))
                    logging.info("Сообщение успешно выслано: " + f"{username}, " + f"{event.object.from_id}")
