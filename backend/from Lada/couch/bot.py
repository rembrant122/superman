import asyncio

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from telegram.constants import ParseMode

from _open_ai import generate_nouns_from_gpt
from db_all import (
    register_user,
    get_users_for_reminder,
    set_notify,
    get_notify_status,
    update_history,
    get_user_skills,
    get_skill_settings,
    add_or_update_skill,
    delete_skill
)
from settings import BOT_TOKEN

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
delete_queue: asyncio.Queue = asyncio.Queue()


def _main_menu(notify_enabled=True):

    toggle_text = "🔕 Не напоминать" if notify_enabled else "🔔 Напоминать"

    keyboard = [[KeyboardButton("МОИ НАВЫКИ")],
        [KeyboardButton("ДОБАВИТЬ"), KeyboardButton("УДАЛИТЬ")],
        [KeyboardButton(toggle_text)]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    tg_name = update.effective_user.username or update.effective_user.full_name
    register_user(tg_id, tg_name)
    notify_enabled = get_notify_status(tg_id)

    text = (
        f"🎉 Привет, {tg_name}!\n\n"
        "Тут вставить текст про методику"
    )
    photo_url = "https://drive.google.com/uc?export=view&id=1y8l8R8JrHxUh8mU9iRxhQ2V5mmyrB9Vc"

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=text,
        parse_mode=ParseMode.HTML,
        reply_markup=_main_menu(notify_enabled)
    )


# ---  Главное меню ---
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = update.message
    user_id = update.effective_user.id

    # только текст из главного меню
    if not message:
        return

    text = message.text

    if text in ("🔕 Не напоминать", "🔔 Напоминать"):
        new_status = text == "🔔 Напоминать"
        set_notify(user_id, new_status)
        await message.reply_text(
            "🔕 Напоминания выключены." if not new_status else "🔔 Напоминания включены.",
            reply_markup=_main_menu(new_status)
        )
        return

    if text == "ДОБАВИТЬ":
        await message.reply_text("Введите название нового навыка:")
        context.user_data["step"] = "await_skill_name"
        return

    if text == "УДАЛИТЬ":
        skills = get_user_skills(user_id)
        if not skills:
            await message.reply_text("У вас пока нет навыков.")
            return

        keyboard = [
            [InlineKeyboardButton(s["skill_name"], callback_data=f"delete_skill:{s['skill_name']}")]
            for s in skills
        ]
        keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="cancel")])

        await message.reply_text(
            "Выберите навык, который хотите удалить:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if text == "МОИ НАВЫКИ":
        skills = get_user_skills(user_id)
        if not skills:
            await message.reply_text("Навыков пока нет.")
            return
        skills_list = "\n".join(f"• {s['skill_name']} ({'Слова' if s['type'] else 'Навык'})" for s in skills)
        await message.reply_text(f"Ваши навыки:\n{skills_list}")
        return


# ---  Добавление навыка ---
async def handle_skill_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    query = update.callback_query
    user_id = update.effective_user.id
    step = context.user_data.get("step")

    if step == "await_skill_name":
        skill_name = message.text.strip()
        context.user_data["skill_name"] = skill_name
        context.user_data["step"] = "await_skill_type"
        await message.reply_text(
            f"Выберите тип для '{skill_name}':",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🗣️ СЛОВА", callback_data="skill_type:1"),
                    InlineKeyboardButton("🧠 НАВЫК", callback_data="skill_type:0")
                ]
            ])
        )
        return

    if query and query.data.startswith("skill_type:"):
        skill_type = int(query.data.split(":")[1])
        context.user_data["skill_type"] = skill_type
        skill_name = context.user_data.get("skill_name")

        if skill_type == 0:
            add_or_update_skill(user_id, skill_name, 0, 0, skill_type)
            context.user_data.clear()
            await query.message.reply_text(
                f"✅ Навык '{skill_name}' добавлен!",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🚀 Начать сейчас", callback_data=f"start_skill:{skill_name}:{skill_type}"),
                        InlineKeyboardButton("❌ Нет, позже", callback_data="cancel")
                    ]
                ])
            )
            return
        else:
            context.user_data["step"] = "await_word_count"
            await query.message.reply_text("📚 Сколько элементов тренировать за раз?")
            return

    if step == "await_word_count":
        if not message.text.isdigit():
            await message.reply_text("Введите число.")
            return
        context.user_data["count_elements"] = int(message.text)
        context.user_data["step"] = "await_time"
        await message.reply_text("⏰ Сколько секунд давать?")
        return

    if step == "await_time":
        if not message.text.isdigit():
            await message.reply_text("Введите число секунд.")
            return
        seconds = int(message.text)
        skill_name = context.user_data["skill_name"]
        skill_type = context.user_data["skill_type"]
        count = context.user_data["count_elements"]

        add_or_update_skill(user_id, skill_name, count, seconds, skill_type)
        context.user_data.clear()

        await message.reply_text(
            f"✅ Навык '{skill_name}' добавлен!",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🚀 Начать сейчас", callback_data=f"start_skill:{skill_name}:{skill_type}"),
                    InlineKeyboardButton("❌ Нет, позже", callback_data="cancel")
                ]
            ])
        )
        return


