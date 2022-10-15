from subprocess import run as srun
from sys import executable
from os import execl
from bot.helpers.Downloader import Downloader

async def restart(app, message):
  msg = await message.reply("**Restarting.....**", quote=True)
  srun(["python3", "upstream.py"])
  with open(".restartmg", "w") as f:
    f.truncate(0)
    f.write(f"{msg.chat.id}\n{msg.id}\n")
  execl(executable, executable, "-m", "bot")


async def log(app, message):
  dldr = Downloader(app, message)
  msg = await message.reply("sending logs...", quote=True)
  await dldr.upload("log.txt", msg, None, None)