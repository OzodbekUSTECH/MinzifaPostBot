from aiogram import Router, F
from aiogram.types import Message, TelegramObject
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.presentation.aiogram_bot.v1.states.posts import CreatePostForm
from app.presentation.aiogram_bot.v1.keyboards.posts import (
    get_types_of_posts_rkb_buttons,
    get_cancel_rkb_button,
    get_post_or_ready_rkb_buttons
)
from app.presentation.aiogram_bot.v1.keyboards.start import get_start_rkb_buttons
from app.infrastructure.config import bot, settings
from app.presentation.aiogram_bot.v1.enums import ButtonNames

router = Router()


@router.message(F.text == "📃 Создать пост")
async def show_types_of_posts(message: Message, state: FSMContext) -> None:
    await state.set_state(CreatePostForm.choosing_type)
    await message.answer("Выберите тип поста",
                         reply_markup=get_types_of_posts_rkb_buttons())


@router.message(CreatePostForm.choosing_type, F.text.in_({
    ButtonNames.TEXT_BUTTON.value,
    ButtonNames.MEDIA_BUTTON.value,
    ButtonNames.BACK_BUTTON.value,
}))
async def choose_post_type(message: Message, state: FSMContext) -> None:
    post_type = message.text
    if post_type == ButtonNames.BACK_BUTTON.value:
        await state.clear()
        await message.answer("Отменено. Выберите действие:", reply_markup=get_start_rkb_buttons())
    elif post_type == ButtonNames.TEXT_BUTTON.value:
        await state.set_state(CreatePostForm.text_post)
        await message.answer("Введите текст для вашего поста:", reply_markup=get_cancel_rkb_button())
    elif post_type == ButtonNames.MEDIA_BUTTON.value:
        await state.set_state(CreatePostForm.media_post)
        await message.answer("Отправьте медиа (одно фото/видео/гиф) для вашего поста:",
                             reply_markup=get_cancel_rkb_button())


@router.message(F.text == ButtonNames.CANCEL_BUTTON.value)
async def handle_cancel(message: Message, state: FSMContext) -> None:
    if await state.get_state() is None:
        return
    await state.clear()
    await message.answer("Создание поста отменено.", reply_markup=get_start_rkb_buttons())


@router.message(CreatePostForm.text_post)
async def handle_text_post(message: Message, state: FSMContext) -> None:
    await state.update_data(post_type="text", caption=message.text)
    await state.set_state(CreatePostForm.buttons)
    await message.answer(
        (
            "Введите метки и ссылки кнопок, разделённые <b>'+'</b>, и каждую кнопку через запятую "
            "без запятой в конце.\n\n"
            "<b>Пример:</b>\n"
            "Кнопка 1 + https://example.com, Кнопка 2 + https://example2.com"
        )
    )


@router.message(CreatePostForm.media_post)
async def handle_media_post(message: Message, state: FSMContext) -> None:
    content = None
    if message.photo:
        content = message.photo[-1].file_id
        await state.update_data(post_type="photo", content=content)
    elif message.video:
        content = message.video.file_id
        await state.update_data(post_type="video", content=content)
    elif message.animation:
        content = message.animation.file_id
        await state.update_data(post_type="gif", content=content)

    if content:
        await state.set_state(CreatePostForm.caption)
        await message.answer("Введите текст для вашего поста:", reply_markup=get_cancel_rkb_button())
    else:
        await message.answer("Пожалуйста, отправьте <b>фото, видео или гиф</b>, чтобы продолжить.")


@router.message(CreatePostForm.caption)
async def handle_caption(message: Message, state: FSMContext) -> None:
    await state.update_data(caption=message.text)
    await state.set_state(CreatePostForm.buttons)
    await message.answer(
        (
            "Введите метки и ссылки кнопок, разделённые <b>'+'</b>, и каждую кнопку через запятую "
            "без запятой в конце.\n\n"
            "<b>Пример:</b>\n"
            "Кнопка 1 + https://example.com, Кнопка 2 + https://example2.com"
        )
    )


