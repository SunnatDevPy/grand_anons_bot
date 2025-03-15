from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def menu(admin=False):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text="✉Объявление✉", callback_data="menu_menu")])
    if admin:
        ikb.add(*[InlineKeyboardButton(text="⚙️Settings⚙️", callback_data='menu_admin')])
    ikb.adjust(1, 2)
    return ikb.as_markup()


def settings():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text="Userlar soni", callback_data='settings_static'),
              InlineKeyboardButton(text="Barcha Userlari uchun xabar", callback_data='send_user'),
              InlineKeyboardButton(text="Barcha kanallar uchun xabar", callback_data='send_channel'),
              InlineKeyboardButton(text="⬅️Ortga", callback_data='settings_back')])
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()


def anons():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        # InlineKeyboardButton(text="🛒Куплю🛒", callback_data='anons_shop'),
        InlineKeyboardButton(text="💲Продажа💲", callback_data='anons_sale'),
        # InlineKeyboardButton(text="👪Набор игроков👪", callback_data='anons_subscribe'),
        InlineKeyboardButton(text="🔙Назад🔙", callback_data='anons_back')])
    ikb.adjust(2, 1, 1)
    return ikb.as_markup()


def business_btn():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text="💲Постамат💲", callback_data='business_Постамат'),
        InlineKeyboardButton(text="🏪Магазин🏪", callback_data='business_Магазин'),
        InlineKeyboardButton(text="⛽АЗС⛽", callback_data='business_АЗС'),
        InlineKeyboardButton(text="🅿Стоянка🅿", callback_data='business_Стоянка'),
        InlineKeyboardButton(text="⛏Каменоломня⛏", callback_data='business_Каменоломня'),
        InlineKeyboardButton(text="👕Одежда👕", callback_data='business_Одежда'),
        InlineKeyboardButton(text="⚔Оружейник⚔", callback_data='business_Оружейник'),
        InlineKeyboardButton(text="🏡Нотариус🏡", callback_data='business_Нотариус'),
        InlineKeyboardButton(text="🔙Назад🔙", callback_data='business_back')])
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()


locations = ['Эдово', "Богатырева", "Батырево",
             "Арзамас", "Элитный Поселок", "Гарель",
             "Лыткарино", "Корякино",
             "Бусаево", "Южный"]

tips = ['Эконом', "Стандарт", "Средний", "Апартаменты", "Элитный"]


def location_btn():
    ikb = InlineKeyboardBuilder()

    for part in locations:
        ikb.add(InlineKeyboardButton(text=part, callback_data=f"locations_{part}"))

    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def tip_home_btn():
    ikb = InlineKeyboardBuilder()

    for part in tips:
        ikb.add(InlineKeyboardButton(text=part, callback_data=f"tips_{part}"))

    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def shop_btn():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text="🚙Автомобиль🚗", callback_data='shop_Автомобиль'),
        InlineKeyboardButton(text="🚁Вертолет🚁", callback_data='shop_Вертолет'),
        InlineKeyboardButton(text="🎈Воздушный Шар🎈", callback_data='shop_Воздушный Шар'),
        InlineKeyboardButton(text="💰Бизнес💰", callback_data='shop_Бизнес'),
        InlineKeyboardButton(text="👕Скин👕", callback_data='shop_Скин'),
        InlineKeyboardButton(text="🕶Аксессуар🕶", callback_data='shop_Аксессуар'),
        InlineKeyboardButton(text="👪Семя👪", callback_data='shop_Семя'),
        InlineKeyboardButton(text="Номера авто/игровой", callback_data='shop_Номера авто/игровой'),
        InlineKeyboardButton(text="🏠Квартира🏠", callback_data='shop_Квартира'),
        InlineKeyboardButton(text="🛏Апартамент🛏", callback_data='shop_Апартамент'),
        InlineKeyboardButton(text="🏡Дом🏡", callback_data='shop_Дом'),
        InlineKeyboardButton(text="🔙Назад🔙", callback_data='shop_back')])
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()


def channel_url():
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='Перейти в канал', url='https://t.me/grand_mobile_anons'))
    return ikb.as_markup()


def server_btn():
    ikb = InlineKeyboardBuilder()
    i = 1
    while i < 37:
        ikb.add(*[InlineKeyboardButton(text=f"#{i}", callback_data=f"server_{i}")])
        i += 1
    ikb.adjust(3, repeat=True)
    return ikb.as_markup()


def subscribe_btn():
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='👪Семя👪', callback_data="subscribe_Семя"))
    ikb.row(InlineKeyboardButton(text='🏢Фракция⚔', callback_data="subscribe_Фракция"))
    ikb.row(InlineKeyboardButton(text="🔙Назад🔙", callback_data='subscribe_back'))
    return ikb.as_markup()


def torg_btn():
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='Обмен', callback_data="subscribe_Обмен"))
    ikb.row(InlineKeyboardButton(text='Торг', callback_data="subscribe_Торг"))
    ikb.row(InlineKeyboardButton(text="Обмен/Торг", callback_data='subscribe_Обмен/Торг'))
    ikb.row(InlineKeyboardButton(text="💰Бабки💰", callback_data='subscribe_💰Бабки💰'))
    ikb.adjust(2, 2)
    return ikb.as_markup()


def contact():
    ikb = ReplyKeyboardBuilder()
    ikb.row(KeyboardButton(text='☎Отправить Контакт☎', request_contact=True))
    return ikb.as_markup(resize_keyboard=True)


def link_from_channel(links):
    ikb = InlineKeyboardBuilder()
    for btn in links:
        ikb.add(InlineKeyboardButton(text=btn[0], url=btn[-1]))
    ikb.adjust(1)
    return ikb.as_markup()


def ft_detail(selected_parts):
    ikb = InlineKeyboardBuilder()

    for part in ["Трансмиссия", "Турбонаддув", "Двигатель", "Тормоза", "Подвеска", "Шины", "Чип"]:
        ikb.add(InlineKeyboardButton(text=part, callback_data=f"ft_{part}"))
        for lvl in range(1, 6):
            button_text = "✅" if selected_parts.get(part) == str(lvl) else "🔴"
            ikb.add(InlineKeyboardButton(text=button_text, callback_data=f"ft_{part}_{lvl}"))

    ikb.row(InlineKeyboardButton(text="✅Завершить✅", callback_data='ft_confirm_1'))
    ikb.adjust(6, repeat=True)
    return ikb.as_markup()


def send_text_type(text):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text="Tayyor text", callback_data=f'types_forward_{text}'),
              InlineKeyboardButton(text="Yaratish", callback_data=f'types_create_{text}'),
              InlineKeyboardButton(text="⬅️Ortga", callback_data='types_back')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def confirm_text():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text="✅Jo'natish✅", callback_data='channel_confirm'),
              InlineKeyboardButton(text="❌O'chirish❌", callback_data='channel_stop')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def confirm_inl():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='✅Подтверждение✅', callback_data=f'confirm_network'),
              InlineKeyboardButton(text="❌Остановит❌", callback_data=f'cancel_network')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


async def channels(channels):
    ikb = InlineKeyboardBuilder()
    for i in channels:
        ikb.add(*[
            InlineKeyboardButton(text=i.name, callback_data=f'channels_info_{i.id}_{i.chat_id}')
        ])
    ikb.row(InlineKeyboardButton(text="Kanalga qo'shish", url=f"https://t.me/Stockfootball_bot?startchannel=true"))
    ikb.row(InlineKeyboardButton(text="⬅️Ortga️", callback_data="channels_back"))
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()
