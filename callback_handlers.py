from aiogram import Router 
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from main import bot
from keyboards import *
from cache import TempData
from states import VKR_States
from additional_functions import *

callback_router = Router() # мы так же как и в message_handlers создаем экземпляр нашего 
# маршрутизатора 
PHOTO_ID_ONE = 'AgACAgIAAxkBAAOiZZWRQKHD18GVlXxmc3XkxFmR4hMAAnjhMRscK7BIt9XPfdWp4AEBAAMCAAN4AAM0BA' 
PHOTO_ID_TWO = "AgACAgIAAxkBAAIBfmWa6HPHq5XIOxnWV6a2uYAC92b0AAJe3DEbaM7ZSAYGx_tW1zjIAQADAgADeAADNAQ"                                                                                                            # Сигнал (или запрос) отправляемый

@callback_router.callback_query(VKR_States.topic)
async def topic_procc(callback: CallbackQuery, state: FSMContext):

    if "theme" in callback.data:
        full_callback = callback.data.split(":")
        page_number = int(full_callback[1])
        cb_data = full_callback[0]

        match page_number:
            case 1:  
                await callback.message.edit_text(text="Обрати внимание!\n❗️Тему работы ОЧЕНЬ важно правильно сформулировать.\nКакие могут возникнуть проблемы? 😖:\n- Несоответствие темы и содержания материала;\n- Отсутствие конкретики в заголовке или непосредственно работе;\n- Размытость или неточность выражений.\nВсё это может помешать тебе на защите, поэтому отнесись к формулировке серьезно. 🧐\nНо не бойся! В тему можно вносить корректировки", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 2:
                await callback.message.edit_text(text="Параметры достойной темы 😎:\n- Актуальность, значимость\n- Четкость, ясность\n- Отражение сути проекта\n- Краткость и емкость", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 3:
                message_send = callback.message.answer(text="Что еще? 🤔:\n- Наименование проекта должно подчеркивать его суть, отмечая, что автор изучил и к чему стремился;\n- Тема и цель исследования должны пересекаться тесным образом, но при этом не дублировать (копировать) друг друга;\n- В названии работы должны прослеживаться направление исследования, объект и предмет;\n- Заглавие соответствует принципу актуальности (то есть изучаемая проблема до сих пор не нашла окончательного решения);\n- Тема должна вызывать интерес не только у автора, но и у читателя, поэтому приветствуется оригинальность и креативность (но всего должно быть в меру);\n- Наименование проекта формулируется кратко и емко в простой форме (без сложных оборотов и конструкций, вводных конструкций и пр.);\n- Заглавие должно подчеркивать уникальность проекта, то есть именно в таком ракурсе, с таким арсеналом инструментов ранее исследование не проводилось;\n- Заглавие проекта подчеркивает его значимость и призывает к конкретным действиям.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                message_change = callback.message.edit_text(text="Что еще? 🤔:\n- Наименование проекта должно подчеркивать его суть, отмечая, что автор изучил и к чему стремился;\n- Тема и цель исследования должны пересекаться тесным образом, но при этом не дублировать (копировать) друг друга;\n- В названии работы должны прослеживаться направление исследования, объект и предмет;\n- Заглавие соответствует принципу актуальности (то есть изучаемая проблема до сих пор не нашла окончательного решения);\n- Тема должна вызывать интерес не только у автора, но и у читателя, поэтому приветствуется оригинальность и креативность (но всего должно быть в меру);\n- Наименование проекта формулируется кратко и емко в простой форме (без сложных оборотов и конструкций, вводных конструкций и пр.);\n- Заглавие должно подчеркивать уникальность проекта, то есть именно в таком ракурсе, с таким арсеналом инструментов ранее исследование не проводилось;\n- Заглавие проекта подчеркивает его значимость и призывает к конкретным действиям.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                await inner_block(coroutine_obj=(message_change, message_send), state=state)
            case 4:
                data = await state.get_data()
                await data["temp_menu"].delete()
                temp_menu = await bot.send_photo(chat_id=TempData.user_id, photo=PHOTO_ID_ONE, caption="Вот полезные слова", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                await state.update_data(temp_menu=temp_menu)
            case 5:
                data = await state.get_data()
                await data["temp_menu"].delete()
                await callback.message.answer(text="Чем я ещё могу тебе помочь?", reply_markup=end_of_proc("theme").as_markup())
                await state.clear()
            case 0:
                await callback.message.edit_text(reply_markup=vkr().as_markup(), text="Что именно тебе нужно?")
                await state.clear()

@callback_router.callback_query(VKR_States.structure)
async def structure_proc(callback: CallbackQuery, state: FSMContext):

    if callback.data == "VKR":
        await callback.message.edit_text(reply_markup=vkr().as_markup(), text="Что именно тебе нужно?")
        await state.clear()
    elif callback.data == "actuality:1":
        await first_state_entry(cb_data=callback, 
                                state_tuple=(state, VKR_States.relevance), 
                                cb_text="Актуальность подчеркивает наличие проблемы, ее значимость и необходимость новых методов ее решения. 😊")
        
    elif callback.data == "problem:1":
        await first_state_entry(cb_data=callback,
                                state_tuple=(state, VKR_States.problem),
                                cb_text="Проблема - это противоречивая ситуация, требующая разрешения. ⚠️Проблема возникает тогда, когда прежнего знания становится недостаточно, а новое еще не приняло развитой формы.")
    elif callback.data == "goal:1":
        await first_state_entry(cb_data=callback,
                                state_tuple=(state, VKR_States.goal),
                                cb_text="Цель исследования - это конечный результат, которого хотел бы достичь исследователь при завершении своей работы. 🧐")
    
@callback_router.callback_query(VKR_States.relevance)
async def relevance_proc(callback: CallbackQuery, state: FSMContext):
    
    if "actuality" in callback.data:
        full_callback = callback.data.split(":")
        page_number = int(full_callback[1])
        cb_data = full_callback[0]
        
        match page_number:
            case 1:
                await callback.message.edit_text(text="Актуальность подчеркивает наличие проблемы, ее значимость и необходимость новых методов ее решения. 😊", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 2:
                message_send = callback.message.answer(text="Обрати внимание на компоненты актуальности 😉:\n- проблема, противоречие\n- необходимость действий, перемен\n- новизна\n- значимость исследования", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                message_change = callback.message.edit_text(text="Обрати внимание на компоненты актуальности 😉:\n- проблема, противоречие\n- необходимость действий, перемен\n- новизна\n- значимость исследования", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                await inner_block(coroutine_obj=(message_change, message_send), state=state)
            case 3:
                data = await state.get_data()
                await data["temp_menu"].delete()
                temp_menu = await bot.send_photo(chat_id=TempData.user_id, photo=PHOTO_ID_TWO, caption="Что если актуальность не очевидна с первого взгляда? 😳", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                await state.update_data(temp_menu=temp_menu)
            case 4:
                data = await state.get_data()
                await data["temp_menu"].delete()
                temp_menu = await callback.message.answer(text="Можно проанализировать следующие критерии 🤔:\n- степень изученности проблемы\n- эффективность ранних и текущих мер\n- потребности науки и отрасли", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                await state.update_data(temp_menu=temp_menu)
            case 5:
                await callback.message.edit_text(text="Можно посмотреть последние научные разработки по теме, частоту выхода в свет исследований в рамках данной и смежных тем, наличие текущих дискуссий. 🤓\nОбрати внимание на доступность и количество материалов по теме.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 6:
                await callback.message.edit_text(text="Избегай таких ошибок, как:\n- слишком сложная формулировка\n- слабая аргументация\n- несовпадение с темой\n- заимствования (плагиат) ⛔️", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 7:
                await callback.message.edit_text(text="Для актуальности выделен отдельный абзац во введении. В нем нужно в нескольких предложениях подчеркнуть нерешенность проблемы, степень ее изученности и новизну, ссылаясь на другие исследования. 📜", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 8:
                await callback.message.edit_text(text="Чем я ещё могу тебе помочь?", reply_markup=end_of_proc("actuality").as_markup())
                await state.clear()
            case 0:
                await callback.message.edit_text(text="Давай по порядку", reply_markup=structure().as_markup())
                await state.set_state(VKR_States.structure)
      
@callback_router.callback_query(VKR_States.problem)
async def problem_proc(callback: CallbackQuery, state: FSMContext):
    
    if "problem" in callback.data:
        full_callback = callback.data.split(":")
        page_number = int(full_callback[1])
        cb_data = full_callback[0]
        
        match page_number:
            case 1:
                await callback.message.edit_text(text="Проблема - это противоречивая ситуация, требующая разрешения. ⚠️Проблема возникает тогда, когда прежнего знания становится недостаточно, а новое еще не приняло развитой формы.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 2:
                await callback.message.edit_text(text="Каким критериям должна соответствовать проблема? 🧐:\n- возникновение проблемы должно быть продиктовано объективными факторами\n- проблема должна иметь теоретическое или прикладное значение для науки", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 3:
                await callback.message.edit_text(text="Что еще?:\n- проблема должна быть посильной (не взваливай на себя слишком много 😊)\n- проблема должна быть существующей, той, которая есть сейчас и которую можно решить в ходе исследования\n- проблема должна отличать твое исследование от аналогичных работ (новые факты, предложение новой идеи, обоснование идеи со ссылкой на авторитетные источники)\n- проблема должна отражать несоответствие практической деятельности ✨идеалу✨, описанному в теории", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 4:
                await callback.message.edit_text(text='Вот "полезные слова" 😇\n"несмотря на наличие таких-то мер (существующие решения 🤝) ..."\n"пользователи такого-то сервиса / клиенты / люди с каким-то заболеванием / студенты / женщины пожилого возраста и т.д. (КТО?👩🧑) ..."\n"не удовлетворены системой / качеством работы / результатом / любым другим параметром (проблема - что-то не так ☹️)\nИЛИ\n"уровень безработицы - высок, эффективность работы - недостаточна, что угодно еще (ЧТО?📈) - НЕ идеально 💎"', reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 5:
                await callback.message.edit_text(text="Чем я ещё могу тебе помочь?", reply_markup=end_of_proc("problem").as_markup())
                await state.clear()
            case 0:
                await callback.message.edit_text(text="Давай по порядку", reply_markup=structure().as_markup())
                await state.set_state(VKR_States.structure)
              
@callback_router.callback_query(VKR_States.goal)
async def goal_proc(callback: CallbackQuery, state: FSMContext):
     
    if "goal" in callback.data:
        full_callback = callback.data.split(":")
        page_number = int(full_callback[1])
        cb_data = full_callback[0]
        
        match page_number:
            case 1:
                await callback.message.edit_text(text="Цель исследования - это конечный результат, которого хотел бы достичь исследователь при завершении своей работы. 🧐", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 2:
                await callback.message.edit_text(text="Виды целей 🤔:\n- определение характеристик явлений, не изученных ранее\n- выявление взаимосвязи неких явлений\n- изучение развития явлений\n- обобщение, выявление общих закономерностей\n- создание классификаций", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 3:
                await callback.message.edit_text(text="'Полезные слова' для цели😇\nВыявление, обоснование, уточнение, конструирование, определение, исследование, обобщение, описание, создание, формирование", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 4:
                await callback.message.edit_text(text='Задачи исследования - это выбор путей и средств для достижения цели в соответствии с выдвинутой гипотезой. 🧐', reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 5:
                await callback.message.edit_text(text='Отнесись к формулированию задач серьезно. 🤔 Именно из задач рождаются заголовки глав (количество задач = количество глав в работе).', reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 6:
                await callback.message.edit_text(text='"Полезные слова" для задач 😇\nВыяснить, изучить, провести, рассмотреть, найти, описать', reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 7:
                await callback.message.edit_text(text="Чем я ещё могу тебе помочь?", reply_markup=end_of_proc("goal").as_markup())
                await state.clear()
            case 0:
                await callback.message.edit_text(text="Давай по порядку", reply_markup=structure().as_markup())
                await state.set_state(VKR_States.structure)  
                 
@callback_router.callback_query(lambda x: x) # только в этом случае будет происходить обработка именно 
# запросов типа CallbackQuery, на что указывает собственно .callback_query 
# можно заметить, что маршрутизатор пропускает любой callback-запрос 
async def button_exe(callback: CallbackQuery, state: FSMContext): # там так же важно сохранить результат нашего
    # callback-а в виде переменной соответсвующего типа
    
    if callback.data == "VKR":
        await callback.message.edit_text(reply_markup=vkr().as_markup(), text="Что именно тебе нужно?")
    elif callback.data == "wk_type_back":
        await callback.message.edit_text(reply_markup=type_of_work().as_markup(), text="Меню")
    elif callback.data == "proc_end":
        await callback.message.edit_text(text="Всегда рад помочь! Желаю удачи!")
    elif "theme:1" == callback.data:
        await first_state_entry(cb_data=callback,
                                state_tuple=(state, VKR_States.topic),
                                cb_text="Обрати внимание!\n❗️Тему работы ОЧЕНЬ важно правильно сформулировать.\nКакие могут возникнуть проблемы? 😖:\n- Несоответствие темы и содержания материала;\n- Отсутствие конкретики в заголовке или непосредственно работе;\n- Размытость или неточность выражений.\nВсё это может помешать тебе на защите, поэтому отнесись к формулировке серьезно. 🧐\nНо не бойся! В тему можно вносить корректировки")
    elif callback.data == "structure":
        await callback.message.edit_text(text="Давай по порядку", reply_markup=structure().as_markup())
        await state.set_state(VKR_States.structure)

    




