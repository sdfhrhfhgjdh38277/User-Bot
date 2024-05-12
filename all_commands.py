from g4f.models import gpt_4
from g4f import ChatCompletion
import tracemalloc
from time import sleep 
from loguru import logger 
import asyncio
from threading import Thread 
from pyrogram.errors  import FloodWait
from time import time

async def type_command(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    text_to_be_printed = ""
    typing_symbol = "ㅤ"
    while text_to_be_printed != orig_text:
        try:
            msg.edit(text_to_be_printed + typing_symbol)
            sleep(0.05)
            
            text_to_be_printed = text_to_be_printed + text[0]
            text = text[1:]
            
            msg.edit(text_to_be_printed)
            sleep(0.05)
            
        except FloodWait as e:  
            sleep(e.x)     

                                    

async def gpt(client, message):
    question =  message.text
    message_to_send = message.text.replace('.ask_gpt', ' ')
    logger.info("Обработка успешна. Ответ генерируется")
    start_timer = time()
    answer = await ChatCompletion.create_async(model=gpt_4,    
    messages=[{"role": "user", "content": question}])
    end_timer = time()
    
    if len(answer) >= 4096:
         with open("answer.txt", "w") as file:
            file.write(answer)
            await app.send_document(message.chat.id, file, file_caption="Ответ оказался слишком большим, и записан в файл")
            
    elif len(answer) < 4096:       
        await message.reply_text(f"Gpt-answer: {answer}")
        
    all_need_time = round(end_timer - start_timer, 2)
    logger.info(f"Request generated in  {all_need_time}sec")    
    


async def helping(_, message):
	     await message.reply_text("Привет. Я - Aind, юзер-бот. Я умею: делать запросы к GPT-4, команда - .ask_gpt \n.dice - Сыграть в кости. вводить числа в диапазоне 1-6")                           
  
                                                      

async def dice(client, message):
	user_number = message.command[1] if len(message.command) > 1 else None
	if user_number and user_number.isdigit() and 1 <= int(user_number) <= 6:
		dice_result = await client.send_dice(message.chat.id)
	   
	if dice_result.dice.value != int(user_number):
		await message.reply_text("Вы ошиблись в своих догадках!")
	elif dice_result.dice.value == int(user_number):
		await message.reply_text("Поздравляю с победой!🎉")
	else:
		await message.reply_text("Введите число от 1 до 6.")
		
		
