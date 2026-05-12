from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os

# Load secrets from environment variables 
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8292906924:AAHjgMruitNDsI-x6OPkstV5Pta-8p-TnGI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
async def set_commands(app):
    commands = [
        BotCommand("start", "Start bot"),
        BotCommand("help", "Help"),
        BotCommand("scheme", "Generate scheme"),
        BotCommand("lessonplan", "Generate lesson plan"),
        BotCommand("notes", "Generate notes"),
        BotCommand("quiz", "Generate quiz"),
        BotCommand("timetable", "Generate timetable"),
    ]
    await app.bot.set_my_commands(commands)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Scheme Bot!\n\n"
        "/scheme\n"
        "/lessonplan\n"
        "/notes\n"
        "/quiz\n"
        "/timetable"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Example:\n"
        "/scheme Grade 10 Physics Term 2"
    )


async def scheme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Generating scheme...")


async def lessonplan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Generating lesson plan...")


async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Generating notes...")


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Generating quiz...")


async def timetable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Generating timetable...")
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
app = ApplicationBuilder().token("8292906924:AAHBzK4u8zMbkRLwO2kAfBlFL_bU9v0L0VU").post_init(set_commands).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_scheme))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("scheme", scheme))
app.add_handler(CommandHandler("lessonplan", lessonplan))
app.add_handler(CommandHandler("notes", notes))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CommandHandler("timetable", timetable))
print("Bot is running...")
app.run_polling()