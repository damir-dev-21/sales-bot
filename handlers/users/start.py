from aiogram.types import Message,InlineQuery,InputTextMessageContent,InlineQueryResultArticle
from aiogram.dispatcher.filters.builtin import CommandStart
from django_project.usersmanage.models import User
from django_project.sales.models import Item
from utils.db_api import db_commands as commands
from keyboards.default.main_menu import menuMain
import hashlib
from loader import dp,bot


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    user: User = await commands.add_user(user_id=message.from_user.id,
                                        full_name=message.from_user.full_name,
                                        username=message.from_user.username)

    success = user.access

    if success:
        await message.answer(
            "Welcome!" ,
            reply_markup=menuMain  
        )
    else:
        await message.answer(
            "&#128683; Доступ запрещен"
        )   

@dp.inline_handler()
async def messages(inline_query: InlineQuery):
    text = inline_query.query
    offset = inline_query.offset
    if offset:
        offset = int(offset)+20
    else:
        offset = 0
    
    all_item = map(lambda i: ' '.join(i[0].split()),list(Item.objects.filter().all().values_list('name')))
    print(all_item)
    a = []
    for s in all_item: 
        if text.lower() in s.lower():
            result_id: str = hashlib.md5(s.encode()).hexdigest()
            input_content = InputTextMessageContent(text)

            a.append(
                InlineQueryResultArticle(
                id=result_id,
                title=s,
                input_message_content=input_content,
                )
            )
    
    await bot.answer_inline_query(inline_query.id, results=a[offset:offset+5], cache_time=1,next_offset=str(offset))
