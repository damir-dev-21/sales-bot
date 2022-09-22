import os
import django
from django_project.botadmin import settings

# from utils.set_bot_commands import set_default_commands
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    import middlewares, filters, handlers

    # Уведомляет про запуск
    from utils.notify_admins import on_startup_notify

    await on_startup_notify(dispatcher)
    await set_default_commands(dp)



def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "django_project.botadmin.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


if __name__ == '__main__':
    setup_django()

    from aiogram import executor
    from loader import dp


    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)