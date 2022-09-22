from turtle import width
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django_project.sales.models import Item
from utils.others.uniq_filter import get_unique_types


all_items = Item.objects.filter().all()
all_goods = map(lambda i:i[0],all_items.values_list("type"))
res = get_unique_types(all_goods)

menuMain = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📦 Товары"),
            KeyboardButton(text="🛒 Корзина")
        ],
        [
            KeyboardButton(text="📖 Мои заказы"),
            KeyboardButton(text="👤 О нас")
        ],
    ],
    resize_keyboard=True
)

menuType = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⏪"),
            KeyboardButton(text="Главное меню 🏠"),
        ],  
    ],
    resize_keyboard=False,
    row_width=2
)

menuGroup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⏪"),
            KeyboardButton(text="Главное меню"),
        ],  
    ],
    resize_keyboard=False,
    row_width=3
)

menuCart = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Очистить корзину ❌"),
            KeyboardButton(text="Оформить заказ ✅")
        ],
        [
            KeyboardButton(text="Главное меню 🏠")
        ]
    ]
)

for i in res:
    menuType.insert(i)


