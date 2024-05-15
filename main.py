from aiogram import Bot, Dispatcher # мы импортируем два основополагающих объекта из
import aiogram
from aiogram.fsm.storage.memory import MemoryStorage
# aiogram
import asyncio as asy # для запуска асинхронных функций мы пользуемся asyncio 

BOT_TOKEN = "6353873033:AAHXjfqGRdMatA9n_zWwew2VhHfBbhIhmfA" # мы закрепляем за константой наш токен

dp = Dispatcher(storage=MemoryStorage()) # тут мы объявляем пустой экземпляр диспечера, в который будем все помещать
bot = Bot(token=BOT_TOKEN) # тут мы помещаем внутрь бота токен

async def on_startup(): # для удобства создаем функцию print-ования сообщения при запуске бота
    print("Бот запущен!")

async def main(): # создаем основную функцию
    import message_handlers, callback_handlers # импортируем внутрь области функции скрипты 
    await bot.delete_webhook(drop_pending_updates=True) # уничтожаем ожидающие udate-ы для того, чтобы предотвратить формирование
    # очередей запросов и предотвратить конфликты и баги
    dp.include_routers(message_handlers.message_router, callback_handlers.callback_router) # присоединяем к диспечеру наши routers-маршрутизаторы
    # НЕ ОБЯЗАТЕЛЬНО allowed_updates=dp.resolve_used_update_types() ---> в start_polling() данный аргумент функции start_polling()
    # определяет то, какие имена событий пропустить, а какие нет.
    # Проще говоря - данная функция определяет, что бот может обрабатывать ТОЛЬКО зарегистрированные типы событий
    # т.е. те, что указаны, например, в функции dp.include_routers(...)
    dp.startup.register(on_startup) # тут мы помещаем внутрю функцию, что срабатывает при запуске бота
    await dp.start_polling(bot) # и непосредственно последним действием мы запускаем процесс, помещая 
    # внутрь start_polling(...) наш экземпляр бота

if __name__ == '__main__': # общепринятые нормы программирования советуют писать 
    # конструкцию вида "if __name__=='название модуля'" для того, чтобы процессы
    # происходящие в боте "руководились" из одного конкретного основного скрипта main
    asy.run(main()) # мы запускаем функцию main()