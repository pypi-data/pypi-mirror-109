""" Модуль конфигурирования приложения

"""

from __future__ import annotations

from rcore import config
from rcore.rpath import rPath
from rcore.rtype import Validator

_VEmptyDict = Validator(dict, [], {})
_VBoolFalse = Validator(bool, [False, True], False)

config_rules = [
    config.CfgRule(
        'Основные настройки компиляции',
        ['setting', 'settings'], _VEmptyDict,
        [
            config.CfgRule(
                'Степень сжатия кода при компиляции',
                ['compression'], Validator(str, ['nested', 'expanded', 'compact', 'compressed'], 'nested'),
            ),
            config.CfgRule(
                'Сохранять предыдущие версии компиляции в папку cache/versions',
                ['backup'], _VBoolFalse,
            ),
            config.CfgRule(
                'Очищать папку экспорта перед компиляцией',
                ['deldist'], _VBoolFalse,
            ),
            config.CfgRule(
                'Упростить вариации вызова конструкций до одного-пары символов (увеличит скорость работы)',
                ['simplified'], _VBoolFalse,
            ),
        ]
    ),

    config.CfgRule(
        'Инициализация маршрутов. Основываясь на этом словаре будут компилироваться страницы.',
        ['route', 'routes'], _VEmptyDict
    ),

    config.CfgRule(
        'Инициализация путей.',
        ['path', 'paths'], _VEmptyDict,
        [
            config.CfgRule(
                'Пути до экспорта файлов.',
                ['export', 'exports'], _VEmptyDict,
                [
                    config.CfgRule(
                        'Для страниц.',
                        ['template'], Validator(str, [], 'template'),
                    ),
                    config.CfgRule(
                        'Для статики',
                        ['static'], Validator(str, [], 'static'),
                    ),
                    config.CfgRule(
                        'Для медиа файлов',
                        ['media'], Validator(str, [], 'media'),
                    ),
                    config.CfgRule(
                        'Для мета файлов (robots.txt, favicon)',
                        ['meta'], Validator(str, [], 'template'),
                    ),
                ]
            ),

            config.CfgRule(
                'Пути для импорта файлов.',
                ['import', 'imports'], _VEmptyDict,
                [
                    config.CfgRule(
                        'Файлы локализации',
                        ['localization', 'local'], Validator(str, [], 'localization'),
                    ),
                    config.CfgRule(
                        'Медиа файлы',
                        ['media'], Validator(str, [], 'media'),
                    ),
                    config.CfgRule(
                        'Файлы статики',
                        ['static'], Validator(str, [], 'static'),
                    ),
                    config.CfgRule(
                        'Мета файлы (robots.txt, favicon)',
                        ['meta'], Validator(str, [], 'meta'),
                    ),

                    config.CfgRule(
                        'Папка для импорта групп шелфов.',
                        ['groups'], Validator(str, [], 'groups'),
                    ),

                    config.CfgRule(
                        'Шелфы страниц.',
                        ['page', 'pages', 'pg'],
                        _VEmptyDict
                    ),
                    config.CfgRule(
                        'Шелфы оберток.',
                        ['wrapper', 'wrappers', 'wp'],
                        _VEmptyDict
                    ),
                    config.CfgRule(
                        'Шелфы тегов.',
                        ['tag', 'tags', 'tg'],
                        _VEmptyDict
                    ),
                    config.CfgRule(
                        'Шелфы блоков.',
                        ['block', 'blocks', 'bl'],
                        _VEmptyDict
                    )
                ]
            )
        ]
    )
]


class ForCompilingConfig(config.ConfigEngine):
    """ Настройки конфигурации дял использования rocshelf для компиляции """

    rules = config_rules

    def preparation(self):
        self.merge()
        self.use_rule()
        self.path_common()
        self.save()
        self.prepared = True


class ForReadingConfig(config.ConfigEngine):
    """ Настройки конфигурации дял использования rocshelf для интеграции в другии python приложения (django, flask).

    Подразумевается, что сначала пройдет компиляция, после чего будет задейстовован этот класс.

    """

    def preparation(self):
        self.init({
            'cache': ['rocshelf-compiled.json']
        })

        self.merge()
        self.use_rule()
        self.prepared = True

    def save_compiled(self, pages: dict):
        """Сохранение необходимой информации для работы функционал интеграции с фреймворками python

        Args:
            pages (dict): Словарь, где ключ - идентификатор маршрута, а значение информация о странице

        """

        distConfig = {
            'export': self.config.get(['path', 'export']),
            'template': {key: pages[key].file for key in pages}
        }
        rPath('rocshelf-compiled.json', fromPath='cache').dump(distConfig)


rcf = config.CfEngine(ForReadingConfig)
pcf = config.CfEngine(ForCompilingConfig)
