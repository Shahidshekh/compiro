import asyncio
from shutil import rmtree
from time import time
import os
from bot import authorized_chats, LOGGER
from bot.helpers.Downloader import Downloader, compress
from bot.helpers.dl_progress import Progress



async def incoming_func(app, message):
    command = message.text
    user_id = message.from_user.id
    mess = message.reply_to_message
    st = time()
    thumbnail = None
    download_location = f"/usr/src/app/Download/{user_id}/"
    ext_location = f"/usr/src/app/extracted/{user_id}/"
    thumb_path = f"/usr/src/app/thumb/{message.from_user.id}.jpg"
    download = Downloader(app, message)
    if os.path.exists(thumb_path):
        thumbnail = thumb_path
    reso = search(authorized_chats, str(message.chat.id))
    if not reso:
        await message.reply(text="I'm not familiar to this chat...\nPlease Contact @the_fourth_minato for authorization", quote=True)
        return
         
    if mess:
        if reso:
            if mess.media and user_id:
                file_name = await download.download_from_file(app)
                LOGGER.info(f"Downloaded : {file_name}")
                filename = os.path.basename(file_name)
                try:
                    os.makedirs(ext_location)
                except Exception:
                    pass
                    
                out = f"{ext_location}{filename}"
                cfile= await compress(file_name, out, message, user_id)
                msg = await message.reply("**Trying to upload...**")
                prog = Progress(msg, file_name, st)
                await download.upload(
                    cfile,
                    msg,
                    thumbnail,
                    prog.up_progress
                )
                await msg.delete()
                await message.reply("Uploaded Successfully!")

            elif mess.text.startswith("http"):
                file_name = await download.download_from_link(url)
                if file_name is False:
                    return
                else:
                    if command.lower().endswith('compress'):
                        filename = os.path.basename(file_name)
                        try:
                            os.makedirs(ext_location)
                        except Exception:
                            pass

                        out = f"{ext_location}{filename}"
                        await compress(file_name, out, message, user_id)
                        msg = await message.reply("**Trying to upload...**", quote=True)
                        await asyncio.sleep(3)
                        prog = Progress(msg, file_name, st)
                        try:
                            await download.upload(
                                file_name,
                                msg,
                                thumbnail,
                                prog.up_progress
                            )
                            await message.reply("Uploaded Successfully!", quote=True)
                        except Exception as e:
                            LOGGER.error(e)

            else:
                await message.reply_text("Doesn't seem to be a <b>Download Source</b>", quote=True)

            clean_all(download_location, ext_location)


        elif not res:
            await message.reply("<b>Ongoing Process Found!</b> Please wait until it's complete", quote=True)
            return

    else:
        lol = await message.reply_text("Reply to a <b>Direct Link or Telegram Media</b>", quote=True)
        await asyncio.sleep(20)
        await message.delete()
        await lol.delete()
        return


def search(listed, item):
    for i in range(len(listed)):
        if listed[i] == item:
            return True
    return False

def clean_all(dl_loc, ext_loc):
    LOGGER.info("Cleaning...")
    try:
        rmtree(dl_loc)
        rmtree(ext_loc)
    except Exception as e:
        pass