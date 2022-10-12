from subprocess import run as srun
from sys import executable
from os import execl

def restart(app, message):
  msg = await message.reply("**Restarting.....**", quote=True)
  srun(["python3", "upstream.py"])
  execl(executable, executable, "-m", "bot")
