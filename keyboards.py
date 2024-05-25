from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup # импортируем объект кнопки 
from aiogram.utils.keyboard import InlineKeyboardBuilder # импортируем объект клавиатуры

def type_of_work():
    kb_type_of_work = InlineKeyboardBuilder() # создаем экземпляр класса клавиатуры 

    btn_abstract = InlineKeyboardButton(text="Реферат", callback_data="abstract") # и создаем экземпляр класса 
    btn_article = InlineKeyboardButton(text="Научная статья", callback_data="article")
    btn_report = InlineKeyboardButton(text="Доклад", callback_data="report")
    btn_course = InlineKeyboardButton(text="Курсовая работа", callback_data="course")
    btn_vkr = InlineKeyboardButton(text="ВКР", callback_data="VKR")
    btn_feedback = InlineKeyboardButton(text="Предложить улучшение\идею", callback_data="suggest")

    kb_type_of_work.add(btn_abstract, btn_article, btn_report, btn_course, btn_vkr, btn_feedback)
    kb_type_of_work.adjust(1) # .add(...) добавляет кнопку к клавиатуре, а .adjust(...) придает форму
    return kb_type_of_work 

def vkr():
    kb_about_vkr = InlineKeyboardBuilder()
    btn_structure = InlineKeyboardButton(text="Введение в ВКР", callback_data="structure")
    btn_sources = InlineKeyboardButton(text="Теоретический Модуль", callback_data="sources")
    btn_methods = InlineKeyboardButton(text="Материалы и Методы", callback_data="all_methods:1")
    btn_empirical_part = InlineKeyboardButton(text="Эмпирическая Составляющая", callback_data="empirical_part")
    btn_ending = InlineKeyboardButton(text="Заключение", callback_data="ending")
    btn_back = InlineKeyboardButton(text="Назад к типам работы", callback_data="wk_type_back")
   
    kb_about_vkr.add(btn_structure, btn_sources, btn_methods, btn_empirical_part, btn_ending, btn_back)
    kb_about_vkr.adjust(1) 
    return kb_about_vkr

def end_of_proc(block_type: str, op_type: str = "none"):
    kb_end = InlineKeyboardBuilder()

    btn_ending = InlineKeyboardButton(text="Спасибо, на этом все", callback_data="proc_end")
    btn_back = InlineKeyboardButton(text="Назад к ВКР", callback_data="VKR")
    btn_bk_structure = InlineKeyboardButton(text="Назад к введению", callback_data="structure")
    # btn_sources = InlineKeyboardButton(text="Работа с источниками", callback_data="sources")
    btn_bk_fork = InlineKeyboardButton(text="Назад к выбору методологии", callback_data=f"theory:{op_type}:0")
    hypothesis = InlineKeyboardButton(text="Гипотеза", callback_data="hypothesis:1")
    
    if block_type == "theme":
        kb_end.add(btn_bk_fork, btn_back, btn_ending)
    elif block_type == "actuality":
        kb_end.add(btn_bk_fork, btn_ending, btn_back, btn_bk_structure)
    elif block_type in ("problem", "obj_sbj", "hypothesis"):
        kb_end.add(btn_bk_fork, btn_ending, btn_back, btn_bk_structure)
    elif block_type == "goal":
        kb_end.add(btn_bk_fork, btn_ending, btn_back, hypothesis, btn_bk_structure)

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

