import rlogging
import rocshelf

from django.apps.config import AppConfig

logger = rlogging.get_logger('mainLogger')


def run():
    rocshelf.set_path(rocshelf.gen_user_workspace(__file__, '../dist'), logsFolderName='/var/log/rocshelf2/')
    rocshelf.set_config(dictconfig={
        'export': {
            'common': '.'
        }
    })
    rocshelf.main.init_for_reading()


class RocshelfAppConfig(AppConfig):
    """ Конфигурация django приложения для подключения к django """

    name = 'rocshelf.integration.django'

    def ready(self):
        run()
