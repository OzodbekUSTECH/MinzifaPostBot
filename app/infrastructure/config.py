from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


class Settings(BaseSettings):
    CHANNEL_ID: str
    TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

