import re

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from bot.buttuns.inline import torg_btn, server_btn, confirm_inl, contact, menu, ft_detail, confirm_text, channel_url
from bot.state import ShopState
from bot.utils import detail_shar
from models.users import AdminPanel

shop_router = Router()

all_parts = ["Трансмиссия", "Турбонаддув", "Двигатель", "Тормоза", "Подвеска", "Шины", "Чип"]


def check_phone(phone):
    validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
    return re.match(validate_phone_number_pattern, phone)


@shop_router.message(ShopState.name)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    res = await state.get_data()
    shop_name = res.get('shop_name')
    await state.update_data(name=msg.text)
    if shop_name == 'Скин':
        await state.set_state(ShopState.id)
        await msg.answer(f"Введите айди скина!")
    elif shop_name == 'Семя':
        await state.set_state(ShopState.photo)
        await msg.answer(f"Отправите одно фото {shop_name} статистику!")
    else:
        await state.set_state(ShopState.photo)
        await msg.answer(f"Отправите одно фото {shop_name}!")


@shop_router.message(ShopState.id)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    res = await state.get_data()
    shop_name = res.get('shop_name')
    await state.update_data(id=msg.text)
    await state.set_state(ShopState.photo)
    await msg.answer(f"Отправите одно фото {shop_name}!")


@shop_router.message(ShopState.photo)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    if msg.photo:
        await state.update_data(photo=msg.photo[-1].file_id)
        await state.set_state(ShopState.owner_name)
        await msg.answer(f"Введите игровой ник пример: Например_Напремиев")
    else:
        await msg.answer(f"Не отправили фото ⚠")


@shop_router.message(ShopState.owner_name)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    await state.update_data(owner_name=msg.text)
    await state.set_state(ShopState.tg_phone)
    await msg.answer(f"Введите телефон номера или нажмите на кнопку контакт", reply_markup=contact())


@shop_router.message(ShopState.tg_phone)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    if msg.contact or check_phone(msg.text):
        if msg.contact:
            await state.update_data(tg_phone=msg.contact.phone_number)
        else:
            await state.update_data(tg_phone=msg.text)
        await state.set_state(ShopState.game_phone)
        await msg.answer(f"Введите игровой телефон номера, внимание: (символ длина от 3 до 6)",
                         reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer(f"❌ Неправильно формат номера, повторно введите ⚠")


@shop_router.message(ShopState.game_phone)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    res = await state.get_data()
    shop_name = res.get('shop_name')
    if 3 <= len(msg.text) <= 6:
        await state.update_data(game_phone=msg.text)
        if shop_name in ["Автомобиль", "Вертолет", "Мотоцикл"]:
            await state.set_state(ShopState.gos_price)
            await msg.answer(f"Введите гос.цена {shop_name} с разделением пример: (1.000.000, 1_000_000)")
        else:
            await state.set_state(ShopState.price)
            await msg.answer(f"Введите цена {shop_name} с разделением пример: (1.000.000, 1_000_000)")
    else:
        await msg.answer(f"❌ Неправильно формат игровой номера, повторно введите внимание: (символ длина от 3 до 6) ⚠")


@shop_router.message(ShopState.gos_price)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    res = await state.get_data()
    shop_name = res.get('shop_name')
    selected_parts = res.get("selected_parts", {})
    price_pattern = r"^\d{1,3}([._]\d{3})*$"
    if re.fullmatch(price_pattern, msg.text):
        await state.update_data(gos_price=msg.text)
        if shop_name in ["Вертолет", "Мотоцикл"]:
            await state.set_state(ShopState.count_owner)
            await msg.answer(f"Введите число водителя в формате целое число ⚠")
        else:
            await state.set_state(ShopState.ft_3)
            await msg.answer(
                f"Выберите все улучшения {shop_name}: {res.get('name')}, нет улучшения или выбрали нажмите кнопку <b>'Завершить'</b>",
                reply_markup=ft_detail(selected_parts), parse_mode="HTML")
    else:
        await msg.answer(f"❌ Неправильный формат гос цены! Введите в таком формате: 1.000.000 или 1_000_000")


@shop_router.callback_query(ShopState.ft_3)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    _, detail, level = call.data.split("_")
    user_data = await state.get_data()
    shop_name = user_data.get('shop_name')
    selected_parts = user_data.get("selected_parts", {})
    if selected_parts.get(detail) == level:
        selected_parts.pop(detail)
    else:
        selected_parts[detail] = level
        await state.update_data(selected_parts=selected_parts)

    if detail == 'confirm':
        final_selection = {part: selected_parts.get(part, "0") for part in all_parts}
        await state.update_data(selected_parts=final_selection)

        await state.set_state(ShopState.count_owner)
        await call.message.answer(f"Введите число водителя в формате целое число ⚠")
    else:
        try:
            await call.message.edit_text(
                f"Выберите все улучшения {shop_name}: {user_data.get('name')}, нет улучшения или выбрали нажмите кнопку <b>'Завершить'</b>",
                reply_markup=ft_detail(selected_parts), parse_mode="HTML")
        except:
            await call.message.answer(
                f"Выберите все улучшения {shop_name}: {user_data.get('name')}, нет улучшения или выбрали нажмите кнопку <b>'Завершить'</b>",
                reply_markup=ft_detail(selected_parts), parse_mode="HTML")


@shop_router.message(ShopState.count_owner)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    shop_name = user_data.get('shop_name')
    if msg.text.isdigit():
        await state.update_data(count_owner=msg.text)
        await state.set_state(ShopState.price)
        await msg.answer(f"Введите цена {shop_name} с разделением пример: (1.000.000, 1_000_000)")
    else:
        await msg.answer(f"❌ Неправильный формат число водителя в формате целое число ⚠")


@shop_router.message(ShopState.price)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    price_pattern = r"^\d{1,3}([._]\d{3})*$"
    if re.fullmatch(price_pattern, msg.text):
        await state.update_data(price=msg.text)
        await state.set_state(ShopState.torg)
        await msg.answer(f"Выберите тип торга", reply_markup=torg_btn())
    else:
        await msg.answer(f"❌ Неправильный формат цены! Введите в таком формате: 1.000.000 или 1_000_000")


@shop_router.callback_query(ShopState.torg)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    await state.update_data(torg=data)
    await call.message.delete()
    await state.set_state(ShopState.server)
    await call.message.answer(f"Выберите сервер", reply_markup=server_btn())


@shop_router.callback_query(ShopState.server)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    await call.message.delete()
    await state.update_data(server=data)
    res = await state.get_data()
    detail = detail_shar(call.from_user, res)
    await state.set_state(ShopState.confirm)
    await call.message.answer_photo(detail[0], detail[-1], reply_markup=confirm_inl(), parse_mode='HTML')


@shop_router.callback_query(ShopState.confirm)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[0]
    await call.message.delete()
    if data == 'confirm':
        res = await state.get_data()
        count: AdminPanel = await AdminPanel.get(1)
        await AdminPanel.update(1, count_anons=count.count_anons + 1)
        detail = detail_shar(call.from_user, res)
        await bot.send_photo(5649321700, detail[0], caption=detail[-1], parse_mode="HTML")
        await call.message.answer("Объявление отправлено к модераторам, скоро оно появится в канале. Спасибо ✅",
                                  reply_markup=channel_url())
        await call.message.answer("Главное меню", reply_markup=menu())
    else:
        await call.message.answer("Отменен ❌")
        await call.message.answer("Главное меню", reply_markup=menu())
    await state.clear()
