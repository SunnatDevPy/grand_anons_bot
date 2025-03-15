from aiogram.fsm.state import StatesGroup, State


class ShopRouterBiznes(StatesGroup):
    name = State()
    finka_photo = State()
    owner_name = State()
    navigator = State()
    tg_phone = State()
    game_phone = State()
    price = State()
    ft_3 = State()
    server = State()


class ShopState(StatesGroup):
    name = State()
    id = State()
    photo = State()
    owner_name = State()
    tg_phone = State()
    game_phone = State()
    gos_price = State()
    ft_3 = State()
    count_owner = State()
    price = State()
    torg = State()
    server = State()
    confirm = State()


class ShopStateHome(StatesGroup):
    photo = State()
    location = State()
    number = State()
    tip = State()
    remont = State()
    owner_name = State()
    tg_phone = State()
    game_phone = State()
    price = State()
    torg = State()
    server = State()
    confirm = State()
