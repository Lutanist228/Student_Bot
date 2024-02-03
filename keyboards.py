from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup # импортируем объект кнопки 
from aiogram.utils.keyboard import InlineKeyboardBuilder # импортируем объект клавиатуры

def type_of_work():
    kb_type_of_work = InlineKeyboardBuilder() # создаем экземпляр класса клавиатуры 

    btn_abstract = InlineKeyboardButton(text="Реферат", callback_data="abstract") # и создаем экземпляр класса 
    btn_article = InlineKeyboardButton(text="Научная статья", callback_data="article")
    btn_report = InlineKeyboardButton(text="Доклад", callback_data="report")
    btn_course = InlineKeyboardButton(text="Курсовая работа", callback_data="course")
    btn_vkr = InlineKeyboardButton(text="ВКР", callback_data="VKR")

    kb_type_of_work.add(btn_abstract, btn_article, btn_report, btn_course, btn_vkr)
    kb_type_of_work.adjust(1) # .add(...) добавляет кнопку к клавиатуре, а .adjust(...) придает форму
    return kb_type_of_work 

def vkr():
    kb_about_vkr = InlineKeyboardBuilder()
    btn_theme = InlineKeyboardButton(text="Тема", callback_data="theme:1")
    btn_structure = InlineKeyboardButton(text="Структура", callback_data="structure")
    btn_sources = InlineKeyboardButton(text="Литературный обзор", callback_data="sources")
    btn_empirical_part = InlineKeyboardButton(text="Эмпирическая часть", callback_data="empirical_part")
    btn_back = InlineKeyboardButton(text="Назад к типам работы", callback_data="wk_type_back")
   
    kb_about_vkr.add(btn_theme, btn_structure, btn_sources, btn_empirical_part, btn_back)
    kb_about_vkr.adjust(1) 
    return kb_about_vkr

def end_of_proc(block_type: str):
    kb_end = InlineKeyboardBuilder()

    btn_ending = InlineKeyboardButton(text="Спасибо, на этом все", callback_data="proc_end")
    btn_back = InlineKeyboardButton(text="Назад к ВКР", callback_data="VKR")
    btn_bk_structure = InlineKeyboardButton(text="Вернуться к структуре", callback_data="structure")
    btn_sources = InlineKeyboardButton(text="Работа с источниками", callback_data="sources")
    hypothesis = InlineKeyboardButton(text="Гипотеза", callback_data="hypothesis:1")
    
    if block_type == "theme":
        kb_end.add(btn_back, btn_ending)
    elif block_type == "actuality":
        kb_end.add(btn_ending, btn_back, btn_bk_structure, btn_sources)
    elif block_type in ("problem", "obj_sbj", "hypothesis"):
        kb_end.add(btn_ending, btn_back, btn_bk_structure)
    elif block_type == "goal":
        kb_end.add(btn_ending, btn_back, hypothesis, btn_bk_structure)

    kb_end.adjust(1)
    return kb_end

def page_surfer(page_n, callback_data):
    kb_pages = InlineKeyboardBuilder()
    next_pg = InlineKeyboardButton(text="Далее", callback_data=f"{callback_data}:{page_n + 1}")
    back_pg = InlineKeyboardButton(text="Назад", callback_data=f"{callback_data}:{page_n - 1}")
    kb_pages.add(next_pg, back_pg)
    kb_pages.adjust(1)
    return kb_pages

def back_to_main():
    kb = [[KeyboardButton(text="Открыть главное меню")]]
    main_menu_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return main_menu_kb

def structure():
    kb_structure = InlineKeyboardBuilder()
    btn_actuality = InlineKeyboardButton(text="Актуальность, новизна", callback_data="actuality:1")
    btn_problem = InlineKeyboardButton(text="Проблема", callback_data="problem:1")
    btn_purpose = InlineKeyboardButton(text="Цель, задачи", callback_data="goal:1")
    btn_obj_sbj = InlineKeyboardButton(text="Объект, предмет", callback_data="obj_sbj:1")
    btn_hypothesis = InlineKeyboardButton(text="Гипотеза", callback_data="hypothesis:1")
    btn_methods = InlineKeyboardButton(text="Методы", callback_data="all_methods:1")
    btn_back_to_vkr = InlineKeyboardButton(text="Назад к ВКР", callback_data="VKR")

    kb_structure.add(btn_actuality, btn_problem, btn_purpose, btn_obj_sbj, btn_hypothesis, btn_methods, btn_back_to_vkr)
    kb_structure.adjust(1)
    return kb_structure 

def methods(methods_type: str = None):
    kb_methods = InlineKeyboardBuilder()
    
    btn_general = InlineKeyboardButton(text="Общие (теоретические)", callback_data="gen_methods:1")
    btn_local = InlineKeyboardButton(text="Частные (эмпирические)", callback_data="loc_methods")
    btn_bk_structure = InlineKeyboardButton(text="Вернуться к структуре", callback_data="structure")
    
    btn_analysis = InlineKeyboardButton(text="Анализ, синтез", callback_data="gen_methods:analysis")
    btn_modeling = InlineKeyboardButton(text="Моделирование", callback_data="gen_methods:modeling")
    btn_analogy = InlineKeyboardButton(text="Аналогия", callback_data="gen_methods:analogy")
    btn_de_in_duction = InlineKeyboardButton(text="Дедукция, индукция", callback_data="gen_methods:de&in_duction")
    btn_summarize = InlineKeyboardButton(text="Обобщение", callback_data="gen_methods:summarize")
    btn_classification = InlineKeyboardButton(text="Классификация", callback_data="gen_methods:classification")
    btn_abstracting = InlineKeyboardButton(text="Абастрагирование", callback_data="gen_methods:abstracting")
    btn_formalization = InlineKeyboardButton(text="Формализация", callback_data="gen_methods:formalization")
    btn_specification = InlineKeyboardButton(text="Конкретизация", callback_data="gen_methods:specification")
    btn_back_to_methods = InlineKeyboardButton(text="Назад к видам методов", callback_data="gen_methods:back_to_methods")

    if methods_type == None:
        kb_methods.add(btn_general, btn_local, btn_bk_structure)
    elif methods_type == "general":
        kb_methods.add(btn_analysis, btn_modeling, btn_analogy, btn_de_in_duction, btn_summarize, btn_classification, btn_abstracting, btn_formalization,
                       btn_specification, btn_back_to_methods)
    elif methods_type == "local":
        pass
        
    kb_methods.adjust(1)
    return kb_methods