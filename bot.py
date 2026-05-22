import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from github import Github

# Получаем настройки из "переменных окружения" (мы их зададим позже в сервисе)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши заголовок заявки:")
    context.user_data['step'] = 'title'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('step') == 'title':
        context.user_data['title'] = update.message.text
        context.user_data['step'] = 'body'
        await update.message.reply_text("Теперь введите описание:")
    elif context.user_data.get('step') == 'body':
        title = context.user_data['title']
        body = update.message.text
        repo.create_issue(title=title, body=body)
        await update.message.reply_text("✅ Заявка создана на GitHub!")
        context.user_data['step'] = None

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
