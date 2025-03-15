from aiogram import Router, Bot, F, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.buttuns.inline import channels, menu, settings, anons, subscribe_btn, shop_btn
from models import BotUser, Channels
from models.users import AdminPanel

start_router = Router()

admin_1 = 5649321700
admin_2 = 1353080275


@start_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext, bot: Bot):
    user = await BotUser.get(message.from_user.id)
    from_user = message.from_user
    text = f'''
Здравствуйте 🙋 {from_user.first_name},

🤖 Бот может отправлять в канал различные объявления из игры Grand Mobile.
⚙ Пример: 🚗 Транспорт, 🏢 Бизнес, 🏠 Жильё и имущество, а также другие категории.

Поддерживайте нас! Скоро добавим новые функции: покупка, поиск игроков, премиум-объявления.

После завершения модераторы проверяют и публикуют ваше объявление в канал.
Если у вас есть ошибки или предложения, свяжитесь с: @SunnatiPy.
По вопросам рекламы: @SunnatiPy.
    '''
    if not user:
        try:
            await BotUser.create(id=from_user.id, first_name=from_user.first_name,
                                 last_name=from_user.last_name,
                                 username=from_user.username)
        except:
            await bot.send_message(5649321700, f'user: {from_user}')
        if from_user.id in [5649321700, ]:
            count: AdminPanel = await AdminPanel.get(1)
            if count == None:
                await AdminPanel.create(count_anons=0)
            await message.answer(text, reply_markup=menu(admin=True))
        else:
            await message.answer(text, reply_markup=menu())
    else:
        if from_user.id in [5649321700, ]:
            count: AdminPanel = await AdminPanel.get(1)
            if count == None:
                await AdminPanel.create(count_anons=0)
            await message.answer(text, parse_mode="HTML", reply_markup=menu(admin=True))
        else:
            await message.answer(text, reply_markup=menu())


@start_router.callback_query(F.data.startswith("menu_"))
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    if data == 'menu':
        await call.message.edit_text("Выберите", reply_markup=anons())
    elif data == 'admin':
        await call.message.edit_text("Выберите", reply_markup=settings())
    else:
        await call.message.answer("Главное меню", reply_markup=menu())


@start_router.callback_query(F.data.startswith("anons_"))
async def command_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split('_')[-1]
    if data == 'sale':
        await call.message.edit_text("Выберите что хотите продать", reply_markup=shop_btn())
    elif data == 'subscribe':
        await call.message.edit_text("Выберите заявления", reply_markup=subscribe_btn())
    elif data == 'back':
        try:
            await call.message.edit_text("Главное меню", reply_markup=menu())
        except:
            await call.message.answer("Главное меню", reply_markup=menu())


@start_router.callback_query(F.data.startswith('settings_'))
async def leagues_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = call.data.split('_')[-1]
    await call.answer()
    if data == 'static':
        users = await BotUser.count()
        channel = await Channels.count()
        count_anons: AdminPanel = await AdminPanel.get(1)
        await call.message.answer(
            html.bold(
                f'Admin\nUserlar soni: <b>{users},\nKanallar soni: {channel}</b>\n<b>Anons soni</b>: {count_anons.count_anons}'),
            parse_mode='HTML')
    elif data == 'subscribe':
        channels_ = await Channels.all()
        if channels_:
            try:
                await call.message.edit_text(text='Kanallar', reply_markup=await channels(channels_))
            except Exception as e:
                print(e)
                try:
                    await call.message.delete()
                except:
                    pass
                await call.message.answer(text='Kanallar', reply_markup=await channels(channels_))

        else:
            try:
                await call.message.edit_text(text='Kanallar', reply_markup=await channels(channels_))
            except:
                await call.message.answer(text='Kanallar', reply_markup=await channels(channels_))
    elif data == 'back':
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer(text=f'Assalomu aleykum Admin {call.from_user.first_name}',
                                  reply_markup=menu(admin=True))
