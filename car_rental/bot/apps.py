from django.apps import AppConfig

class BotConfig(AppConfig):
    name = 'bot'

    def ready(self):
        # Запуск бота, используя стандартный менеджер
        from .bot import run_bot
        run_bot()