@router.message(CreatePostForm.buttons)
async def handle_buttons(message: Message, state: FSMContext) -> None:
    button_data = message.text.split(',')
    builder = InlineKeyboardBuilder()

    for item in button_data:
        parts = item.strip().split(' + ')
        if len(parts) == 2:
            text, url = parts[0].strip(), parts[1].strip()
            builder.button(text=text, url=url)
        else:
            await message.answer(
                (
                    "Неверно!"
                    "Введите метки и ссылки кнопок, разделённые <b>'+'</b>, и каждую кнопку через запятую "
                    "без запятой в конце.\n\n"
                    "<b>Пример:</b>\n"
                    "Кнопка 1 + https://example.com, Кнопка 2 + https://example2.com"
                )
            )

            return

    await state.update_data(button_builder=builder)
    await state.set_state(CreatePostForm.sizes)
    await message.answer(
        (
            "Введите размеры кнопок для каждой строки, разделённые запятыми. "
            "Каждое число определяет количество кнопок в соответствующей строке.\n\n"
            "<b>Пример:</b>\n"
            "'3, 2, 1'\n\n"
            "В данном примере:\n"
            "- Первая строка будет содержать <b>3 кнопки</b>.\n"
            "- Вторая строка будет содержать <b>2 кнопки</b>.\n"
            "- Третья строка будет содержать <b>1 кнопку</b>.\n\n"
            "Если вы отправите одно число, например, '2', то каждая строка будет содержать по <b>2 кнопки</b>.\n\n"
            "Вы можете настроить кнопки в соответствии с вашими потребностями. Убедитесь, "
            "что общее количество кнопок соответствует количеству меток и ссылок, "
            "которые вы указали ранее."
        )
    )


@router.message(CreatePostForm.sizes)
async def handle_sizes(message: Message, state: FSMContext) -> None:
    try:
        sizes = [int(size.strip()) for size in message.text.split(',')]
        data = await state.get_data()
        builder = data['button_builder']
        builder.adjust(*sizes)

        post_type = data['post_type']
        content = data.get('content', '')
        caption = data.get('caption', '')

        if post_type == "text":
            await message.answer(text=caption, reply_markup=builder.as_markup())
        elif post_type == "photo":
            await message.answer_photo(photo=content, caption=caption, reply_markup=builder.as_markup())
        elif post_type == "video":
            await message.answer_video(video=content, caption=caption, reply_markup=builder.as_markup())
        elif post_type == "gif":
            await message.answer_animation(animation=content, caption=caption, reply_markup=builder.as_markup())

        await state.set_state(CreatePostForm.confirm)
        await message.answer("Отлично! Теперь вы можете переслать пост на канал или нажать 'Готово'.",
                             reply_markup=get_post_or_ready_rkb_buttons())
    except ValueError:
        await message.answer(
            "Пожалуйста, введите правильные числа, разделённые запятыми (например, '3, 2, 1'):"
        )


@router.message(CreatePostForm.confirm, F.text.in_({
    ButtonNames.POST_TO_CHANNEL_BUTTON.value,
    ButtonNames.READY_BUTTON.value
}))
async def confirm_post(message: Message, state: FSMContext) -> None:
    if message.text == ButtonNames.POST_TO_CHANNEL_BUTTON.value:
        data = await state.get_data()
        post_type = data['post_type']
        content = data.get('content', '')
        caption = data.get('caption', '')
        builder = data['button_builder']

        try:
            if post_type == "text":
                await bot.send_message(chat_id=settings.CHANNEL_ID, text=caption, reply_markup=builder.as_markup())
            elif post_type == "photo":
                await bot.send_photo(chat_id=settings.CHANNEL_ID, photo=content, caption=caption,
                                     reply_markup=builder.as_markup())
            elif post_type == "video":
                await bot.send_video(chat_id=settings.CHANNEL_ID, video=content, caption=caption,
                                     reply_markup=builder.as_markup())
            elif post_type == "gif":
                await bot.send_animation(chat_id=settings.CHANNEL_ID, animation=content, caption=caption,
                                         reply_markup=builder.as_markup())

            await message.answer("Пост был успешно отправлен на канал.", reply_markup=get_start_rkb_buttons())
        except Exception as e:
            await message.answer(f"Не удалось отправить пост на канал. Ошибка: {str(e)}",
                                 reply_markup=get_start_rkb_buttons())

    elif message.text == ButtonNames.READY_BUTTON.value:
        await message.answer("Пост готов к отправке. Вы можете переслать его на канал позже.",
                             reply_markup=get_start_rkb_buttons())

    await state.clear()


