import asyncio
from shutil import rmtree
from time import time
import os
from bot import authorized_chats, LOGGER



async def incoming_func(app, message):
    command = message.text
    user_id = message.from_user.id
    mess = message.reply_to_message
    st = time()
    thumbnail = None
    download_location = f"/usr/src/app/Download/{user_id}/"
    ext_location = f"/usr/src/app/extracted/{user_id}/"
    thumb_path = f"/usr/src/app/thumb/{message.from_user.id}.jpg"
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
                msg = await message.reply("**Compressing...**", quote=True)
                filename = os.path.basename(file_name)
                os.makedirs(ext_location)
                out = f"{ext_location}{filename}"
                await compress(file_name, out, msg, user_id)
                msg = await message.reply("**Trying to upload...**")
                prog = Progress(msg, file_name, st)
                await download.upload(
                    file_name,
                    msg,
                    thumbnail,
                    prog.up_progress
                )
                await msg.delete()
                await message.reply("Uploaded Successfully!")

            elif mess.text.startswith("http"):
                try:
                    c = mess.text.split(" | ")
                    url = c[0]
                    new_name = c[1]
                except:
                    url = mess.text
                    new_name = ""
                file_name = await download.download_from_link(url)
                if file_name is False:
                    return
                else:
                    if command.lower().endswith('compress'):
                        msg = await message.reply("**Compressing...**", quote=True)
                        filename = os.path.basename(file_name)
                        os.makedirs(ext_location)
                        out = f"{ext_location}{filename}"
                        await compress(file_name, out, msg, user_id)
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


        elif not res:
            await message.reply("<b>Ongoing Process Found!</b> Please wait until it's complete", quote=True)
            return

    else:
        lol = await message.reply_text("Reply to a <b>Direct Link or Telegram Media</b>", quote=True)
        await asyncio.sleep(20)
        await message.delete()
        await lol.delete()
        return