from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

TOKEN = "8092165983:AAEurAHjjOIC9YEppehS8izSr-fChN2uuqo"

class JobApplicationBot:
    def __init__(self, linkedin_cookies, internshala_cookies):
        self.linkedin_session = requests.Session()
        self.internshala_session = requests.Session()
        self.linkedin_session.cookies.update(linkedin_cookies)
        self.internshala_session.cookies.update(internshala_cookies)

    def apply_linkedin(self, job_url):
        headers = {
            "User-Agent": "Your User Agent Here",
        }
        response = self.linkedin_session.post(job_url, headers=headers)
        return response.ok

    def apply_internshala(self, job_url):
        headers = {
            "User-Agent": "Your User Agent Here",
        }
        response = self.internshala_session.post(job_url, headers=headers)
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
    await update.message.reply_text("Please enter your LinkedIn cookies in the format 'cookie_name=cookie_value; ...'")

async def handle_cookies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cookies_input = update.message.text
    try:
        cookies = dict([cookie.split('=') for cookie in cookies_input.split('; ')])
        
        # Ask for job URLs
        await update.message.reply_text("Please enter the LinkedIn job URL you want to apply to:")

        # Here, wait for the user to send the job URL
        # This can be improved by saving the state to capture the next message as the URL

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}. Please enter your cookies again.")

# Create the Application instance
app = ApplicationBuilder().token(TOKEN).build()

# Add command handlers
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(CommandHandler('apply_jobs', apply_jobs))

# Handle messages that are not commands (to input cookies)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_cookies))

# Start the bot
app.run_polling()
