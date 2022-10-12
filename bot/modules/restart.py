from subprocess import run as srun
from sys import executable

def restart(app, message):
  msg = await message.reply("**Restarting.....**", quote=True)
  clean_all()
  srun(["python3", "upstream.py"])
  
