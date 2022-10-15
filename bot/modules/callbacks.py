from pyrogram.types import CallbackQuery
from bot import LOGGER, filenames


@app.on_callback_query()
async def cb(app, update: CallbackQuery):
    cb_data = update.data
    message = update.message
    user_id = update.from_user.id
    directory = f"/usr/src/app/extracted/{user_id}/"
    dl_directory = f"/usr/src/app/Download/{user_id}/"
    if cb_data.startswith('c'):
        user = cb_data.split('|')[-1]
        filename = filenames[user]
        dl_loc = f"{dl_directory}{filename}"
        out_loc = f"{directory}{filename}"
        try:
            total = humanbytes(os.stat(dl_loc).st_size)
            current = humanbytes(os.stat(out_loc).st_size)
        except Exception as e:
            LOGGER.error(e)
        await app.answer_callback_query(update.id, text=f"STATS\n\nTotal : {total}\nDone : {current}", show_alert=True)