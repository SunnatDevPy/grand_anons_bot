import re

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from bot.buttuns.inline import contact, server_btn, confirm_inl, menu, torg_btn, confirm_text, channel_url
from bot.state import ShopStateHome
from bot.utils import detail_home
from models.users import AdminPanel

shop_home = Router()


def check_phone(phone):
    validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
    return re.match(validate_phone_number_pattern, phone)


@shop_home.message(ShopStateHome.photo)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    res = await state.get_data()
    shop_name = res.get('shop_name')
    if msg.photo:
        await state.update_data(photo=msg.photo[-1].file_id)
        await state.set_state(ShopStateHome.location)
        await msg.answer(f"Выберите место нахождение {shop_name}")
    else:
        await msg.answer(f"Не отправили фото ⚠")


@shop_home.callback_query(ShopStateHome.location)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    res = await state.get_data()
    shop_name = res.get('shop_name')
    await state.update_data(location=data)
    await state.set_state(ShopStateHome.tip)
    await call.message.answer(f"Выберите тип {shop_name}")


@shop_home.callback_query(ShopStateHome.tip)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    res = await state.get_data()
    data = call.data.split('_')[-1]
    shop_name = res.get('shop_name')
    await state.update_data(tip=data)
    await state.set_state(ShopStateHome.number)
    await call.message.answer(f"Введите номер {shop_name}")


@shop_home.message(ShopStateHome.number)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    await state.update_data(number=msg.text)
    await state.set_state(ShopStateHome.remont)
    await msg.answer(f"Введите ремонт жилё")


@shop_home.message(ShopStateHome.remont)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    await state.update_data(remont=msg.text)
    await state.set_state(ShopStateHome.owner_name)
    await msg.answer(f"Введите игровой ник пример: Например_Напремиев")


@shop_home.message(ShopStateHome.owner_name)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    await state.update_data(owner_name=msg.text)
    await state.set_state(ShopStateHome.tg_phone)
    await msg.answer(f"Введите телефон номера или нажмите на кнопку контакт", reply_markup=contact())


@shop_home.message(ShopStateHome.tg_phone)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    if msg.contact or check_phone(msg.text):
        if msg.contact:
            await state.update_data(tg_phone=msg.contact.phone_number)
        else:
            await state.update_data(tg_phone=msg.text)
        await state.set_state(ShopStateHome.game_phone)
        await msg.answer(f"Введите игровой телефон номера, внимание: (символ длина от 3 до 6)",
                         reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer(f"❌ Неправильно формат номера, повторно введите ⚠")


@shop_home.message(ShopStateHome.game_phone)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    if 3 <= len(msg.text) <= 6:
        await state.update_data(game_phone=msg.text)
        await state.set_state(ShopStateHome.price)
        await msg.answer(f"Введите цена бизнеса с разделением пример: (1.000.000, 1_000_000)")
    else:
        await msg.answer(f"❌ Неправильно формат игровой номера, повторно введите внимание: (символ длина от 3 до 6) ⚠")


@shop_home.message(ShopStateHome.price)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    price_pattern = r"^\d{1,3}([._]\d{3})*$"
    if re.fullmatch(price_pattern, msg.text):
        await state.update_data(price=msg.text)
        await state.set_state(ShopStateHome.torg)
        await msg.answer(f"Выберите тип торга", reply_markup=torg_btn())
    else:
        await msg.answer(f"❌ Неправильный формат цены! Введите в таком формате: 1.000.000 или 1_000_000")


@shop_home.callback_query(ShopStateHome.torg)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    await state.update_data(torg=data)
    await call.message.delete()
    await state.set_state(ShopStateHome.server)
    await call.message.answer(f"Выберите сервер", reply_markup=server_btn())


@shop_home.callback_query(ShopStateHome.server)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    await call.message.delete()
    await state.update_data(server=data)
    res = await state.get_data()
    detail = detail_home(call.from_user, res)
    print(detail)
    await state.set_state(ShopStateHome.confirm)
    await call.message.answer_photo(detail[0], detail[-1], reply_markup=confirm_inl(), parse_mode="HTML")


@shop_home.callback_query(ShopStateHome.confirm)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[0]
    await call.message.delete()
    if data == 'confirm':
        count: AdminPanel = await AdminPanel.get(1)
        await AdminPanel.update(1, count_anons=count.count_anons + 1)
        res = await state.get_data()
        detail = detail_home(call.from_user, res)
        await bot.send_photo(5649321700, detail[0], caption=detail[-1], parse_mode="HTML")
        await call.message.answer("Объявление отправлено к модераторам, скоро оно появится в канале. Спасибо ✅",reply_markup=channel_url())
        await call.message.answer("Главное меню", reply_markup=menu())
    else:
        await call.message.answer("Отменен ❌")
        await call.message.answer("Главное меню", reply_markup=menu())
    await state.clear()


@shop_home.callback_query(F.data.startswith('channel_'))
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')
    if data == 'confirm':
        count: AdminPanel = await AdminPanel.get(1)
        await AdminPanel.update(1, count_anons=count.count_anons + 1)

        # Получаем фото и текст из сообщения
        photo = call.message.photo[-1].file_id if call.message.photo else None
        caption = call.message.caption

        if photo:
            await bot.send_photo(chat_id=-1002229527376, photo=photo, caption=caption, parse_mode="HTML",
                                 reply_markup=None)
        else:
            await bot.send_message(chat_id=-1002229527376, text=caption, parse_mode="HTML", reply_markup=None)

        await call.message.answer("Объявление отправлено к модераторам, скоро оно появится в канале. Спасибо ✅")
    else:
        await call.message.answer("Отменено ❌")

    await call.message.answer("Главное меню", reply_markup=menu())
    await state.clear()
