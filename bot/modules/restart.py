from subprocess import run as srun
from sys import executable
from os import execl

async def restart(app, message):
  msg = await message.reply("**Restarting.....**", quote=True)
  srun(["python3", "upstream.py"])
  with open(".restartmg", "w") as f:
    f.truncate(0)
    f.write(f"{msg.chat.id}\n{msg.id}\n")
  execl(executable, executable, "-m", "bot")
