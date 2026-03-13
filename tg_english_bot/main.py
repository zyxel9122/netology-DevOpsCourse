import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import database as db
import handlers

# Вставьте свой токен, полученный от BotFather
TOKEN = "YOUR_BOT_TOKEN"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def main():
    # Инициализация БД
    db.init_db()

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help_command))
    application.add_handler(CommandHandler("add", handlers.add_command))
    application.add_handler(CommandHandler("list", handlers.list_command))
    application.add_handler(CommandHandler("learn", handlers.learn_command))
    application.add_handler(CommandHandler("stats", handlers.stats_command))
    application.add_handler(CommandHandler("delete", handlers.delete_command))

    # Обработчик текстовых сообщений (для ответов в тренировке)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_message))

    # Запуск бота (polling)
    application.run_polling()

if __name__ == "__main__":
    main()
