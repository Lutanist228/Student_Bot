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
PHOTO_ID_TWO = "AgACAgIAAxkBAAIBfmWa6HPHq5XIOxnWV6a2uYAC92b0AAJe3DEbaM7ZSAYGx_tW1zjIAQADAgADeAADNAQ"
PHOTO_ID_THREE = "AgACAgIAAxkBAAICbGWwE24UiAT4pQIrc9LsGF1ADA8oAAIm-TEbST6ASQKK5zr7tZwEAQADAgADeQADNAQ"# Сигнал (или запрос) отправляемый
PHOTO_ID_FOUR = "AgACAgIAAxkBAAICiGWwH6_EFC_7PDuUpf-YsZB6wAcPAAJ6_DEbST6AScrsLIxx-SyXAQADAgADeAADNAQ"


@callback_router.callback_query(VKR_States.lit_review)
async def lit_review(callback: CallbackQuery, state: FSMContext):
    if callback.data == "VKR":
        await callback.message.edit_text(reply_markup=vkr().as_markup(), text="Что именно тебе нужно по ВКР 😇?")
        await state.clear()
    elif callback.data in ("content_analysis", "quoting", "lit_list", "libraries",
                           "hist_rev", "laws", "experience"):
        await callback.answer(text="Функция находится в разработке")

@callback_router.callback_query(VKR_States.practice)
async def practice(callback: CallbackQuery, state: FSMContext):
    if callback.data == "VKR":
        await callback.message.edit_text(reply_markup=vkr().as_markup(), text="Что именно тебе нужно по ВКР 😇?")
        await state.clear()
    elif callback.data in ("doc_analysis", "survey", "expert_survey", "focus_group", 
                           "tools", "respondents", "ethics", "passage", "analis"):
        await callback.answer(text="Функция находится в разработке")
    elif callback.data == "interview":
        await callback.message.edit_text(reply_markup=survey().as_markup(), text="Как проводить интервью")
    elif callback.data == "empirical_part":
        await callback.message.edit_text(text="Как делать практику?\nЗдесь собраны основные практические методы исследования", reply_markup=practical_part().as_markup())

