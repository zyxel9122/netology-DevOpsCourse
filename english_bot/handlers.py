import sqlite3
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import database as db

# Состояния для разговоров (если используем пошаговые диалоги)
ADD_WORD, DELETE_WORD = range(2)

# Клавиатура основного меню
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("➕ Добавить слово"), KeyboardButton("📖 Мой словарь")],
        [KeyboardButton("🎓 Тренировка"), KeyboardButton("📊 Статистика")],
        [KeyboardButton("❓ Помощь"), KeyboardButton("🗑 Удалить слово")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я бот для изучения английских слов.\n"
        "Используй кнопки ниже для управления.",
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 Доступные действия:\n"
        "➕ Добавить слово — добавить новое слово с переводом.\n"
        "📖 Мой словарь — показать все твои слова.\n"
        "🎓 Тренировка — проверить знание слов.\n"
        "📊 Статистика — твоя успеваемость.\n"
        "🗑 Удалить слово — удалить слово из словаря.\n"
        "❓ Помощь — эта подсказка."
    )
    await update.message.reply_text(text, reply_markup=get_main_keyboard())

async def handle_menu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "➕ Добавить слово":
        await update.message.reply_text("Отправь мне слово и перевод в формате: слово перевод (пример необязателен)\nНапример: dog собака")
        # Переходим в состояние ожидания добавления
        return ADD_WORD

    elif text == "📖 Мой словарь":
        words = db.get_user_words(user_id)
        if not words:
            await update.message.reply_text("У тебя пока нет слов. Добавь через кнопку «➕ Добавить слово».")
        else:
            lines = []
            for w, t, e in words:
                line = f"{w} — {t}"
                if e:
                    line += f" (пример: {e})"
                lines.append(line)
            await update.message.reply_text("Твои слова:\n" + "\n".join(lines))

    elif text == "🎓 Тренировка":
        word_data = db.get_random_word(user_id)
        if not word_data:
            await update.message.reply_text("Сначала добавь слова через кнопку «➕ Добавить слово».")
            return
        word_id, word, translation = word_data
        context.user_data['current_word_id'] = word_id
        context.user_data['current_word'] = word
        context.user_data['current_translation'] = translation

        # Создаём инлайн-кнопки для ответа
        keyboard = [
            [InlineKeyboardButton("✅ Знаю", callback_data="know")],
            [InlineKeyboardButton("❌ Не знаю", callback_data="dont_know")],
            [InlineKeyboardButton("👀 Показать перевод", callback_data="show_translation")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Переведи слово: {word}", reply_markup=reply_markup)

    elif text == "📊 Статистика":
        conn = sqlite3.connect(db.DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM user_words WHERE user_id=?", (user_id,))
        total = cur.fetchone()[0]
        cur.execute('''
            SELECT SUM(times_asked), SUM(correct_answers) FROM user_words WHERE user_id=?
        ''', (user_id,))
        row = cur.fetchone()
        asked = row[0] or 0
        correct = row[1] or 0
        conn.close()
        percent = (correct / asked * 100) if asked > 0 else 0
        await update.message.reply_text(
            f"📊 Статистика:\n"
            f"Всего слов: {total}\n"
            f"Показов: {asked}\n"
            f"Правильных ответов: {correct}\n"
            f"Точность: {percent:.1f}%"
        )

    elif text == "🗑 Удалить слово":
        await update.message.reply_text("Введи слово, которое хочешь удалить:")
        return DELETE_WORD

    elif text == "❓ Помощь":
        await help_command(update, context)

    # Если не подошло ни одно из значений, просто проигнорируем
    return ConversationHandler.END

async def add_word_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка ввода слова для добавления
    user_id = update.effective_user.id
    text = update.message.text.strip()
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await update.message.reply_text("Неверный формат. Отправь слово и перевод через пробел.\nНапример: dog собака")
        return ADD_WORD  # остаёмся в том же состоянии

    word = parts[0]
    rest = parts[1]
    rest_parts = rest.split(maxsplit=1)
    translation = rest_parts[0]
    example = rest_parts[1] if len(rest_parts) > 1 else None

    if db.word_exists(user_id, word):
        await update.message.reply_text(f"Слово '{word}' уже есть в словаре.", reply_markup=get_main_keyboard())
        return ConversationHandler.END

    db.add_word(user_id, word, translation, example)
    await update.message.reply_text(f"Слово '{word}' добавлено!", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def delete_word_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка ввода слова для удаления
    user_id = update.effective_user.id
    word = update.message.text.strip()
    if not word:
        await update.message.reply_text("Введи слово для удаления:")
        return DELETE_WORD

    if not db.word_exists(user_id, word):
        await update.message.reply_text(f"Слово '{word}' не найдено в твоём словаре.", reply_markup=get_main_keyboard())
        return ConversationHandler.END

    db.delete_word(user_id, word)
    await update.message.reply_text(f"Слово '{word}' удалено.", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def inline_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if 'current_word_id' not in context.user_data:
        await query.edit_message_text("Сначала начни тренировку через кнопку «🎓 Тренировка».")
        return

    word_id = context.user_data['current_word_id']
    word = context.user_data['current_word']
    translation = context.user_data['current_translation']
    action = query.data

    if action == "know":
        db.update_stat(word_id, correct=True)
        await query.edit_message_text(f"✅ Правильно! Слово '{word}' — {translation}")
    elif action == "dont_know":
        db.update_stat(word_id, correct=False)
        await query.edit_message_text(f"❌ Неправильно. Правильный перевод: {translation}")
    elif action == "show_translation":
        await query.edit_message_text(f"Перевод слова '{word}': {translation}")

    # Очищаем данные текущей тренировки
    context.user_data.pop('current_word_id', None)
    context.user_data.pop('current_word', None)
    context.user_data.pop('current_translation', None)

    # Предлагаем продолжить
    await query.message.reply_text("Чтобы продолжить тренировку, нажми кнопку «🎓 Тренировка»", reply_markup=get_main_keyboard())

# Заглушка для обработки обычных текстовых сообщений, не попадающих в диалоги
async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я не понимаю эту команду. Используй кнопки меню.", reply_markup=get_main_keyboard())
