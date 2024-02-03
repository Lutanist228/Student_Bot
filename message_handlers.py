from aiogram import Router, F # мы импортируем класс Router-а (для маршрутизации запросов)
# а так же объект фильтра для корректной и гибкой фильтрации запроса 
from aiogram.types import Message # мы импортируем класс Message, что содержит в себе
# целый ряд информации о присылаемом пользователем сообщении (будь то команда или же просто текст)
from aiogram.filters import Command # мы так же импортируем объект Commands который отвечает за 
# фильтр особых текстовых сообщений, содержищих специальный символы, 
# что в свою очередь принадлежат к командам 
from aiogram.fsm.context import FSMContext

from main import bot
from keyboards import * 
from cache import TempData 

message_router = Router() 

@message_router.message(lambda x: x.text == "Открыть главное меню")
async def back_to_mm(message: Message, state: FSMContext):
    # data = await state.get_data()
    await state.clear() ; await message.delete()
    TempData.user_id = message.from_user.id
    menu = await bot.send_message(chat_id=message.from_user.id, text="Тип научной работы", reply_markup=type_of_work().as_markup())                                                 

@message_router.message(Command("start"))                                            
async def starting_menu(message: Message, state: FSMContext):
    await state.clear()
    TempData.user_id = message.from_user.id
    await message.answer(text="Открытие главного меню", reply_markup=back_to_main())
    menu = await bot.send_message(chat_id=message.from_user.id, text="Тип научной работы", reply_markup=type_of_work().as_markup())

@message_router.message(lambda x: x)
async def message_del(message: Message, state: FSMContext):
    await message.delete()

# @message_router.message(lambda x: x)
# async def photo_proc(message: Message):
#     photo_info = message.photo
#     photo_id = message.photo[-1].file_id
#     print(photo_id)


            