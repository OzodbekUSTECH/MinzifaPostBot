from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.presentation.aiogram_bot.v1.enums import ButtonNames


def get_types_of_posts_rkb_buttons() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=ButtonNames.TEXT_BUTTON.value))
    builder.add(KeyboardButton(text=ButtonNames.MEDIA_BUTTON.value))
    builder.add(KeyboardButton(text=ButtonNames.BACK_BUTTON.value))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_cancel_rkb_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=ButtonNames.CANCEL_BUTTON.value))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_post_or_ready_rkb_buttons() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=ButtonNames.POST_TO_CHANNEL_BUTTON.value))
    builder.add(KeyboardButton(text=ButtonNames.READY_BUTTON.value))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
