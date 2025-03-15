
def detail_business(from_user, data):
    username = f"🏌 Username: @{from_user.username}" if from_user.username else ''
    return data.get('photo'), f"""
🛍<b>Продажа</b> {data.get('shop_name')}

💾 <b>Сервер</b>: {data.get('server')}
📛 <b>Названия</b>: {data.get('name')}
🙂 <b>Игрок</b>: {data.get('owner_name')} 
🧭 <b>Навигатор</b>: {data.get("navigator")}
☎ <b>Номер связи</b>: {data.get('tg_phone')}
📱 <b>Игровой номер</b>: {data.get('game_phone')}
💰 <b>Цена</b>: {data.get('price')}
🔄 <b>Тип торга</b>: {data.get('torg')}
{username}

⚠ <b><span class="tg-spoiler">*Если обманули, администратор не несет ответственность!*</span> </b>
"""


def detail_shar(from_user, data):
    username = f"\n🏌<b> Username: @{from_user.username}</b>" if from_user.username else ''
    skin_d = f"\n🔢<b> id: {data.get('id')}</b>" if data.get('id') else ''
    details = data.get('selected_parts', {})
    count_owner = f"<b>Количество Владелец</b>: {data.get('count_owner')}\n" if data.get('count_owner') else ''

    # text_details = "\n".join(
    #     [f"🔧 {key}: {level_colors.get(int(value), '⚫')} {value}" for key, value in details.items() if key != 'confirm']
    # ) if details else "❌ Улучшений нет"

    def format_circles(level):
        max_level = 5
        return " ".join(["🟡" if i < level else "⚪" for i in range(max_level)])

    if details:
        detail = "⚙ <b>Улучшение</b>\n"


        text_detail = "\n".join(
            [f"🔧 {key}: {format_circles(int(value))}" if int(value) > 0 else f"🔧 {key}: ❌ Нет улучшения"
             for key, value in details.items() if key != 'confirm']
        )
    else:
        detail = ''
        text_detail = ''
    gos_price = f"<b> Гос.цена</b>: {data.get('gos_price', 0)}" if data.get('gos_price') else ''

    return data.get('photo'), f"""
<b>🛍 Продажа </b>{data.get('shop_name')}

💾<b> Сервер</b>: {data.get('server')}
📛<b> Названия</b>: {data.get('name')}{skin_d}
🙂<b> Игрок</b>: {data.get('owner_name')}
☎<b> Номер связи</b>: {data.get('tg_phone')}
📱<b> Игровой номер</b>: {data.get('game_phone')}
💰<b> Цена</b>: {data.get('price')}
🔄<b> Тип торга</b>: {data.get('torg')}{username}
{gos_price}
{count_owner}

{detail + text_detail}

⚠ <b><span class="tg-spoiler">*Если обманули, администратор не несет ответственность!*</span> </b>
"""


def detail_home(from_user, data):
    username = f"🏌 Username: @{from_user.username}" if from_user.username else ''
    return data.get('photo'), f"""
🛍<b> Продажа </b> {data.get('shop_name')}

💾<b> Сервер</b>: {data.get('server')}
🚩<b> Местоположение</b>: {data.get('location')}
🔢<b> Номер жилё</b>: {data.get('number')}
🏢<b> Тип жилё</b>: {data.get('tip')}
🔨<b> Ремонт</b>: {data.get('remont')}
📛<b> Названия: {data.get('name')}</b>
🙂<b> Игрок: {data.get('owner_name')} </b>
☎<b> Номер связи: {data.get('tg_phone')}</b>
📱<b> Игровой номер: {data.get('game_phone')}</b>
💰<b> Цена: {data.get('price')}</b>
🔄 <b>Тип торга: {data.get('torg')}</b>
<b>{username}</b>

⚠ <b><span class="tg-spoiler">*Если обманули, администратор не несет ответственность!*</span> </b>
"""
