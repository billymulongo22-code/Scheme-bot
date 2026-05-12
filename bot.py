from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os

# Load secrets from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("8292906924:AAHjgMruitNDsI-x6OPkstV5Pta-8p-TnGI")
OPENAI_API_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_API_KEY)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a subject like:\nForm 2 Biology Term 1\nand I will generate a scheme of work."
    )

# Message handler
async def generate_scheme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    prompt = f"""
    Generate a detailed Scheme of Work for:
    {user_input}

    Include:
    - Weekly breakdown
    - Topics
    - Subtopics
    - Learning outcomes
    - Simple teacher-friendly format
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content

    await update.message.reply_text(result[:4000])  # Telegram message limit


# Run bot
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_scheme))

print("Bot is running...")
app.run_polling()