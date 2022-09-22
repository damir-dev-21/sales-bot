from datetime import datetime
from aiogram.utils.markdown import hbold

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton
from django_project.sales.models import Item, Order, OrderItem
from django_project.usersmanage.models import User

from keyboards.inline.main_inline import calculate_inline, menu_cd, categories_keyboard, calculate_cd
from keyboards.default.main_menu import menuMain, menuType, menuCart
from loader import dp
from states.menu_state import MenuState
from aiogram.dispatcher import FSMContext

from utils.others.uniq_filter import get_groups_of_types, get_item, get_items_of_group,get_unique_types


@dp.message_handler(content_types=['text'])
async def get_message_items(message: types.Message, state: FSMContext):
    if message.text == "📦 Товары":
        inline_markup = await categories_keyboard()
        await message.answer("Найти 🔍", reply_markup=inline_markup)

        await message.answer("Смотри что у нас есть 👇", reply_markup=menuType)

        await MenuState.TYPE.set()
    elif message.text == "📖 Мои заказы":
        user_discover = User.objects.filter(
            user_id=message.from_user.id).first()
        order_discover = Order.objects.filter(
            buyer=user_discover).filter(success=True).all()
        text_markup = "Ваши заказы: \n\n"
        for i in order_discover:
            text_markup += "Время заказа:" + \
                str(i.purchase_time) + "\nСумма: " + str(i.total) + "\n\n"

        await message.answer(text=text_markup, reply_markup=ReplyKeyboardMarkup(keyboard=[[
            KeyboardButton(text="Главное меню 🏠")
        ]]))

    elif message.text == "🛒 Корзина":
        text_markup = """Ваш заказ: \n\n"""

        user_discover = User.objects.filter(
            user_id=message.from_user.id).first()
        order_discover = Order.objects.filter(
            buyer=user_discover).filter(success=False).first()
        order_item_discover = OrderItem.objects.filter(
            order=order_discover).all()
        total = 0
        for i in order_item_discover:
            total += i.quantity * i.amount
            text_markup += hbold(i.product.name) + "\n\n" + \
                f"Кол-во: {i.quantity}, Цена: {i.amount} \n\n"

        text_markup += f"\n Всего: {hbold(total)} \n"
        if order_discover:
            await message.answer(text=text_markup, reply_markup=menuCart)
        else:
            await message.answer(text=text_markup, reply_markup=ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="Главное меню 🏠")]
            ]))

    elif message.text == "Главное меню 🏠":
        await message.answer(text="Вы в главном меню", reply_markup=menuMain)
    elif message.text == "Оформить заказ ✅":
        await message.answer("Пришлите свой телефон", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[
                KeyboardButton("Прислать телефон", request_contact=True),
                KeyboardButton("Главное меню 🏠"),
            ]], resize_keyboard=True
        ))

        await state.set_state("enter_phone")
    elif message.text == "👤 О нас":
        await message.answer("Created by Tuychiev Damir @damir1786")


@dp.message_handler(state="enter_phone", content_types=types.ContentType.CONTACT)
async def enter_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    user_discover = User.objects.filter(user_id=message.from_user.id).first()
    order_discover = Order.objects.filter(
        buyer=user_discover).filter(success=False).first()
    order_discover.success = True
    order_discover.phone_number = phone_number
    order_discover.save()
    await message.answer("Заказ оформлен ✅")
    await state.finish()


@dp.message_handler(state=MenuState.TYPE)
async def answer_type(message: types.Message, state: FSMContext):
    answer = message.text
    all_groups_of_type = get_groups_of_types(
        all_items=Item.objects.filter().all(), answer=answer)
    keyboard_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        keyboard=[
            [
                KeyboardButton(text="⏪"),
                KeyboardButton(text="Главное меню 🏠"),
            ],
        ]
    )
    for i in all_groups_of_type:
        keyboard_markup.insert(i)
    if message.text == "⏪":
        await state.reset_state(with_data=False)
        await message.answer(text="Назад", reply_markup=menuMain)
    elif message.text == "Главное меню 🏠":
        await state.reset_state(with_data=False)
        await message.answer(text="Вы в главном меню",reply_markup=menuMain)      
    else:
        await state.update_data(type=answer)
        await message.answer("Выберите вид товара: ", reply_markup=keyboard_markup)
        await MenuState.GROUP.set()


