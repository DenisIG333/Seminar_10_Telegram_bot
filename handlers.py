import time
from create import dp
from aiogram import Bot, Dispatcher, executor, types
import random
from datetime import datetime

total = random.randint(57, 130)
count_candies = random.randint(15, 25)
isBot = False
isGamer = False
scoreGamer = 0
scoreBot = 0
user = []
games_count = 0




@dp.message_handler(commands=['start', "старт"])
async def mes_hi(message: types.Message):
    global isGamer
    global isBot
    global count_candies
    global user

    await message.answer(f'Привет, <b>{message.from_user.first_name}</b> мы будем играть в конфетки', parse_mode=types.ParseMode.HTML)
    time.sleep(1)
    await message.answer(f'<b>Правила игры:</b> На столе лежит <b>{total} конфет.</b>'
                         'Играют два игрока делая ход друг после друга. Первый ход определяется жеребьёвкой.'
                         f'За один ход можно забрать <i><b>не более чем {count_candies} конфет</b></i>. Все конфеты оппонента достаются сделавшему последний ход. '
                         f'Количество конфет на столе и сколько за один ход можно забрать определяется <b> в случайном порядке </b>'
                         , parse_mode=types.ParseMode.HTML)

    await message.answer(f'Погнали играть!')
    time.sleep(1)
    rnd = random.randint(1, 2)
    if rnd == 1:
        await message.answer(f'По результатам жеребьевки первый ход делаешь ты, введи число от <b>1 до {count_candies} </b> ', parse_mode=types.ParseMode.HTML)
        isGamer = True
    if rnd == 2:
        await message.answer(f'По результатам жеребьевки первый ход делаю я. <b> Для начала игры введи любой текст </b> ' , parse_mode=types.ParseMode.HTML)
        isBot = True

    user.append(datetime.now())
    user.append(message.from_user.full_name)
    user.append(message.from_user.id)
    user.append(message.from_user.username)
    user_log(user)


def user_log(log: list):
    log = list(map(str, log))
    with open("text.txt", "a", encoding="UTF-8") as data:
        data.write(" | ".join(log) + "\n")


@dp.message_handler() #lambda msg: msg.text.isdigit()
async def mes_start(message: types.Message):
    global isBot
    global isGamer
    global total
    global scoreBot
    global scoreGamer
    global count_candies
    global games_count

    while True:
        if total > 0:
            if message.text.isdigit() and isGamer == True:
                    print("hello")
                    if int(message.text) > 0 and int(message.text) <= count_candies:
                        total -= int(message.text)
                        isBot = True
                        isGamer = False
                    else:
                        return await message.answer(f'введи количество конфет, <b>не более {count_candies}</b>', parse_mode=types.ParseMode.HTML)

        if total <= 0:
            total = random.randint(57, 130)
            scoreGamer += 1
            await message.answer(f'ты победил!')
            await message.answer(f'счет побед: бот - {scoreBot}: ты - {scoreGamer}')
            isGamer = True
            isBot = False
            count_candies = random.randint(15, 25)
            await message.answer(
                f'На столе новое количество конфет - <b>{total} </b> . За один ход можно забрать <i><b>не более чем {count_candies} конфет</b></i>.',
                parse_mode=types.ParseMode.HTML)
            if games_count > 0: #если игрок играет не первый раз, то перезаписываем количество побед
                index_value = len(user) - 1
                user[index_value] = scoreGamer
            else: #если играет первый раз, то добавляем в user победу
                user.append(scoreGamer)

            user_log(user)
            games_count += 1
            await message.answer(f'Если хочешь начать игру заново, введи количество конфет <b>от 1 до {count_candies} </b>', parse_mode=types.ParseMode.HTML)




        if isBot == True:
            await message.answer(f' На столе <b>{total} конфет </b>', parse_mode=types.ParseMode.HTML)
            print(message)
            time.sleep(1)

            await message.answer(f' Следующий ход мой')
            time.sleep(1)
            await message.answer(f' Думаю......')
            time.sleep(2)
            casting_lots = random.randint(1, count_candies)
            if total > count_candies:
                total -= casting_lots
                await message.answer(f'возьму <b>{casting_lots} конфет </b>', parse_mode=types.ParseMode.HTML)
                time.sleep(0.5)
                await message.answer(f'На столе <b>{total} конфет</b>', parse_mode=types.ParseMode.HTML)
                time.sleep(0.5)
                await message.answer(f'{message.from_user.first_name}, следующий ход твой, введи число от <b>1 до {count_candies} </b>', parse_mode=types.ParseMode.HTML)
            else:
                await message.answer(f' А нечего думать :-) забираю всё :-)')
                total -= total
                scoreBot += 1
                await message.answer(f'я победил!')
                await message.answer(f'счет побед: <b>бот - {scoreBot}: ты - {scoreGamer} </b> ', parse_mode=types.ParseMode.HTML)
                total = random.randint(57, 130)
                count_candies = random.randint(15, 25)
                await message.answer(
                    f'На столе новое количество конфет - <b>{total} </b> . За один ход можно забрать <i><b>не более чем {count_candies} конфет</b></i>.',
                    parse_mode=types.ParseMode.HTML)
                await message.answer(f'Если хочешь начать игру заново, введи количество конфет <b>от 1 до {count_candies} </b>', parse_mode=types.ParseMode.HTML)


            isGamer = True
            isBot = False


        if isGamer == True:
            print("gamer")
            return await message.answer(f'<b>введи число</b>', parse_mode=types.ParseMode.HTML)


