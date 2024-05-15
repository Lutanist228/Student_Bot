from aiogram.fsm.state import State, StatesGroup

class VKR_States(StatesGroup):
    topic = State()
    structure = State()
    review = State()
    research = State()
    relevance = State()
    problem = State()
    goal = State()
    object = State()
    hypothesis = State()
    methods = State()
    lit_review = State()
    practice = State()
    ending = State()
     