@dp.message_handler(state=MenuState.GROUP)
async def get_items(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == "⏪":
        data = await state.get_data()
        all_items = Item.objects.filter().all()
        
        all_goods = map(lambda i: i[0], all_items.values_list("type"))

        all_groups_of_type = get_unique_types(
            types=all_goods)
        keyboard_markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=2,
            keyboard=[
                [
                    KeyboardButton(text="⏪"),
                    KeyboardButton(text="Главное меню 🏠"),
                ],
            ]
        )
        for i in all_groups_of_type:
            keyboard_markup.insert(i)
        
        # await state.reset_state(with_data=False)
        await message.answer(text="Назад", reply_markup=keyboard_markup)
        await MenuState.TYPE.set()
    elif message.text == "Главное меню 🏠":
        await state.reset_state(with_data=False)
        await message.answer(text="Вы в главном меню",reply_markup=menuMain)  
    else:
        all_items_of_group = get_items_of_group(
            all_items=Item.objects.filter().all(),
            type=data.get("type"),
            group=message.text
        )
        keyboard_markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=2,
            keyboard=[
                [
                    KeyboardButton(text="⏪"),
                    KeyboardButton(text="Главное меню 🏠"),
                ],
            ]
        )
        for i in range(len(all_items_of_group)):
            if i < 100:
                keyboard_markup.insert(all_items_of_group[i])

        await state.update_data(group=message.text)

        await message.answer(text="Выберите товар", reply_markup=keyboard_markup)
        await MenuState.ITEM.set()



@dp.message_handler(state=MenuState.ITEM)
async def get_items(message: types.Message, state: FSMContext):
    await state.update_data(item=message.text)
    data = await state.get_data()
    if message.text == "⏪":
        data = await state.get_data()
        all_groups_of_type = get_groups_of_types(
            all_items=Item.objects.filter().all(), answer=data.get("type"))
        keyboard_markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=2,
            
            keyboard=[
                [
                    KeyboardButton(text="⏪"),
                    KeyboardButton(text="Главное меню 🏠"),
                ],
            ]
        )
        for i in range(len(all_groups_of_type)):
            if i < 100:
                keyboard_markup.insert(all_groups_of_type[i])
        await state.reset_state(with_data=False)
        await message.answer(text="Назад", reply_markup=keyboard_markup)
        await MenuState.GROUP.set()
    elif message.text == "Главное меню 🏠":
        await state.reset_state(with_data=False)
        await message.answer(text="Вы в главном меню",reply_markup=menuMain)    
    else:
        item = get_item(
            all_items=Item.objects.filter().all(),
            item=message.text
        )

        all_groups_of_type = get_items_of_group(
            all_items=Item.objects.filter().all(), type=data.get("type"),  group=data.get("group"))
        keyboard_markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=2,
            keyboard=[
                [
                    KeyboardButton(text="⏪"),
                    KeyboardButton(text="Главное меню 🏠"),
                ],
            ]
        )

        for i in all_groups_of_type:
            keyboard_markup.insert(i)
        count = ""
        text_markup = f"""
{hbold(item.name)}

Остаток: {item.remind}
Цена: {item.price}
Кол-во: {count}
        

        """

        # await state.reset_state(with_data=False)
        markup = await calculate_inline(item_id=item.id, sample_quantity=count)
        await message.answer(text=text_markup, reply_markup=markup)



@dp.callback_query_handler(calculate_cd.filter(), state="*")
async def callback_calculator(query: types.CallbackQuery, callback_data: dict):
    item = Item.objects.filter(id=int(callback_data.get('item_id'))).first()
    action = callback_data.get("action")
    count = str(callback_data.get('sample_quantity'))
    if action == 'erase':
        count = str(count[:len(str(count))-1])
    elif action == 'order':
        user = User.objects.filter(user_id=query["from"]['id']).first()
        order_discover = Order.objects.filter(buyer=user.id).filter(success=False).first()
        text_markup = "Товар добавлен в корзину ✅"
        if order_discover:
            new_order_item = OrderItem(
                order=order_discover,
                user=user,
                product=item,
                amount=item.price,
                quantity=count)
            new_order_item.save()
            # order_discover.total = int(item.price * count)
            # order_discover.save()
            await query.answer(text=text_markup)
            return
        else:
            new_order = Order(
                buyer=user,
                total=item.price,
                # phone_number=user.phone_number,
                purchase_time=datetime.now(),
                success=False)
            new_order.save()

            new_order_item = OrderItem(
                order=new_order,
                user=user,
                product=item,
                amount=item.price,
                quantity=count)
            new_order_item.save()
            await query.answer(text=text_markup)
            return
    else:
        count = str(callback_data.get('sample_quantity')) + \
            str(callback_data.get('numeral'))

    text_markup = f"""
{hbold(item.name)}

Остаток: {item.remind}
Цена: {item.price}
Кол-во: {count}
        

    """
    markup = await calculate_inline(item_id=item.id, sample_quantity=count)
    await query.message.edit_text(text_markup, reply_markup=markup)


