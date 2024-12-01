import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import asyncio
import nest_asyncio
import re
#Test request LOL
nest_asyncio.apply()

Students = [
    "Ahmad 0955197878",
    "Kasem 0921223113",
        "Ahmad 0955197878",
    "Kasem 0921223113",
        "Ahmad 0955197878",
    "Kasem 0921223113",
        "Ahmad 0955197878",
    "Kasem 0921223113",
        "Ahmad 0955197878",
    "Kasem 0921223113",
        "Ahmad 0955197878",
    "Kasem 0921223113",
        "Ahmad 0955197878",
    "Kasem 0921223113",
]

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states
REQUEST_ID, REQUEST_PHONE, BUTTON_CHOICE, PREDEFINED_BUTTONS , REQUEST_CLASS , REQUEST_LIST= range(6)

# async def get_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

#     return ConversationHandler.END

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter your ID like 'ahmed_173916':")
    return REQUEST_ID
async def get_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_subject_class = update.message.text
    user_id = update.message.from_user.id
    pattern = r"[cC]+\d{1,2}"
    if re.fullmatch(pattern,user_subject_class):
        await update.message.reply_text("Your Class is " + user_subject_class)
        await  update.message.reply_text(Students)
        #return REQUEST_LIST
    else:
        await update.message.reply_text("Error")
        return REQUEST_CLASS
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.text
    user_id_1 = update.message.from_user.id
    pattern = r"^[A-Za-z_]+_\d{3,10}$"
    if re.fullmatch(pattern, user_id):
        context.user_data['user_id'] = user_id
        await update.message.reply_text("Thank you! Now, please enter your phone number like '09XXXXXXXX' :")
        return REQUEST_PHONE
    else:
        await update.message.reply_text("Sorry but the ID is wrong")
        return REQUEST_ID

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone_number = update.message.text
    user_id = update.message.from_user.id
    pattern = r"^\d{10,15}$"
    if re.fullmatch(pattern, phone_number):
        context.user_data['phone_number'] = phone_number

        # Send options as buttons (commands)
        await update.message.reply_text("Please choose one of the following options by sending the command:\n"
                                        "/GCS301 مهارات الحاسوب\n"
                                        "/GOE301 مدخل الى التعلم الالكتروني\n"
                                        "/BPH401 الفيزياء")
        return BUTTON_CHOICE
    else:
        await update.message.reply_text("Sorry but the number is wrong")
        return REQUEST_PHONE

async def option_a(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("You chose Option مهارات الحاسوب , enter your class like 'C1'")
    return REQUEST_CLASS

async def option_b(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("You chose Option مدخل الى التعلم الالكتروني , enter your class like 'C1'")
    return REQUEST_CLASS

async def option_c(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("You chose Option الفيزياء , enter your class like 'C1'")
    return REQUEST_CLASS

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

async def main() -> None:
    application = ApplicationBuilder().token('TOKEN').build()

    # Set up the conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            REQUEST_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)],
            REQUEST_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            BUTTON_CHOICE: [
                CommandHandler("GCS301", option_a),
                CommandHandler("GOE301", option_b),
                CommandHandler("BPH401", option_c),
            ],
            REQUEST_CLASS : [MessageHandler(filters.TEXT & ~filters.COMMAND, get_class)],
            #REQUEST_LIST : [MessageHandler(filters.TEXT & ~filters.COMMAND, get_list)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(conv_handler)
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
