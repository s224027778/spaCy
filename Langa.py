#!/usr/bin/env python3
import spacy
import random
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Predefined list of quotes
QUOTES = [
    "Believe you can and you're halfway there.",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn’t just find you. You have to go out and get it.",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Don’t stop when you’re tired. Stop when you’re done.",
    "Wake up with determination. Go to bed with satisfaction.",
    "Do something today that your future self will thank you for."
]

# Function to send a random quote
async def send_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote = random.choice(QUOTES)
    await update.message.reply_text(quote)

# Function to set a daily reminder
async def set_daily_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    time_str = context.args[0] if context.args else "09:00"
    time = datetime.datetime.strptime(time_str, "%H:%M").time()

    context.job_queue.run_daily(
        send_quote_callback,
        time=time,
        context=chat_id,
        name=str(chat_id),
    )

    await update.message.reply_text(f"Daily quote set for {time_str}.")

# Callback function to send the quote at the scheduled time
async def send_quote_callback(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(job.context, text=random.choice(QUOTES))

# Function to start the bot and greet the user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I will send you a daily inspirational quote. Type /quote to get one now or /set <HH:MM> to set a daily reminder.")

# Function to remove the daily reminder
async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    if job_removed:
        await update.message.reply_text("Daily quote reminder removed!")
    else:
        await update.message.reply_text("No active reminder to remove.")

# Helper function to remove an existing job
def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

# Function to handle messages (echo back to user)
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: '{update.message.text}'")

def main():
    application = ApplicationBuilder().token('7377395631:AAGF_7Y0FmPTSQA_Tv6KFyce1CIW8w5deXM').build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quote", send_quote))
    application.add_handler(CommandHandler("set", set_daily_quote))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()


