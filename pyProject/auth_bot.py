import logging

from datetime import datetime, timedelta

# 설정 관련 variables
last_message_time = {}
token = "6836424743:AAH1VjpxMAop4Fw1o0OP0A0-WqL640Hnr2A"
adminChatId = -4059875363 # 수락해주는방
channelId = -1002146066434 # 수락한사람 초대되는 채널

from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, Updater, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("텔레그램 닉네임과 스샷의 닉네임을 같게 만드세요. 그리고 스샷을 업로드하세요. 한시간에 한번만 업로드 가능합니다.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("텔레그램 닉네임과 스샷의 닉네임을 같게 만드세요. 그리고 스샷을 업로드하세요. 한시간에 한번만 업로드 가능합니다.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def attachment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # log user name
    logger.info(f"Received from {update.message.from_user.name}.")

    # log type of attachment
    logger.info(f"Received {update.message.document.mime_type} attachment.")

    # if file is ePub, convert the epub to txt and send it back
    if update.message.document.mime_type == "application/epub+zip":
        # log user name
        logger.info(f"Received from {update.message.from_user.name}.")
        logger.info(f"Start processing {update.message.document.file_name}.")

        # get file object
        file = await context.bot.get_file(update.message.document.file_id)

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    now = datetime.now()

    if user_id in last_message_time and now - last_message_time[user_id] < timedelta(minutes=60):
        # If the user has sent a message in the last minute, ignore the message or send a warning
        await update.message.reply_text("1시간에 한번만 요청할수있습니다")
        return

    # Update the last message time for the user
    last_message_time[user_id] = now

    # log user name
    logger.info(f"Received from {update.message.from_user.name}.")

    # log type of attachment
    logger.info(f"Received {update.message.photo} attachment.")

    # forward this message to group chat id -4008155612
    # message with choice of approve / decline
   

    await context.bot.forward_message(chat_id=adminChatId,
                                       from_chat_id=update.message.chat_id,
                                         message_id=update.message.message_id)
    
    # user id as a string
    user_id = str(update.message.from_user.id)

    keyboard = [
        [
            InlineKeyboardButton("수락", callback_data=user_id),
            InlineKeyboardButton("거절", callback_data="2"),
        ]
    ]
    
    # parse userid to send message to
    userid = update.message.from_user.id

    reply_markup = InlineKeyboardMarkup(keyboard)

    # send message to adminChatId with inline keyboard
    await context.bot.send_message(chat_id=adminChatId, 
                                   text=f"유저: {update.message.from_user.name}\n요청을 수락하시겠습니까?",
                                   reply_markup=reply_markup)
    
    # response to user
    await update.message.reply_text("요청 전송 완료")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()
        
    if query.data == "2":
        await query.edit_message_text(text=f"거절")
        return
    else:
        await query.edit_message_text(text=f"수락")
    
    # invitation link must be 1 time usage only
    inviteLink = await context.bot.create_chat_invite_link(chat_id=channelId, member_limit=1)

    await context.bot.send_message(chat_id= query.data, text=f"요청이 수락되었습니다. 이 초대 링크는 1회용입니다.\n\n {inviteLink.invite_link}")

def main() -> None:    
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    application.add_handler(CallbackQueryHandler(button))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()