class StructureVKR():
    
    def __init__(self) -> None:
        self.btn_theme = InlineKeyboardButton(text="Тема", callback_data="theme:1")
        self.btn_actuality = InlineKeyboardButton(text="Актуальность, новизна", callback_data="actuality:1")
        self.btn_problem = InlineKeyboardButton(text="Проблема", callback_data="problem:1")
        self.btn_purpose = InlineKeyboardButton(text="Цель, задачи", callback_data="goal:1")
        self.btn_obj_sbj = InlineKeyboardButton(text="Объект, предмет", callback_data="obj_sbj:1")
        self.btn_hypothesis = InlineKeyboardButton(text="Гипотеза", callback_data="hypothesis:1")
        self.btn_back_to_vkr = InlineKeyboardButton(text="Назад к ВКР", callback_data="VKR")
        self.btn_bk_structure = InlineKeyboardButton(text="Назад к введению", callback_data="structure")

    def structure(self):
        kb_structure = InlineKeyboardBuilder()
        
        kb_structure.add(self.btn_theme, self.btn_actuality, self.btn_problem, 
                         self.btn_purpose, self.btn_obj_sbj, self.btn_hypothesis, self.btn_back_to_vkr)
        kb_structure.adjust(1)
        return kb_structure 
    
    def fork(self, prev_callback):
        kb_fork = InlineKeyboardBuilder()
        theor_pt = InlineKeyboardButton(text="Теоретическая часть", callback_data=f"theory:{prev_callback}")
        emphir_pt = InlineKeyboardButton(text="Эмпирическая часть", callback_data=f"practice:{prev_callback}") 
        
        kb_fork.add(theor_pt, emphir_pt, self.btn_bk_structure)
        kb_fork.adjust(1)
        return kb_fork
        
def methods(methods_type: str = None):
    kb_methods = InlineKeyboardBuilder()
    
    btn_general = InlineKeyboardButton(text="Общие (теоретические)", callback_data="gen_methods:1")
    btn_local = InlineKeyboardButton(text="Частные (эмпирические)", callback_data="loc_methods:1")
    btn_bk_structure = InlineKeyboardButton(text="Назад к ВКР", callback_data="structure")
    
    btn_analysis = InlineKeyboardButton(text="Анализ, синтез", callback_data="gen_methods:analysis")
    btn_modeling = InlineKeyboardButton(text="Моделирование", callback_data="gen_methods:modeling")
    btn_analogy = InlineKeyboardButton(text="Аналогия", callback_data="gen_methods:analogy")
    btn_de_in_duction = InlineKeyboardButton(text="Дедукция, индукция", callback_data="gen_methods:de&in_duction")
    btn_summarize = InlineKeyboardButton(text="Обобщение", callback_data="gen_methods:summarize")
    btn_classification = InlineKeyboardButton(text="Классификация", callback_data="gen_methods:classification")
    btn_abstracting = InlineKeyboardButton(text="Абастрагирование", callback_data="gen_methods:abstracting")
    btn_formalization = InlineKeyboardButton(text="Формализация", callback_data="gen_methods:formalization")
    btn_specification = InlineKeyboardButton(text="Конкретизация", callback_data="gen_methods:specification")
    btn_back_to_methods = InlineKeyboardButton(text="Назад к видам методов", callback_data="all_methods:back_to_methods")
    btn_description = InlineKeyboardButton(text="Наблюдение, описание", callback_data="loc_methods:description")
    btn_comparison = InlineKeyboardButton(text="Сравнение", callback_data="loc_methods:comparison")
    btn_experiment = InlineKeyboardButton(text="Эксперимент", callback_data="loc_methods:experiment")
    btn_measurement = InlineKeyboardButton(text="Измерение", callback_data="loc_methods:measurement")
    btn_modeling = InlineKeyboardButton(text="Практическое моделирование", callback_data="loc_methods:modeling")
    btn_interview = InlineKeyboardButton(text="Беседа, интервью", callback_data="loc_methods:interview")
    btn_group = InlineKeyboardButton(text="Фокус-группа", callback_data="loc_methods:group")
    btn_survey = InlineKeyboardButton(text="Опрос, анкетирование", callback_data="loc_methods:survey")
    
    if methods_type == None:
        kb_methods.add(btn_general, btn_local, btn_bk_structure)
    elif methods_type == "general":
        kb_methods.add(btn_analysis, btn_modeling, btn_analogy, btn_de_in_duction, btn_summarize, 
                       btn_classification, btn_abstracting, btn_formalization,btn_specification, btn_back_to_methods)
    elif methods_type == "practical":
        kb_methods.add(btn_description, btn_comparison, btn_experiment, btn_measurement, 
                    btn_modeling,btn_interview, btn_group, btn_survey, btn_back_to_methods)
    kb_methods.adjust(1)
    return kb_methods

