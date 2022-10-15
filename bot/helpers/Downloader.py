import asyncio
import os
from time import time
from bot.helpers.dl_progress import Progress
from bot.helpers.aria_start import add_url, aria_start, progress_aria
from bot import LOGGER, filenames
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from shutil import rmtree
from pyrogram.errors import FloodWait


class Downloader:
    def __init__(self, client, message):
        self.msg = message
        self.client = client
        self.st = time()
        self.user = message.from_user.id
        self.download_location = f"/usr/src/app/Download/{self.user}/"

    async def download_from_link(self, url):

        if url.startswith("http"):
            msg = await self.msg.reply("**Checking...**", quote=True)
            await asyncio.sleep(2)
            aria_i = await aria_start()
            done, gid = add_url(aria_i, url, self.download_location)
            file = await progress_aria(aria_i, gid, msg, self.user)
            if file is None:
                await msg.delete()
                return False
            else:
                file_name = f"{self.download_location}{file}"
                return file_name

    async def download_from_file(self, app):
        mess = self.msg.reply_to_message
        if mess.media:
            message = await self.msg.reply("**Checking...**")
            file = [mess.document, mess.video, mess.audio]
            file_name = [fi for fi in file if fi is not None][0].file_name
            file_loc = f"{self.download_location}{file_name}"
            prog = Progress(message, file_name, self.st)
            file = await app.download_media(
                mess,
                file_loc,
                progress=prog.dl_progress
            )
            return file_loc


    async def upload(self, local_file_name, message, thumbnail, progress):
        file_name = os.path.basename(local_file_name)
        LOGGER.info(f"uploading : {file_name}")
        stats = os.stat(local_file_name)
        size = stats.st_size / (1024 * 1024)
        if size < 1950.00:
            try:
                total = await message.reply_document(
                    document=local_file_name,
                    thumb=thumbnail,
                    caption=f"<code>{file_name}</code>",
                    disable_notification=True,
                    progress=progress
                )
                clean_all(self.download_location)

            except Exception as e:
                LOGGER.error(e)
            except FloodWait as fd:
                await asyncio.sleep(fd.value)
            return
        else:
            message.edit(f"Can't Upload :( Due to Telegram Limitation\n\n**Size :** {round(size, 2)}MiB")
            return

def clean_all(dl_loc):
    LOGGER.info("Cleaning...")
    try:
        rmtree(dl_loc)
    except Exception as e:
        pass


async def compress(local_file, out, message, user):
    filename = os.path.basename(local_file)
    filenames.update({f"{user}" : f"{filename}"})
    cmd = f'ffmpeg -i "{local_file}" -preset ultrafast -c:v libx265 -crf 27 -map 0:v -c:a aac -map 0:a -c:s copy -map 0:s? "{out}" -y'
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Stats", callback_data=f"c |{user}")
            ]        
        ]
    )
    mess = await message.reply(
        f"**Compressing...**\n\n**Name** : `{filename}`", 
        reply_markup=reply_markup
        )
    proc = await asyncio.create_subprocess_shell(cmd, stderr=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    err = stderr.decode()
    if err:
        await mess.edit("**Error 🤷‍♂️**")
        LOGGER.error(err)
        return
    
    #total = humanbytes(os.stat(dl_loc).st_size)
    #current = humanbytes(os.stat(out_loc).st_size)
    await mess.edit(f"**Compressed Successfully!!**")#\n\n**Name** : `{filename}`\n**Original** : `{total}`\n**Compressed** : `{current}`")
    return out


def humanbytes(size: int):
    if not size:
        return "N/A"
    power = 2 ** 10
    n = 0
    dic_powern = {0: " ", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {dic_powern[n]}B"