from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
import database as db

# Состояния для разговора (если используем ConversationHandler)
ADD_WORD, LEARN_WAIT = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я бот для изучения английских слов.\n"
        "Используй /add слово перевод [пример] — добавить слово.\n"
        "/list — показать все твои слова.\n"
        "/learn — начать тренировку.\n"
        "/stats — статистика.\n"
        "/delete слово — удалить слово.\n"
        "/help — помощь."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/add слово перевод [пример] — добавить слово (пример необязателен).\n"
        "/list — список всех слов.\n"
        "/learn — случайное слово для перевода.\n"
        "/stats — твоя статистика.\n"
        "/delete слово — удалить слово."
    )

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Парсим аргументы: /add dog собака [собака гавкает]
    text = update.message.text.strip()
    parts = text.split(maxsplit=2)  # максимум 3 части: команда, слово, перевод + пример
    if len(parts) < 3:
        await update.message.reply_text("Формат: /add слово перевод [пример]")
        return
    word = parts[1]
    rest = parts[2]
    # Может быть перевод и пример через пробел, либо только перевод
    rest_parts = rest.split(maxsplit=1)
    translation = rest_parts[0]
    example = rest_parts[1] if len(rest_parts) > 1 else None

    user_id = update.effective_user.id
    if db.word_exists(user_id, word):
        await update.message.reply_text(f"Слово '{word}' уже есть в словаре.")
        return

    db.add_word(user_id, word, translation, example)
    await update.message.reply_text(f"Слово '{word}' добавлено!")

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    words = db.get_user_words(user_id)
    if not words:
        await update.message.reply_text("У тебя пока нет слов. Добавь с помощью /add")
        return
    lines = []
    for w, t, e in words:
        line = f"{w} — {t}"
        if e:
            line += f" (пример: {e})"
        lines.append(line)
    await update.message.reply_text("Твои слова:\n" + "\n".join(lines))

async def learn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    word_data = db.get_random_word(user_id)
    if not word_data:
        await update.message.reply_text("Сначала добавь слова через /add")
        return
    word_id, word, translation = word_data
    # Сохраняем в context.user_data, чтобы знать, какое слово ожидаем
    context.user_data['current_word_id'] = word_id
    context.user_data['current_word'] = word
    context.user_data['current_translation'] = translation
    await update.message.reply_text(f"Переведи слово: {word}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка ответа пользователя во время тренировки
    if 'current_word' not in context.user_data:
        await update.message.reply_text("Используй /learn, чтобы начать тренировку.")
        return
    user_answer = update.message.text.strip().lower()
    correct_translation = context.user_data['current_translation'].lower()
    word_id = context.user_data['current_word_id']
    word = context.user_data['current_word']

    # Простейшее сравнение (можно улучшить: игнорировать пунктуацию, учитывать несколько вариантов)
    if user_answer == correct_translation:
        db.update_stat(word_id, correct=True)
        await update.message.reply_text(f"✅ Правильно! Слово '{word}' — {correct_translation}")
    else:
        db.update_stat(word_id, correct=False)
        await update.message.reply_text(f"❌ Неправильно. Правильный перевод: {correct_translation}")

    # Очищаем данные текущей тренировки
    context.user_data.pop('current_word_id', None)
    context.user_data.pop('current_word', None)
    context.user_data.pop('current_translation', None)
    # Предлагаем продолжить или выйти
    await update.message.reply_text("Чтобы продолжить, нажми /learn")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect(db.DB_NAME)
    cur = conn.cursor()
    # Общее количество слов
    cur.execute("SELECT COUNT(*) FROM user_words WHERE user_id=?", (user_id,))
    total = cur.fetchone()[0]
    # Статистика ответов
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

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Укажи слово: /delete слово")
        return
    word = args[0]
    user_id = update.effective_user.id
    if not db.word_exists(user_id, word):
        await update.message.reply_text(f"Слово '{word}' не найдено в твоём словаре.")
        return
    db.delete_word(user_id, word)
    await update.message.reply_text(f"Слово '{word}' удалено.")
