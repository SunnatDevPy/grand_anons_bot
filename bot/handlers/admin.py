# from aiogram import Bot, F, Router, html
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.types import CallbackQuery, Message
#
# from bot.buttuns.inline import send_text, menu, channels, settings, zayafka_change
# from models import BotUser, Channels
# from models.users import TextZayafka
#
# admin_router = Router()
#
# import re
#
#
# class ZayafkaText(StatesGroup):
#     photo = State()
#     text = State()
#
#
# def Find(string):
#     regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
#     url = re.findall(regex, string)
#     return [x[0] for x in url]
#
#
# @admin_router.callback_query(F.data.startswith('settings_stock'))
# async def leagues_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
#     await call.message.edit_text("Settings", reply_markup=settings())
#
#
#
# @admin_router.message(ZayafkaText.photo)
# async def leagues_handler(message: Message, bot: Bot, state: FSMContext):
#     if message.photo:
#         await state.update_data(photo=message.photo[-1].file_id)
#         await state.set_state(ZayafkaText.text)
#         await message.answer('Text kiriting')
#     else:
#         await message.answer("Rasim jo'nating")
#
#
# @admin_router.message(ZayafkaText.text)
# async def leagues_handler(message: Message, bot: Bot, state: FSMContext):
#     data = await state.get_data()
#     zayafka_text = await TextZayafka.get(1)
#
#     # try:
#     if zayafka_text:
#         await TextZayafka.update(1, photo=data.get('photo'), name=message.text)
#         await message.answer_photo(photo=data.get('photo'), caption=message.text,
#                                    reply_markup=zayafka_change(zayafka_text.status))
#         await message.answer("Muvoffaqyatli o'zgardi!✅")
#     else:
#         zayafka_text: TextZayafka = await TextZayafka.create(photo=data.get('photo'), name=message.text, status=True)
#         await message.answer_photo(photo=zayafka_text.photo, caption=zayafka_text.name,
#                                    reply_markup=zayafka_change(zayafka_text.status))
#         await message.answer("Muvoffaqyatli saqlandi!✅")
#
#     # except:
#     #     await message.answer("Saqlashda xatolik!❌")
#     #     await message.answer("Settings", reply_markup=settings())
#
#
# @admin_router.callback_query(F.data.startswith('zayafka_'))
# async def leagues_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
#     data = call.data.split('_')[-1]
#     print(data)
#     if data == 'change':
#         await call.message.delete()
#         await state.set_state(ZayafkaText.photo)
#         await call.message.answer("Rasim kiriting")
#     elif data == 'status':
#         zayafka_text: TextZayafka = await TextZayafka.get(1)
#         if zayafka_text.status:
#             status = False
#         else:
#             status = True
#         await TextZayafka.update(1, status=status)
#         try:
#             await call.message.edit_reply_markup(inline_message_id=call.inline_message_id,
#                                                  reply_markup=zayafka_change(status))
#         except:
#             await call.message.answer_photo(photo=zayafka_text.photo, caption=zayafka_text.name,
#                                             reply_markup=zayafka_change(status))
#     else:
#         await call.message.delete()
#         await call.message.answer("Settings", reply_markup=settings())
