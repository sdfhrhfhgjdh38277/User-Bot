from pyrogram import Client, filters
import asyncio
import logging
import tracemalloc
import tracemalloc
from Commands import all_commands

tracemalloc.start()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Client("my_account")


@app.on_message(filters.command("type", prefixes="."))
async def typing(_, message):
	await all_commands.type_command(_, message)


@app.on_message(filters.command("ask_gpt", prefixes="."))
async def typing(_, message):
	await all.commands.gpt(_, message)
	
	
def main():
	logger.info("UserBot started")
	app.run()
	

main()