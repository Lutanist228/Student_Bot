from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from typing import Coroutine
from aiogram.fsm.context import FSMContext
from keyboards import page_surfer
from states import VKR_States

from copy import copy

async def inner_block(coroutine_obj: tuple[Coroutine, Coroutine], state: FSMContext):
    """Обработка ситуаций перед возникновении фотографии при перелистывании.
    * coroutine_obj - множественный объект типа "кортеж", первым элементом принимает корутину с .edit_text, вторым - с .answer
    * state - принимает хранилище FSM"""
    
    try:
        temp_menu = await coroutine_obj[0] 
        await state.update_data(temp_menu=temp_menu)
    except TelegramBadRequest:
        data = await state.get_data()
        await data["temp_menu"].delete()
        temp_menu = await coroutine_obj[1]
        await state.update_data(temp_menu=temp_menu)
    
async def first_state_entry(state_tuple: tuple[FSMContext, VKR_States], cb_data: CallbackQuery, cb_text: str):
    """Обработка первых вхождений в блоки статусов.
    * cb_data - принимает callback-объект
    * state_tuple - множественный объект типа "кортеж", принимает хранилище FSM и объект VKR_States
    * cb_text - принимает текст для .edit_text
    """
    callback_query = copy(cb_data)
    full_callback = cb_data.data.split(":")
    page_number = int(full_callback[1])
    cb_data = full_callback[0]
    
    await callback_query.message.edit_text(text=cb_text, reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
    await state_tuple[0].set_state(state_tuple[1])
    
async def message_delition(message_tuple: tuple):
    for msg in message_tuple:
        await msg.delete()