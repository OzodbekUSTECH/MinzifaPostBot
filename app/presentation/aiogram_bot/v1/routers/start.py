from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.presentation.aiogram_bot.v1.keyboards.start import get_start_rkb_buttons

router = Router()


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(
        text="Привет! Здесь ты можешь создать пост с кнопками :)",
        reply_markup=get_start_rkb_buttons()
    )




