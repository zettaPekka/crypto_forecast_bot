from aiogram.fsm.state import State, StatesGroup

class UserDataState(StatesGroup):
    trader_id = State()

class AffiliateState(StatesGroup):
    user_info = State()