from aiogram.fsm.state import State, StatesGroup


class CreatePostForm(StatesGroup):
    choosing_type = State()
    text_post = State()
    media_post = State()
    caption = State()
    buttons = State()
    sizes = State()
    confirm = State()
