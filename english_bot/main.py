import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
import database as db
import handlers

TOKEN = "871523885.......dlxHIA"  # замени на свой токен

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def main():
    # Инициализация БД
    db.init_db()

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд (на случай, если пользователь введёт команду вручную)
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help_command))

    # Диалог добавления слова
    conv_handler_add = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("➕ Добавить слово"), handlers.handle_menu_buttons)],
        states={
            handlers.ADD_WORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.add_word_received)]
        },
        fallbacks=[CommandHandler("start", handlers.start)]
    )
    application.add_handler(conv_handler_add)

    # Диалог удаления слова
    conv_handler_delete = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("🗑 Удалить слово"), handlers.handle_menu_buttons)],
        states={
            handlers.DELETE_WORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.delete_word_received)]
        },
        fallbacks=[CommandHandler("start", handlers.start)]
    )
    application.add_handler(conv_handler_delete)

    # Обработчик для остальных кнопок меню (которые не запускают диалоги)
    application.add_handler(MessageHandler(
        filters.Text(["📖 Мой словарь", "🎓 Тренировка", "📊 Статистика", "❓ Помощь"]),
        handlers.handle_menu_buttons
    ))

    # Обработчик инлайн-кнопок
    application.add_handler(CallbackQueryHandler(handlers.inline_button_handler))

    # Обработчик неизвестных текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.unknown_message))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