def immertion_lvl():
    kb_immertion = InlineKeyboardBuilder()
    
    btn_shortly = InlineKeyboardButton(text="Кратко о каждом методе", callback_data="loc_methods:shortly_methods")
    btn_fully = InlineKeyboardButton(text="Подробно о практике", callback_data="loc_methods:fully_methods")
    btn_back_to_methods = InlineKeyboardButton(text="Назад к видам методов", callback_data="all_methods:back_to_methods")

    kb_immertion.add(btn_shortly, btn_fully, btn_back_to_methods)
    kb_immertion.adjust(1)
    return kb_immertion

def liter_review():
    kb_review = InlineKeyboardBuilder()
    
    btn_hist_rev = InlineKeyboardButton(text="Ист-обзор по проблеме", callback_data="hist_rev")
    btn_lows = InlineKeyboardButton(text="Обзор законов", callback_data="laws")
    btn_exper = InlineKeyboardButton(text="Опыт", callback_data="experience")
    btn_libraries = InlineKeyboardButton(text="Библиотеки и БЦ", callback_data="libraries")
    btn_content = InlineKeyboardButton(text="Контент-анализ", callback_data="content_analysis")
    btn_quoting = InlineKeyboardButton(text="Правила цитирования", callback_data="quoting")
    btn_list = InlineKeyboardButton(text="Список литературы", callback_data="lit_list")
    
    btn_vkr_back = InlineKeyboardButton(text="Назад к ВКР", callback_data="VKR")
    
    kb_review.add(btn_hist_rev, btn_lows, btn_exper, btn_libraries, btn_content, btn_quoting, btn_list, btn_vkr_back)
    kb_review.adjust(1)
    return kb_review

def practical_part():
    kb_practical = InlineKeyboardBuilder()
    
    btn_doc_analysis = InlineKeyboardButton(text="Анализ документов", callback_data="doc_analysis")
    btn_survey = InlineKeyboardButton(text="Анкетирование", callback_data="survey")
    btn_expert_survey = InlineKeyboardButton(text="Экспертный опрос", callback_data="expert_survey")
    btn_focus_group = InlineKeyboardButton(text="Фокус-группа", callback_data="focus_group")
    btn_interview = InlineKeyboardButton(text="Интервью", callback_data="interview")    
    btn_vkr_back = InlineKeyboardButton(text="Назад к ВКР", callback_data="VKR")
    
    kb_practical.add(btn_doc_analysis, btn_survey, btn_expert_survey,
                     btn_focus_group, btn_interview, btn_vkr_back)
    kb_practical.adjust(1)
    return kb_practical

def survey():
    kb_survey = InlineKeyboardBuilder()
    
    btn_tools = InlineKeyboardButton(text="Инструментарий", callback_data="tools")
    btn_respondents = InlineKeyboardButton(text="Респонденты", callback_data="respondents")
    btn_ethics = InlineKeyboardButton(text="Этика", callback_data="ethics")
    btn_passage = InlineKeyboardButton(text="Проведение", callback_data="passage")
    btn_interview = InlineKeyboardButton(text="Анализ", callback_data="analis")
    btn_empirical_part = InlineKeyboardButton(text="Назад к практике", callback_data="empirical_part")
    
    kb_survey.add(btn_tools, btn_respondents, btn_ethics,
                     btn_passage, btn_interview, btn_empirical_part)
    kb_survey.adjust(1)
    return kb_survey

def ending():
    kb_ending = InlineKeyboardBuilder()
    btn_summ = InlineKeyboardButton(text="Вывод", callback_data="summirize")
    btn_source = InlineKeyboardButton(text="Список Источников", callback_data="source_lst")
    btn_attach = InlineKeyboardButton(text="Приложения", callback_data="attachments")
    btn_back_to_vkr = InlineKeyboardButton(text="Назад к ВКР", callback_data="VKR")

    kb_ending.add(btn_summ, btn_source, btn_attach, btn_back_to_vkr)    
    kb_ending.adjust(1)
    return kb_ending
    
    