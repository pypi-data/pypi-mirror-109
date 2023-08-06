from django.apps.config import AppConfig


class RocshelfAppConfig(AppConfig):
    """ Конфигурация django приложения для подключения к django """

    name = 'rocshelf.integration.django'

    def ready(self):
        pass
