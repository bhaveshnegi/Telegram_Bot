from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

# Replace with your actual Telegram Bot Token
TOKEN = "8092165983:AAEurAHjjOIC9YEppehS8izSr-fChN2uuqo"

class JobApplicationBot:
    def __init__(self, linkedin_cookies, internshala_cookies):
        self.linkedin_session = requests.Session()
        self.internshala_session = requests.Session()
        self.linkedin_session.cookies.update(linkedin_cookies)
        self.internshala_session.cookies.update(internshala_cookies)

    def apply_linkedin(self, job_url):
        # Placeholder for the actual LinkedIn job application logic
        response = self.linkedin_session.post(job_url)
        return response.status_code == 200

    def apply_internshala(self, job_url):
        # Placeholder for the actual Internshala job application logic
        response = self.internshala_session.post(job_url)
        return response.status_code == 200

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
    # Here you can handle the cookie input from the user
    cookies_input = update.message.text
    try:
        # Split the cookies and create a dictionary
        cookies = dict([cookie.split('=') for cookie in cookies_input.split('; ')])

        # Placeholder for actual job URLs
        linkedin_job_url = "https://www.linkedin.com/jobs/example-job"  # Replace with actual LinkedIn job URL
        internshala_job_url = "https://internshala.com/internship/example-job"  # Replace with actual Internshala job URL

        # Create a job application bot instance with cookies
        bot_instance = JobApplicationBot(cookies, cookies)

        # Apply for jobs
        linkedin_success = bot_instance.apply_linkedin(linkedin_job_url)
        internshala_success = bot_instance.apply_internshala(internshala_job_url)

        if linkedin_success and internshala_success:
            await update.message.reply_text("Successfully applied for jobs on LinkedIn and Internshala.")
        else:
            await update.message.reply_text("Failed to apply for jobs. Please check your cookies and try again.")
    
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