@callback_router.callback_query(VKR_States.structure)
async def structure_proc(callback: CallbackQuery, state: FSMContext):
    
    full_callback = callback.data.split(":")
    data = await state.get_data()

    if callback.data == "VKR":
        await callback.message.edit_text(reply_markup=vkr().as_markup(), text="Что именно тебе нужно по ВКР 😇?")
        await state.clear()
    elif callback.data == "structure":
        await callback.message.edit_text(text="Давай разберёмся со Структурой ВКР 🧐", reply_markup=StructureVKR().structure().as_markup())
    elif "actuality" in callback.data:

        try:
            data = await state.get_data() 
            fst_cb = data["first_entry_cd"]
        except KeyError:
            await state.update_data(first_entry_cd=callback.data)
            data = await state.get_data()
            fst_cb = data["first_entry_cd"]
        
        if len(full_callback) == 2:
            temp_menu = await callback.message.edit_text(text="Что именно тебе нужно по актуальности", reply_markup=StructureVKR().fork(prev_callback=fst_cb).as_markup())
            await state.update_data(temp_menu=temp_menu)
        else:
            if callback.data == "structure":
                await callback.message.edit_text(text="Давай разберёмся со Структурой ВКР 🧐", reply_markup=StructureVKR().structure().as_markup())
            else:    
                page_number = int(full_callback[2])
                op_type = full_callback[1]
                fork_status = full_callback[0]
            
                if fork_status == "theory":
                    match page_number:
                        case 1:
                            await callback.message.edit_text(text="Актуальность подчеркивает наличие проблемы, ее значимость и необходимость новых методов ее решения. 😊\n\nОбрати внимание на компоненты актуальности 😉:\n- проблема, противоречие\n- необходимость действий, перемен\n- новизна\n- значимость исследования\n\nДля актуальности выделен отдельный абзац во введении. В нем нужно в нескольких предложениях подчеркнуть нерешенность проблемы, степень ее изученности и новизну, ссылаясь на другие исследования. 📜", reply_markup=page_surfer(page_n=page_number, callback_data=f"{fork_status}:{op_type}").as_markup())
                        case 2:
                            await callback.message.edit_text(text="Чем я ещё могу тебе помочь?", reply_markup=end_of_proc("actuality", "actuality").as_markup())
                        case 0:
                            await callback.message.edit_text(text="Что именно тебе нужно по актуальности", reply_markup=StructureVKR().fork(prev_callback=fst_cb).as_markup())
                else:
                    match page_number:
                        case 1:
                            data = await state.get_data()
                            await data["temp_menu"].delete()
                            temp_menu = await bot.send_photo(chat_id=TempData.user_id, photo=PHOTO_ID_TWO, caption="Что если актуальность не очевидна с первого взгляда? 😳", reply_markup=page_surfer(page_n=page_number, callback_data=f"{fork_status}:{op_type}").as_markup())
                            await state.update_data(temp_menu=temp_menu)
                        case 2:
                            data = await state.get_data()
                            await data["temp_menu"].delete()
                            temp_menu = await callback.message.answer(text="Можно проанализировать следующие критерии 🤔:\n- степень изученности проблемы\n- эффективность ранних и текущих мер\n- потребности науки и отрасли.\n\nМожно посмотреть последние научные разработки по теме, частоту выхода в свет исследований в рамках данной и смежных тем, наличие текущих дискуссий. 🤓\nОбрати внимание на доступность и количество материалов по теме.\n\nИзбегай таких ошибок, как:\n- слишком сложная формулировка\n- слабая аргументация\n- несовпадение с темой\n- заимствования (плагиат) ⛔️", 
                                                                      reply_markup=page_surfer(page_n=page_number, callback_data=f"{fork_status}:{op_type}").as_markup())
                            await state.update_data(temp_menu=temp_menu)
                        case 3:
                            await callback.message.edit_text(text="Чем я ещё могу тебе помочь?", reply_markup=end_of_proc("actuality", "actuality").as_markup())
                        case 0:
                            await data["temp_menu"].delete()
                            temp_menu = await callback.message.answer(text="Что именно тебе нужно по актуальности", reply_markup=StructureVKR().fork(prev_callback=fst_cb).as_markup())
                            await state.update_data(temp_menu=temp_menu)
   
    elif callback.data == "problem:1":
        await first_state_entry(cb_data=callback,
                                state_tuple=(state, VKR_States.problem),
                                cb_text="Проблема - это противоречивая ситуация, требующая разрешения. ⚠️ Проблема возникает тогда, когда прежнего знания становится недостаточно, а новое еще не приняло развитой формы.")
    elif callback.data == "goal:1":
        await first_state_entry(cb_data=callback,
                                state_tuple=(state, VKR_States.goal),
                                cb_text="Цель исследования - это конечный результат, которого хотел бы достичь исследователь при завершении своей работы. 🧐")
    elif callback.data == "obj_sbj:1":
        await first_state_entry(cb_data=callback,
                                state_tuple=(state, VKR_States.object),
                                cb_text="Простыми словами 😉:\nОбъект — это что-то (кто-то), что (кого) ты планируешь изучать.\nПредмет – характеристика или определенные функции этого объекта, которые каким-то образом могут на него влиять.")
    elif callback.data == "hypothesis:1":
        await first_state_entry(cb_data=callback,
                                state_tuple=(state, VKR_States.hypothesis),
                                cb_text="Гипотеза - это научное предположение, дающее объяснение каких-либо фактов, явлений и процессов, которое надо подтвердить или опровергнуть. 🧐")
    elif "theme" in callback.data:
        
        try:
            data = await state.get_data() 
            fst_cb = data["first_entry_cd"]
        except KeyError:
            await state.update_data(first_entry_cd=callback.data)
            data = await state.get_data()
            fst_cb = data["first_entry_cd"]
        
        if len(full_callback) == 2:
            temp_menu = await callback.message.edit_text(text="Что именно тебе нужно по теме", reply_markup=StructureVKR().fork(prev_callback=fst_cb).as_markup())
            await state.update_data(temp_menu=temp_menu)
        else:
            if callback.data == "structure":
                await callback.message.edit_text(text="Давай разберёмся со Структурой ВКР 🧐", reply_markup=StructureVKR().structure().as_markup())
            else:    
                page_number = int(full_callback[2])
                op_type = full_callback[1]
                fork_status = full_callback[0]

            if fork_status == "theory":
                match page_number:
                    case 1:
                        await callback.message.edit_text(text="Обрати внимание!❗️\nТему работы ОЧЕНЬ важно правильно сформулировать.\nКакие могут возникнуть проблемы? 😖:\n- Несоответствие темы и содержания материала;\n- Отсутствие конкретики в заголовке или непосредственно работе;\n- Размытость или неточность выражений.\nВсё это может помешать тебе на защите, поэтому отнесись к формулировке серьезно. 🧐\nНо не бойся! В тему можно вносить корректировки\n\nПараметры достойной темы 😎:\n- Актуальность, значимость\n- Четкость, ясность\n- Отражение сути проекта\n- Краткость и емкость\n\nЧто еще? 🤔:\n- Наименование проекта должно подчеркивать его суть, отмечая, что автор изучил и к чему стремился;\n- Тема и цель исследования должны пересекаться тесным образом, но при этом не дублировать (копировать) друг друга;\n- В названии работы должны прослеживаться направление исследования, объект и предмет;\n- Заглавие соответствует принципу актуальности (то есть изучаемая проблема до сих пор не нашла окончательного решения);\n- Тема должна вызывать интерес не только у автора, но и у читателя, поэтому приветствуется оригинальность и креативность (но всего должно быть в меру);\n- Наименование проекта формулируется кратко и емко в простой форме (без сложных оборотов и конструкций, вводных конструкций и пр.);\n- Заглавие должно подчеркивать уникальность проекта, то есть именно в таком ракурсе, с таким арсеналом инструментов ранее исследование не проводилось;\n- Заглавие проекта подчеркивает его значимость и призывает к конкретным действиям.", 
                                                         reply_markup=page_surfer(page_n=page_number, callback_data=f"{fork_status}:{op_type}").as_markup())    
                    case 2:
                        await callback.message.edit_text(text="Чем я ещё могу тебе помочь?", reply_markup=end_of_proc("theme", "theme").as_markup())
                    case 0:
                        await callback.message.edit_text(text="Что именно тебе нужно по теме", reply_markup=StructureVKR().fork(prev_callback=fst_cb).as_markup())
            else:
                match page_number:
                    case 1:
                        data = await state.get_data()
                        await data["temp_menu"].delete()
                        temp_menu = await bot.send_photo(chat_id=TempData.user_id, photo=PHOTO_ID_ONE, caption="Вот полезные слова", reply_markup=page_surfer(page_n=page_number, callback_data=f"{fork_status}:{op_type}").as_markup())
                        await state.update_data(temp_menu=temp_menu)
                    case 2:
                        data = await state.get_data()
                        await data["temp_menu"].delete()
                        await callback.message.answer(text="Чем я ещё могу тебе помочь?", reply_markup=end_of_proc("theme", "theme").as_markup())
                        await state.clear()
                    case 0:
                        await data["temp_menu"].delete()
                        temp_menu = await callback.message.answer(text="Что именно тебе нужно по теме", reply_markup=StructureVKR().fork(prev_callback=fst_cb).as_markup())
                        await state.update_data(temp_menu=temp_menu)
          
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
                await callback.message.edit_text(text="Давай разберёмся со Структурой ВКР 🧐", reply_markup=StructureVKR().structure().as_markup())
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
                await callback.message.edit_text(text="Давай разберёмся со Структурой ВКР 🧐", reply_markup=StructureVKR().structure().as_markup())
                await state.set_state(VKR_States.structure)  
       
