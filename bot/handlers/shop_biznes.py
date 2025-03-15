import re

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from bot.buttuns.inline import business_btn, anons, contact, server_btn, confirm_inl, menu, torg_btn, confirm_text, \
    channel_url
from bot.state import ShopState, ShopStateHome
from bot.utils import detail_business
from models.users import AdminPanel

shop_business_router = Router()


def check_phone(phone):
    validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
    return re.match(validate_phone_number_pattern, phone)


class ShopRouterBiznes(StatesGroup):
    name = State()
    photo = State()
    owner_name = State()
    navigator = State()
    tg_phone = State()
    game_phone = State()
    price = State()
    torg = State()
    server = State()
    confirm = State()


@shop_business_router.callback_query(F.data.startswith("shop_"))
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    await state.update_data(shop_name=data)
    if data == 'Бизнес':
        await state.set_state(ShopRouterBiznes.name)
        await call.message.edit_text("Выберите бизнес", reply_markup=business_btn())
    elif data == "Номера авто/игровой":
        await state.set_state(ShopState.name)
        await call.message.answer(f"Вводите названия {data} привем (авто - F111AAA|01, тел - )")
    elif data == ["Квартира", "Апартамент", "Дом"]:
        await state.set_state(ShopStateHome.photo)
        await call.message.answer(f"Отправите одно фото {data} статистику !")
    elif data == "back":
        await state.clear()
        try:
            await call.message.edit_text("Выберите", reply_markup=anons())
        except:
            await call.message.answer("Выберите", reply_markup=anons())
    else:
        await call.message.delete()
        await state.set_state(ShopState.name)
        await call.message.answer(f"Вводите названия {data}")



@shop_business_router.callback_query(ShopRouterBiznes.name)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    await state.update_data(name=data)
    if data == "back":
        await state.clear()
        try:
            await call.message.edit_text("Выберите", reply_markup=anons())
        except:
            await call.message.answer("Выберите", reply_markup=anons())
    else:
        await call.message.delete()
        await state.set_state(ShopRouterBiznes.photo)
        await call.message.answer(f"Отправите одно фото бизнеса {data} прибил (финка)!")


@shop_business_router.message(ShopRouterBiznes.photo)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    if msg.photo:
        await state.update_data(photo=msg.photo[-1].file_id)
        await state.set_state(ShopRouterBiznes.owner_name)
        await msg.answer(f"Введите игровой ник пример: Например_Напремиев")
    else:
        await msg.answer(f"Не отправили фото ⚠")


@shop_business_router.message(ShopRouterBiznes.owner_name)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    await state.update_data(owner_name=msg.text)
    await state.set_state(ShopRouterBiznes.navigator)
    await msg.answer(f"Введите навигатор бизнеса: (12>15, 12>40)")


@shop_business_router.message(ShopRouterBiznes.navigator)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    pattern = r"^\d+>\d+$"
    if re.fullmatch(pattern, msg.text.strip()):
        await state.update_data(navigator=msg.text)
        await state.set_state(ShopRouterBiznes.tg_phone)
        await msg.answer(f"Введите телефон номера или нажмите на кнопку контакт", reply_markup=contact())
    else:
        await msg.answer(f"❌ Повторно введите нет символ '>' или номера не правильно ⚠")


@shop_business_router.message(ShopRouterBiznes.tg_phone)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    if msg.contact or check_phone(msg.text):
        if msg.contact:
            await state.update_data(tg_phone=msg.contact.phone_number)
        else:
            await state.update_data(tg_phone=msg.text)
        await state.set_state(ShopRouterBiznes.game_phone)
        await msg.answer(f"Введите игровой телефон номера, внимание: (символ длина от 3 до 6)",
                         reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer(f"❌ Неправильно формат номера, повторно введите ⚠")


@shop_business_router.message(ShopRouterBiznes.game_phone)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    if 3 <= len(msg.text) <= 6:
        await state.update_data(game_phone=msg.text)
        await state.set_state(ShopRouterBiznes.price)
        await msg.answer(f"Введите цена бизнеса с разделением пример: (1.000.000, 1_000_000)")
    else:
        await msg.answer(f"❌ Неправильно формат игровой номера, повторно введите внимание: (символ длина от 3 до 6) ⚠")


@shop_business_router.message(ShopRouterBiznes.price)
async def command_start(msg: Message, state: FSMContext, bot: Bot):
    price_pattern = r"^\d{1,3}([._]\d{3})*$"
    if re.fullmatch(price_pattern, msg.text):
        await state.update_data(price=msg.text)
        await state.set_state(ShopRouterBiznes.torg)
        await msg.answer(f"Выберите тип торга", reply_markup=torg_btn())
    else:
        await msg.answer(f"❌ Неправильный формат цены! Введите в таком формате: 1.000.000 или 1_000_000")


@shop_business_router.callback_query(ShopRouterBiznes.torg)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    await state.update_data(torg=data)
    await call.message.delete()
    await state.set_state(ShopRouterBiznes.server)
    await call.message.answer(f"Выберите сервер", reply_markup=server_btn())


@shop_business_router.callback_query(ShopRouterBiznes.server)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    await call.message.delete()
    await state.update_data(server=data)
    res = await state.get_data()
    detail = detail_business(call.from_user, res)
    print(detail)
    await state.set_state(ShopRouterBiznes.confirm)
    await call.message.answer_photo(detail[0], detail[-1], reply_markup=confirm_inl(), parse_mode="HTML")


@shop_business_router.callback_query(ShopRouterBiznes.confirm)
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[0]
    await call.message.delete()
    if data == 'confirm':
        count: AdminPanel = await AdminPanel.get(1)
        await AdminPanel.update(1, count_anons=count.count_anons + 1)
        res = await state.get_data()
        detail = detail_business(call.from_user, res)
        await bot.send_photo(5649321700, detail[0], caption=detail[-1], parse_mode="HTML")
        await call.message.answer("Объявление отправлено к модераторам, скоро оно появится в канале. Спасибо ✅",reply_markup=channel_url())
        await call.message.answer("Главное меню", reply_markup=menu())
    else:
        await call.message.answer("Отменен ❌")
        await call.message.answer("Главное меню", reply_markup=menu())
    await state.clear()
