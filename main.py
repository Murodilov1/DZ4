from conf import token
from aiogram     import Dispatcher, types, Bot, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, callback_query, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio, logging, os
import random
from button import keyboard_confirm, keyboard_confirm1

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

number = random.randint(2000, 5000)
user_text = ""
number2 = random.randint(1000,5000)
class UserReg(StatesGroup):
    name = State()
    adress = State()
    dop = State()
    stuff = State()
    zaz = State()
    check = State()
User_data = {}
buttom1 = InlineKeyboardButton(
    text = "Еда",
    callback_data='buttom1_press'
)
buttom2 = InlineKeyboardButton(
    text="Запчасти",
    callback_data='buttom2_press'
)
buttom3 = InlineKeyboardButton(
    text="Мебель",
    callback_data='buttom3_press'
)
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[buttom1],
                     [buttom2],
                     [buttom3]]
                     
)

@dp.message(Command("status"))
async def check(message:types.Message):
    await message.answer(f'Общий статус:\n Имя Заказчика:{User_data['name']}\n Адрес доставки:{User_data["adress"]}\n Название товара:{User_data['stuff']}\n Предпочтения: {User_data["dop"]}\n Уникальный код клиента:{number}')

@dp.message(Command("check"))
async def cccc(message:types.Message):
    await message.answer(f"Ваш товар:{User_data['stuff']} в процессе упокования, ускорить?", reply_markup=keyboard_confirm())
@dp.message(F.text == 'Да')
async def da(message:types.Message):
    await message.answer(f"Ваш заказ: {User_data['stuff']} в процессе доставки, \n Мы можем ускорить еще.", reply_markup=keyboard_confirm1())
@dp.message(F.text == "Нет")
async def za(message:types.Message):
    await message.answer(f'Ваш заказ {User_data['stuff']} доставлен по адресу: {User_data["adress"]} \n С вас {number2} долларов из-за ускорения:)', reply_markup=keyboard_confirm1())
@dp.message(F.text == "Нет")
async def sa(message:types.Message):
    await message.answer("Не нет а да. Вы обязаны оплатить.")

@dp.message(Command("start"))
async def start(message:types.Message):
    await message.answer(
        text="Выбери то что хочешь",
        reply_markup=keyboard
    )
@dp.callback_query(F.data.in_(['buttom1_press',
                               'buttom2_press',
                               'buttom3_press']))
async def call(callback: types.CallbackQuery):
    if callback.data == "Еда" or "Мебель" or "Запчасти":
        await callback.message.answer('Напишите "принять" без скобок .')

@dp.message(F.text == "принять")
async def start(message:types.Message, state:FSMContext):
    await message.answer("Вот теперь напишите что хотите")
    await state.set_state(UserReg.stuff)

@dp.message(UserReg.stuff)
async def stuff(message:types.Message, state:FSMContext):
    User_data['stuff'] = message.text
    await message.reply("Напишите свое имя")
    await state.set_state(UserReg.name)

@dp.message(UserReg.name)
async def stuff(message:types.Message, state:FSMContext):
    User_data['name'] = message.text
    await message.reply("Адрес проживания?")
    await state.set_state(UserReg.adress)

@dp.message(UserReg.adress)
async def stuff(message:types.Message, state:FSMContext):
    User_data['adress'] = message.text
    await message.reply("Напишите какого цвето будет ваш товар")
    await state.set_state(UserReg.dop)
@dp.message(UserReg.dop)
async def stuff(message:types.Message, state:FSMContext):
    User_data['dop'] = message.text
    await message.answer(f""" Хорошо,ваш заказ: {User_data['stuff']} потвержден.\n Ваш уникальный номер:{number} \n напишите команду /status что бы узнать данные. \n И /check для проверки местонахождения""")
    await state.clear











async def main():
    await dp.start_polling(bot)
asyncio.run(main())