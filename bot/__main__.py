from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.handlers import MessageHandler
from bot.modules.restart import restart
from bot import LOGGER


if __name__ == "__main__":
    app = Client(
        "hello",
        api_id=11873433,
        api_hash="96abaf0d59cd1f5482bdc93ba6030424",
        bot_token="5269784341:AAFAz_umXmT9iaj5ds5mlZK0Jh0AwaT6hRQ"
    )
app.start()


@app.on_message(filters.command('start'))
async def start_command(app, message):
    help_button = [
        [
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("Owner", url="https://t.me/the_fourth_minato")
        ]
    ]
    user = message.from_user.username
    name = message.from_user.first_name
    await message.reply_text(f"Hello <a href='t.me/{user}'>{name}</a>! 😉\n\nThis is a compressor bot and "
                             f"can do a lot of things. 😁\nStill under Devlopment so u can may Encounter some errors. /restart "
                             f"\n\nMaintained and Purely coded by :\n\n@The_Fourth_Minato 💫",
                             quote=True,
                             reply_markup=InlineKeyboardMarkup(help_button)
                             )
    
restaer_handler = MessageHandler(
    restart,
    filters=filters.command('restart')
)
app.add_handler(restart)
    
LOGGER.info("The Bot Has Been Started 😎")

idle()

app.stop()