@callback_router.callback_query(VKR_States.object)
async def object_proc(callback: CallbackQuery, state: FSMContext):
    
    if "obj_sbj" in callback.data:
        full_callback = callback.data.split(":")
        page_number = int(full_callback[1])
        cb_data = full_callback[0]
        
        match page_number:
            case 1:
                await callback.message.edit_text(text="Простыми словами 😉:\nОбъект — это что-то (кто-то), что (кого) ты планируешь изучать.\nПредмет – характеристика или определенные функции этого объекта, которые каким-то образом могут на него влиять.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 2:
                await callback.message.edit_text(text="Объект – это процесс / явление / комплекс процессов, который ты хочешь изучить, исследовать, определить.\nНапример,\n- сообщество / группа 👩🧑\n- погодное явление ☔️\n- банковская структура / зона управления / распределение (ресурсов, финансов, энергозатрат, рынка, и пр.) 🏦\n- философское понятие ⭐️\n- микроорганизмы, металл, материал, территориальная зона 🗿\nи т.д.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 3:
                message_change = callback.message.edit_text(text="Предмет исследования – это часть объекта, его составляющая или компонента его системы.\nЭто могут быть любые свойства данного объекта / его характеристики, которые вы запланировали изучить, классифицировать, проанализировать, упорядочить, определить соотношение между их отдельными элементами и т.д.\nНапример,\n- некое состояние / статус объекта, которое изменяется определенным образом под влиянием факторов 📈\n- процесс изменения таких факторов ↗️\n- порядок их взаимодействия друг с другом ↔️\n- определение их характерных черт ✨\n- порядок их взаимного влияния или их влияния на объект исследования 🔄\nи т.п.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                message_send = callback.message.answer(text="Предмет исследования – это часть объекта, его составляющая или компонента его системы.\nЭто могут быть любые свойства данного объекта / его характеристики, которые вы запланировали изучить, классифицировать, проанализировать, упорядочить, определить соотношение между их отдельными элементами и т.д.\nНапример,\n- некое состояние / статус объекта, которое изменяется определенным образом под влиянием факторов 📈\n- процесс изменения таких факторов ↗️\n- порядок их взаимодействия друг с другом ↔️\n- определение их характерных черт ✨\n- порядок их взаимного влияния или их влияния на объект исследования 🔄\nи т.п.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                await inner_block(coroutine_obj=(message_change, message_send), state=state)
            case 4:
                data = await state.get_data()
                await data["temp_menu"].delete()
                temp_menu = await bot.send_photo(chat_id=TempData.user_id, photo=PHOTO_ID_THREE, caption="Вот несколько примеров 😇", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                await state.update_data(temp_menu=temp_menu)
            case 5:
                data = await state.get_data()
                await data["temp_menu"].delete()
                await callback.message.answer(text="Чем я ещё могу тебе помочь?", reply_markup=end_of_proc("obj_sbj").as_markup())
                await state.clear()
            case 0:
                await callback.message.edit_text(text="Давай разберёмся со Структурой ВКР 🧐", reply_markup=StructureVKR().structure().as_markup())
                await state.set_state(VKR_States.structure)  
          
@callback_router.callback_query(VKR_States.hypothesis)
async def hypothesis_proc(callback: CallbackQuery, state: FSMContext):
    
    if "hypothesis" in callback.data:
        full_callback = callback.data.split(":")
        page_number = int(full_callback[1])
        cb_data = full_callback[0]
        
        match page_number:
            case 1:
                await callback.message.edit_text(text="Гипотеза - это научное предположение, дающее объяснение каких-либо фактов, явлений и процессов, которое надо подтвердить или опровергнуть. 🧐", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 2:
                await callback.message.edit_text(text="Виды гипотез 🤔:\n- описательные (предполагающие существование какого-либо явления / процесса)\n- объяснительные (вскрывающие причины явления / процесса)\n- описательно-объяснительные", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 3:
                message_change = callback.message.edit_text(text='Гипотеза должна:\n- быть простой (меньше возможных допущений 🤨)\n- быть проверяемой при данном уровне знаний (не бери на себя слишком много 😊)\n- содержать предположение ("если... то", "при условии, что..." 🤔)\n- не противоречить установленным научным фактам 🙅‍♀️', reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                message_send = callback.message.answer(text='Гипотеза должна:\n- быть простой (меньше возможных допущений 🤨)\n- быть проверяемой при данном уровне знаний (не бери на себя слишком много 😊)\n- содержать предположение ("если... то", "при условии, что..." 🤔)\n- не противоречить установленным научным фактам 🙅‍♀️', reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                await inner_block(coroutine_obj=(message_change, message_send), state=state)
            case 4:
                data = await state.get_data()
                await data["temp_menu"].delete()
                temp_menu = await bot.send_photo(chat_id=TempData.user_id, photo=PHOTO_ID_FOUR, caption="Вот способы построения гипотезы 🤔\nИ помни 🤓\nОдно исследование - одна гипотеза", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
                await state.update_data(temp_menu=temp_menu)
            case 5:
                data = await state.get_data()
                await data["temp_menu"].delete()
                await callback.message.answer(text="Чем я ещё могу тебе помочь?", reply_markup=end_of_proc("hypothesis").as_markup())
                await state.clear()
            case 0:
                await callback.message.edit_text(text="Давай разберёмся со Структурой ВКР 🧐", reply_markup=StructureVKR().structure().as_markup())
                await state.set_state(VKR_States.structure)  
          
@callback_router.callback_query(VKR_States.methods)
async def methods_proc(callback: CallbackQuery, state: FSMContext):
    
    if "all_methods" in callback.data:
        page_number = 999 ; method_type = ""
        data = await state.get_data()

        try:
            await message_delition(data["msg_buffer"])
        except (KeyError, TelegramBadRequest):
            pass
    
        try:
            full_callback = callback.data.split(":")
            page_number = int(full_callback[1])
            cb_data = full_callback[0]
        except ValueError:
            full_callback = callback.data.split(":")
            method_type = full_callback[1]
        
        match page_number:
            case 1:
                await callback.message.edit_text(text="""Разберемся с понятиями 🧐\n\nМетодология – система принципов организации научного исследования, способов достижения и построение научного диагноза.\n\nМетодология:\n-учит, как надо действовать ученому или практику, чтобы получить истинный результат;\n-исследует внутренние механизмы, логику движения и организации знания;\n-выявляет законы функционирования и изменения знания;\n-изучает объяснительные схемы науки и т.п.""", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 2:
                await callback.message.edit_text(text="Методика – это конкретное воплощение метода как выработанного способа организации взаимодействия субъекта и объекта исследования на основе конкретного материала и конкретной процедуры.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 3:
                await callback.message.edit_text(text="""Метод (от греч. methodos - путь исследования, теория, учение) - "способ достижения какой-либо цели, решения конкретной задачи; совокупность приемов или операций практического и теоретического освоения (познания) действительности". \nОсновная функция метода - внутренняя организация и регулирование процесса познания и практического преобразования того или иного объекта. Поэтому метод (в той или иной своей форме) сводится к совокупности определенных правил, приемов, способов, норм познания и действия.""", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())
            case 4:
                await callback.message.edit_text(text="Ознакомимся с видами методов в исследовании", reply_markup=methods().as_markup())
            case 0:
                await callback.message.edit_text(text="Давай разберёмся со Структурой ВКР 🧐", reply_markup=vkr().as_markup())
                await state.clear() 
            
        match method_type:
            case "back_to_methods":
                await callback.message.edit_text(text="Ознакомимся с видами методов в исследовании", reply_markup=methods().as_markup())                            
    elif callback.data == "structure":
        await callback.message.edit_text(text="Давай разберёмся со Структурой ВКР 🧐", reply_markup=vkr().as_markup())
        await state.clear() 
    elif "gen_methods" in callback.data:
        data = await state.get_data()
        page_number = 999 ; method_type = ""
        
        try:
            await message_delition(data["msg_buffer"])
        except (KeyError, TelegramBadRequest):
            pass
        
        try:
            full_callback = callback.data.split(":")
            page_number = int(full_callback[1])
            cb_data = full_callback[0]
        except ValueError:
            full_callback = callback.data.split(":")
            method_type = full_callback[1]
        
        match page_number:
            case 1:
                await callback.message.edit_text(text="Теоретические методы являются универсальными и служат для систематизации фактов в научной работе.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())    
            case 2:
                await callback.message.edit_text(text="Теоретические методы", reply_markup=methods(methods_type="general").as_markup())    
            case 0:
                await callback.message.edit_text(text="Ознакомимся с видами методов в исследовании", reply_markup=methods().as_markup())

        match method_type:
            case "analysis":
                message_one = await callback.message.answer(text="Анализ ✏️\n\nНаиболее часто используемый метод.\nМетодологическая основа исследования, которая опирается на анализ, призвана разложить предмет или описываемое явление на признаки и свойства, чтобы изучить его более конкретно.\nВ качестве примера можно привести частые сравнения разных художественных стилей, автомобильных характеристик разных марок, стилей выражения мыслей писателей и так далее.")
                message_two = await callback.message.answer(text="Синтез 🔍\n\nВ отличие от анализа синтез соединяет отдельные элементы (свойства, признаки) в единое целое для более детального изучения.\nМетоды синтеза и анализа часто используют вместе как методологическую основу исследования. Это позволяет сначала найти различия, а потом элементы, которые объединяют полученные результаты.")
                await state.update_data(msg_buffer=(message_one, message_two))
            case "modeling":
                message_one = await callback.message.answer(text="Моделирование 🌐\n\nПри этом методе объект исследования, существующий в реальности, переносится в искусственно созданную модель. Делается это с целью более успешного моделирования ситуаций и получения итогов, которые трудно было бы достичь в действительности.")
                await state.update_data(msg_buffer=(message_one,))
            case "analogy":
                message_one = await callback.message.answer(text="Аналогия 👯\n\nПри методологической основе в виде аналогии производится поиск сходства предметов и явлений по определённым признакам. И на этом сходстве делают выводы.")
                await state.update_data(msg_buffer=(message_one,))
            case "de&in_duction":
                message_one = await callback.message.answer(text="Дедукция 🌏➡️💁‍♀️\n\nМетод дедукции позволяет сделать выводы об определённых явлениях и предметах, основываясь на общих данных. Здесь действует принцип от общего к частному.")
                message_two = await callback.message.answer(text="Индукция 💁‍♀️➡️🌏\n\nВ противоположность к дедукции индуктивный метод основан на принципе от частного к общему. И побуждает вести рассуждения от конкретных моментов к общей картине.")
                await state.update_data(msg_buffer=(message_one, message_two))
            case "summarize":
                message_one = await callback.message.answer(text="Обобщение 🤲\n\nМетод обобщения чем-то схож с дедукцией. Здесь также делается общий вывод о предметах или явлениях на основе многих мелких признаков.\nСпециалисты различают:\n- индуктивное обобщение (эмпирическое) — переход от более конкретных свойств или характеристик предмета и явления к более общим;\n- аналитическое обобщение — переход от одного мнения к другому в ходе мыслительного процесса без применения эмпирической действительности, то есть конкретных опытов.")
                await state.update_data(msg_buffer=(message_one,))
            case "classification":
                message_one = await callback.message.answer(text="Классификация ↙️⬇️↘️\n\nМетод классификации подразумевает деление предмета или явления на группы по определённым признакам. Основная задача этого метода — структурировать, сделать информацию более чёткой и понятной для усвоения.")
                message_two = await callback.message.answer(text="Классифицировать можно на основе разных признаков. 🤔\n\nНапример:\n- по физическим свойствам (весу, размеру, объёму);\n- по материалу (пластик, дерево, металл, фарфор);\n- по жанрам (скульптура, живопись, литература);\n- по архитектурным стилям;\n- по геополитическим факторам;\n- по хронологии и др.")
                await state.update_data(msg_buffer=(message_one, message_two))
            case "abstracting":
                message_one = await callback.message.answer(text="Абстрагирование 🌌\n\nВ основе этого метода лежит конкретизация отдельных признаков какого-то отдельно взятого явления или предмета, которое необходимо изучить в рамках исследования. Суть абстрагирования — изучить какое-то конкретное свойство исследуемого объекта, не учитывая при этом все остальные его характеристики.")
                message_two = await callback.message.answer(text="💡 Метод абстрагирования — один из самых важных и основных методов исследования в дипломной работе гуманитарного уклона. С его помощью смогли отметить незаметные на первый взгляд, но важнейшие закономерности в таких науках, как педагогика, психология, философия.")
                await state.update_data(msg_buffer=(message_one, message_two))
            case "formalization":
                message_one = await callback.message.answer(text="Формализация 📊\n\nСуть метода формализации — передать структуру или сущность явления (объекта) через знаковую модель, используя для этого математические схемы, формулы или символы.")
                await state.update_data(msg_buffer=(message_one,))
            case "specification":
                message_one = await callback.message.answer(text="Конкретизация 👉👈\n\nПод конкретизацией понимают детальное изучение объекта или явления в реально существующих условиях.")
                await state.update_data(msg_buffer=(message_one,))        
    elif "loc_methods" in callback.data:
        data = await state.get_data()
        page_number = 999 ; method_type = ""
        
        try:
            await message_delition(data["msg_buffer"])
        except (KeyError, TelegramBadRequest):
            pass
        
        try:
            full_callback = callback.data.split(":")
            page_number = int(full_callback[1])
            cb_data = full_callback[0]
        except ValueError:
            full_callback = callback.data.split(":")
            method_type = full_callback[1]
        
        match page_number:
            case 1:
                await callback.message.edit_text(text="Эмпирические методы исследования в дипломной работе используются непосредственно для сбора конкретных данных о явлении или объекте. Эти методы помогают описать и выявить новые явления и предметы, найти закономерности или доказать гипотезы.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())    
            case 2:
                await callback.message.edit_text(text="Подробнее про эмпирические методы можно прочитать в разделе 'Эмпирическая часть' ВКР.", reply_markup=page_surfer(page_n=page_number, callback_data=cb_data).as_markup())    
            case 3:
                await callback.message.edit_text(text="Выбирай уровень 'погружения'", reply_markup=immertion_lvl().as_markup())    
            case 0:
                await callback.message.edit_text(text="Ознакомимся с видами методов в исследовании", reply_markup=methods().as_markup())
        
        match method_type:
            case "shortly_methods":
                await callback.message.edit_text(text="Практические методы", reply_markup=methods(methods_type="practical").as_markup())
            case "fully_methods":
                await state.set_state(VKR_States.practice)
                await callback.message.edit_text(text="Как делать практику?\nЗдесь собраны основные практические методы исследования", reply_markup=practical_part().as_markup())
            case "description":
                message_one = await callback.message.answer(text="Наблюдение 👀\n\nВ основе наблюдения лежит объективное восприятие действительности для сбора данных о свойствах и отношениях объектов исследования. \n\nЭтот метод открывает любое научное познание, вот почему его считают ключевым при проведении любых исследований.\n\nСуть метода состоит в том, чтобы наблюдать за объектом исследования и фиксировать любые важные изменения в форме, реакциях, свойствах или его положения в пространстве.")
                message_two = await callback.message.answer(text="Описание 👀🔍\n\nСпециалисты отмечают сходство данного метода с наблюдением. При проведении исследования методом описания фиксируют не только поведение и явления, но также внешний вид и признаки объекта изучения.")
                await state.update_data(msg_buffer=(message_one, message_two))
            case "comparison":
                message_one = await callback.message.answer(text="Сравнение 👩🧑\n\nМетод сравнения считается одним из самых популярных. Его используют для сопоставления двух или нескольких объектов исследования по какому-то одному признаку.")
                await state.update_data(msg_buffer=(message_one,))   
            case "experiment":
                message_one = await callback.message.answer(text="Эксперимент 🧪\n\nМетод эксперимента толкуется как воспроизведение наблюдения или явления в определённых условиях. Экспериментом может служить также опыт, целью которого будет проверка (опровержение или подтверждение) имеющихся положений.")
                message_two = await callback.message.answer(text="Главное — сохранить два критерия грамотного исследования: доказательность и повторяемость. Ведь задача эксперимента заключается не только в том, чтобы продемонстрировать наглядные результаты или открыть новое свойство, но и показать, что его можно повторить на практике. 💁‍♀️")
                await state.update_data(msg_buffer=(message_one, message_two))
            case "measurement":
                message_one = await callback.message.answer(text="Измерение 📏\n\nМетод измерения — один из самых эффективных. Речь идёт о фиксации каких бы то ни было физических параметров объекта исследования (объём, рост, вес, длина и прочие) с помощью единиц измерения. Результат, полученный в ходе применения данного метода, будет фиксироваться в числовом значении.")
                await state.update_data(msg_buffer=(message_one,))   
            case "modeling":
                message_one = await callback.message.answer(text="Практическое моделирование 🌐\n\nВ общем смысле модель — это структурированный уменьшенный образ чего-то, имитация одного или нескольких объектов.\n\nБез моделирования не обойтись при разработке новейших технологий, конструировании автомобилей, сооружений и так далее.")
                await state.update_data(msg_buffer=(message_one,)) 
            case "interview":
                message_one = await callback.message.answer(text="Беседа и интервью 👄👂\n\nСуть обоих методов заключается в том, чтобы найти и опросить человека, который обладает какой-либо ценной информацией об изучаемом предмете исследования.")
                message_two = await callback.message.answer(text="В чем разница между беседой и интервью? 🤷‍♂️\n\nИнтервью отличается более структурированным и регламентированным порядком: в ходе проведения интервью собеседник отвечает на чётко поставленные вопросы, которые интервьюер заготовил заранее. Кроме того, человек, задающий вопросы, никак не должен демонстрировать своё отношение.")
                await state.update_data(msg_buffer=(message_one, message_two))
            case "group":
                message_one = await callback.message.answer(text="Фокус-группа 👩🧑👩‍🦱\n\nЭто качественный метод исследования, который представляет собой групповое интервью с представителями целевой аудитории.\n\nВ процессе фокус-группы несколько человек под руководством одного или нескольких модераторов обсуждают заданную тему, высказывают свое отношение к вопросу, обмениваются мнениями, предлагают собственные идеи для разработки или продвижения товаров.")
                await state.update_data(msg_buffer=(message_one,)) 
            case "survey":
                message_one = await callback.message.answer(text="Опрос и анкетирование 📃\n\nДанные методы также имеют много общего между собой. Их суть заключается в предварительной подготовке вопросов, на которые хотят получить ответы. Отвечающим могут предоставить несколько готовых вариантов ответов на выбор.\n\nОсновное отличие опроса от анкетирования состоит в форме их проведения. Опрос, как правило, может быть как устным, так и письменным. А вот анкетирование предполагает только письменный формат. Нередко во время анкетирования ответ можно давать в графическом виде.")
                message_two = await callback.message.answer(text="💡 Плюсом этих практических методов в дипломе считается большой охват аудитории. Ведь если удалось опросить много человек, то и шансов получить более точные данные намного выше.")
                await state.update_data(msg_buffer=(message_one, message_two))
                    
@callback_router.callback_query(VKR_States.ending)
async def ending_proc(callback: CallbackQuery, state: FSMContext):
    if callback.data in ("summirize", "source_lst", "attachments"):
        await callback.answer(text="Функция находится в разработке")
    elif callback.data == "VKR":
        await callback.message.edit_text(reply_markup=vkr().as_markup(), text="Что именно тебе нужно по ВКР 😇?")
        await state.clear()
                    
@callback_router.callback_query(lambda x: x) # только в этом случае будет происходить обработка именно 
# запросов типа CallbackQuery, на что указывает собственно .callback_query 
# можно заметить, что маршрутизатор пропускает любой callback-запрос 
async def button_exe(callback: CallbackQuery, state: FSMContext): # там так же важно сохранить результат нашего
    # callback-а в виде переменной соответсвующего типа
    
    if callback.data == "VKR":
        await callback.message.edit_text(reply_markup=vkr().as_markup(), text="Что именно тебе нужно по ВКР 😇?")
    elif callback.data == "wk_type_back":
        await callback.message.edit_text(reply_markup=type_of_work().as_markup(), text="Тип научной работы")
    elif callback.data == "proc_end":
        await callback.message.edit_text(text="Всегда рад помочь! Желаю удачи!🍀")
    elif callback.data == "structure":
        await callback.message.edit_text(text="Давай разберёмся со Структурой ВКР 🧐", reply_markup=StructureVKR().structure().as_markup())
        await state.set_state(VKR_States.structure)
    elif callback.data == "sources":
        await callback.message.edit_text(text="Литобзор и работа с источниками", reply_markup=liter_review().as_markup())
        await state.set_state(VKR_States.lit_review)
    elif callback.data == "empirical_part":
        await callback.message.edit_text(text="Как делать практику?\nЗдесь собраны основные практические методы исследования", reply_markup=practical_part().as_markup())
        await state.set_state(VKR_States.practice)
    elif callback.data == "hypothesis:1":
        await first_state_entry(cb_data=callback,
                                state_tuple=(state, VKR_States.hypothesis),
                                cb_text="Гипотеза - это научное предположение, дающее объяснение каких-либо фактов, явлений и процессов, которое надо подтвердить или опровергнуть. 🧐")
    elif callback.data in ("course", "abstract", "article", "report", "content_analysis", "quoting", "lit_list", "suggest"):
        await callback.answer(text="Функция находится в разработке")
    elif callback.data == "all_methods:1":
        await first_state_entry(cb_data=callback,
                                state_tuple=(state, VKR_States.methods),
                                cb_text="""Разберемся с понятиями 🧐\nМетодология – система принципов организации научного исследования, способов достижения и построение научного диагноза.\n\nМетодология:\n-учит, как надо действовать ученому или практику, чтобы получить истинный результат;\n-исследует внутренние механизмы, логику движения и организации знания;\n-выявляет законы функционирования и изменения знания;\n-изучает объяснительные схемы науки и т.п.""")
    elif callback.data == "ending":
        await callback.message.edit_text(text="Завершающим этапом написания ВКР являются следующие блоки", reply_markup=ending().as_markup())
        await state.set_state(VKR_States.ending)




