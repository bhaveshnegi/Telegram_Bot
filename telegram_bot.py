from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

TOKEN = "8092165983:AAEurAHjjOIC9YEppehS8izSr-fChN2uuqo"

LINKEDIN_COOKIES = {
    "li_at": "AQEDAT2ZwL8FZFp7AAABkj59npwAAAGSYooinE0AwuQtUTOs5VNV6u_tsy0aCAGyJ6oz9nIrfZSIitzvvJzq-ySMCAoxS_V_JC8d1NchPw9L-ZxNHCyJ3eKcKeFjYfK7g1xysy92ozWJRD30hz_MfU7I"
}

class JobApplicationBot:
    def __init__(self, linkedin_cookies):
        self.linkedin_session = requests.Session()
        self.linkedin_session.cookies.update(linkedin_cookies)

    def apply_linkedin(self, job_url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",  
            "Referer": "https://www.linkedin.com/",
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = self.linkedin_session.post(job_url, headers=headers)
        return response.ok

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Job Application Bot! Use /help to see available commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    """
    /start -> Welcome to the channel
    /help -> This message
    /apply_jobs -> Start applying for jobs
    """
    )

async def apply_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter the LinkedIn job URL you want to apply to:")

async def handle_job_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    job_url = update.message.text
    bot = JobApplicationBot(LINKEDIN_COOKIES)  

    if bot.apply_linkedin(job_url):
        await update.message.reply_text("Successfully applied for the job!")
    else:
        await update.message.reply_text("Failed to apply for the job. Please try again.")

# Create the Application instance
app = ApplicationBuilder().token(TOKEN).build()

# Add command handlers
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(CommandHandler('apply_jobs', apply_jobs))

# Handle messages that are not commands (to input job URL)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_job_url))

# Start the bot
app.run_polling()
