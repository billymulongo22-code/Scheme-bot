from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# 👉 PUT YOUR KEYS HERE
import os

TELEGRAM_BOT_TOKEN = os.getenv("8292906924:AAHK1_cZjw2Lx4mjWExSs754LD81fruSO-M")
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
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content

    await update.message.reply_text(result[:4000])  # Telegram limit protection


# Run bot
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_scheme))

app.run_polling()