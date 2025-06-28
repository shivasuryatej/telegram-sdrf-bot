from telegram.ext import Updater, CommandHandler
from docxtpl import DocxTemplate
import os

# Read bot token securely from Railway environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

# List of required placeholders
REQUIRED_KEYS = [
    'reference_from', 'reporting_officer', 'no', 'date', 'reference',
    'reference_date', 'no_of_persons', 'location', 'time', 'deployment'
]

def start(update, context):
    update.message.reply_text(
        "Welcome to SDRF Document Bot!\n\n"
        "To generate a document, use this command:\n\n"
        "/generate reference_from=... reporting_officer=... no=... date=... reference=... reference_date=... no_of_persons=... location=... time=... deployment=..."
    )

def generate(update, context):
    try:
        args = context.args
        data = {}

        for arg in args:
            key, value = arg.split('=')
            data[key] = value

        # Check for missing placeholders
        missing_keys = [key for key in REQUIRED_KEYS if key not in data]
        if missing_keys:
            update.message.reply_text(f"Error: Missing input(s): {', '.join(missing_keys)}")
            return

        doc = DocxTemplate("46-L&O-I-2025.docx")
        doc.render(data)

        output_path = "generated_doc.docx"
        doc.save(output_path)

        with open(output_path, 'rb') as file:
            update.message.reply_document(file)

        update.message.reply_text("Word document generated successfully!")

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", generate))

    updater.start_polling()
    updater.idle()

if _name_ == '_main_':
    main()
