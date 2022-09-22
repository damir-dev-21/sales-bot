from aiogram.bot.base import Union
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import get_categories

menu_cd = CallbackData("show_menu", "level", "category",
                       "subcategory", "item_id")

calculate_cd = CallbackData("calc","action","item_id","numeral","sample_quantity")

def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(level=level, category=category, subcategory=subcategory, item_id=item_id)

async def calculate_inline(item_id: int, sample_quantity: Union[int,str]=0):
    markup = InlineKeyboardMarkup(row_width=3)

    for i in range(1,10):
        markup.insert(
            InlineKeyboardButton(text=str(i),
                                callback_data=calculate_cd.new(
                                    action="quantity",
                                    item_id=item_id,
                                    numeral=i,
                                    sample_quantity=sample_quantity
                                ))
        )

    markup.row(
        InlineKeyboardButton(
            text="⬅️",
            callback_data=calculate_cd.new(
                action="erase",
                item_id=item_id,
                numeral='unknown',
                sample_quantity=sample_quantity
            )
        ),
        InlineKeyboardButton(
            text=str(0),
            callback_data=calculate_cd.new(
                action="quantity",
                item_id=item_id,
                numeral=0,
                sample_quantity=sample_quantity
            )
        ),
        
        InlineKeyboardButton(
            text="✅",
            callback_data=calculate_cd.new(
                action="order",
                item_id=item_id,
                numeral='unknown',
                sample_quantity=sample_quantity
            )
        ),
    )    

    return markup

    


async def categories_keyboard():
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup()

    categories = await get_categories()

    button_text = f"Поиск 🔍"

    markup.insert(
        InlineKeyboardButton(text=button_text
                             ,switch_inline_query_current_chat="")
    )

    return markup