# ---  Запуск навыка (начать / позже) ---
async def handle_start_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()
    data = query.data

    if data.startswith("start_skill:"):
        _, skill_name, skill_type = data.split(":")
        skill_type = int(skill_type)

        if skill_type == 1:
            settings = get_skill_settings(user_id, skill_name)
            count = settings["count_elements"]
            seconds = settings["time_show"]

            await query.message.reply_text(f"🚀 Начинай '{skill_name}' — слова!")
            update_history(user_id, skill_name, True)
            await generate_words(update, context, count, seconds)
        else:
            await query.message.reply_text(f"🚀 Начинай '{skill_name}' — навык!")
            keyboard = [
                [InlineKeyboardButton("✅ О да!  Я  сделал это!", callback_data="next_step")],
                [InlineKeyboardButton("❌ Это не так-то просто!", callback_data="repeat_recommend")]
            ]
            await query.message.reply_text(
                "Как прошла практика?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            update_history(user_id, skill_name, True)
        return

    if data == "cancel":
        await query.message.reply_text("❌ Хорошо, позже!")
        return


async def reminds(bot):
    tg_ids = get_users_for_reminder()
    print("[USERS FOR REMINDER]", tg_ids)

    for user in tg_ids:
        tg_id = user["tg_id"]
        skills = user["skills"]
        keyboard = [
            [InlineKeyboardButton(s["skill_name"], callback_data=f"start_skill:{s['skill_name']}:{s['type']}")]
            for s in skills
        ]
        await bot.send_message(
            tg_id,
            "ПОРА ЭВОЛЮЦИОНИРОВАТЬ!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# --- хендлер ---
async def handle_skill_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # обязательно!
    if query.data.startswith("start_skill:"):
        skill_name = query.data.split(":", 1)[1]
        await query.edit_message_text(f"Запускаю навык: {skill_name}")
        await start_skill(update, context, skill_name)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Реагирует на текст: либо шаг создания навыка, либо главное меню."""
    step = context.user_data.get("step")
    if step:  # если пользователь в процессе добавления навыка
        await handle_skill_creation(update, context)
    else:     # иначе — это обычное меню
        await handle_menu(update, context)

async def handle_result_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    # из текста или контекста можно достать текущий навык
    skill_name = context.user_data.get("skill_name")
    if not skill_name and query.message.reply_to_message:
        skill_name = query.message.reply_to_message.text.strip()

    if data == "next_step":
        update_history(user_id, skill_name, True)
        await query.message.reply_text("🔥 Отлично! Продолжай в том же духе!")
    elif data == "repeat_recommend":
        update_history(user_id, skill_name, False)
        await query.message.reply_text("💪 Не сдавайся! Попробуй ещё раз чуть позже.")



# --- Удаление навыка ---
async def handle_delete_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "cancel":
        await query.message.reply_text("❌ Отменено.")
        return

    if data.startswith("delete_skill:"):
        _, skill_name = data.split(":", 1)
        user_id = update.effective_user.id
        delete_skill(user_id, skill_name)
        await query.message.reply_text(f"🗑️ Навык '{skill_name}' удалён.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    async def on_startup(app):
        scheduler.add_job(reminds, "interval", seconds=60, args=[app.bot])
        scheduler.start()
        print("✅ Scheduler started")

    app.post_init = on_startup

    # --- Команда /start ---
    app.add_handler(CommandHandler("start", start))

    # --- Удаление навыка ---
    app.add_handler(CallbackQueryHandler(handle_delete_skill, pattern="^(delete_skill:|cancel)"))

    # --- Все текстовые сообщения ---
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # --- Выбор типа навыка ---
    app.add_handler(CallbackQueryHandler(handle_skill_creation, pattern="^skill_type:"))

    # --- Запуск навыка (начать / позже) ---
    app.add_handler(CallbackQueryHandler(handle_start_skill, pattern="^(start_skill:|cancel)"))

    app.add_handler(CallbackQueryHandler(handle_result_callback, pattern="^(next_step|repeat_recommend)$"))

    app.run_polling()


if __name__ == "__main__":
    main()
