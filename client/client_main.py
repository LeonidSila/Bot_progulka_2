import logging
from aiogram import types, Dispatcher, F, Router
from create_bot import dp, bot, id_chat, id_admin_1, id_admin_2
from aiogram.filters import Command
from database import data_base as db
from keaboards import key
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class Wait(StatesGroup):
    name_item = State()
    rub_item = State()
    rub = State()
    admin = State()
    admin_2 = State()
    admin_3 = State()
    admin_4 = State()


router_client = Router()
logi_file = logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

@router_client.message(Command(commands=['start']))
async def start_help_command(message : types.Message):
    try:
        count_sum_rub_item = 0
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
        user_last_name = message.from_user.last_name
        print(message.text, message.from_user.id, message.from_user.first_name)
        await message.delete()
        db.cursor.execute('SELECT COUNT(*) FROM main WHERE id = ?', (user_id, ))
        db.conn.commit()
        user_count = db.cursor.fetchone()
        user_count = user_count[0]
        if user_count == 0:
            logging.info(f'Результат: {user_id} - занесен в базу данных')
            db.cursor.execute('INSERT INTO main (id, first_name, last_name) VALUES (?, ?, ?)', (user_id, user_first_name, user_last_name, ))
            db.conn.commit()
            
            
            db.cursor.execute('SELECT id, first_name, rupii, dolg_rupii FROM main')
            user_count_all_user = db.cursor.fetchall()
            db.conn.commit()
            db.cursor.execute('SELECT name, rub FROM all_in')
            user_count_item = db.cursor.fetchall()
            db.conn.commit()
            for i in range(len(user_count_item)):
                count_sum_rub_item =count_sum_rub_item+ int(user_count_item[i][1])
            sum_rub_del = count_sum_rub_item / len(user_count_all_user)
            for i in range(len(user_count_all_user)):
                db.cursor.execute('UPDATE main set dolg_rupii = ? where id = ?', (sum_rub_del, user_count_all_user[i][0], ))
                db.conn.commit()

            
        else: 
            await bot.send_message(chat_id=user_id, text=f"Ну что у нас там {user_first_name}?")
    except Exception as e:
        logging.error(f'Ошибка в обработке комады help, start: {str(e)}')
        
@router_client.message(Command(commands=['help']))
async def help_command(message : types.Message):
    try:
        count_sum_rub_item = 0
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
        user_last_name = message.from_user.last_name
        db.cursor.execute('SELECT id, first_name, rupii, dolg_rupii FROM main')
        user_count_all_user = db.cursor.fetchall()
        db.conn.commit()
        db.cursor.execute('SELECT name, rub FROM all_in')
        user_count_item = db.cursor.fetchall()
        db.conn.commit()
        for i in range(len(user_count_item)):
            count_sum_rub_item =count_sum_rub_item+ int(user_count_item[i][1])
        sum_rub_del = count_sum_rub_item / len(user_count_all_user)
        for i in range(len(user_count_all_user)):
            db.cursor.execute('UPDATE main set dolg_rupii = ? where id = ?', (sum_rub_del, user_count_all_user[i][0], ))
            db.conn.commit()

        if user_id != id_admin_1 and user_id != id_admin_2:
            print(message.text, message.from_user.id, message.from_user.first_name)
            await message.delete()
            db.cursor.execute('SELECT COUNT(*) FROM main WHERE id = ?', (user_id, ))
            db.conn.commit()
            user_count = db.cursor.fetchone()
            user_count = user_count[0]
            if user_count == 0:
                logging.info(f'Результат: {user_id} - занесен в базу данных')
                db.cursor.execute('INSERT INTO main (id, first_name, last_name) VALUES (?, ?, ?)', (user_id, user_first_name, user_last_name, ))
                db.conn.commit()
                db.cursor.execute('SELECT id, first_name, rupii, dolg_rupii FROM main')
                user_count_all_user = db.cursor.fetchall()
                db.conn.commit()
                db.cursor.execute('SELECT name, rub FROM all_in')
                user_count_item = db.cursor.fetchall()
                db.conn.commit()
                for i in range(len(user_count_item)):
                    count_sum_rub_item =count_sum_rub_item+ int(user_count_item[i][1])
                sum_rub_del = count_sum_rub_item / len(user_count_all_user)
                for i in range(len(user_count_all_user)):
                    db.cursor.execute('UPDATE main set dolg_rupii = ? where id = ?', (sum_rub_del, user_count_all_user[i][0], ))
                    db.conn.commit()

                await bot.send_message(chat_id=user_id, text=f"Вот возможные команды.\n/start - Начало, ничего такого тут нет\n/help - выдает возможные команды\n/show_me - показывает  сколько ты должен и сколько ты уже перевел {user_first_name}?")
            else: 
                await bot.send_message(chat_id=user_id, text=f"Вот возможные команды.\n/start - Начало, ничего такого тут нет\n/help - выдает возможные команды\n/show_me - показывает  сколько ты должен и сколько ты уже перевел {user_first_name}?")
        else:
            await bot.send_message(chat_id=user_id, text=f"Вот возможные команды.\n/start - Начало, ничего такого тут нет\n/help - выдает возможные команды\n/work - Дает возможность зайти и заполнить товар\n/show_me - показывает  сколько ты должен и сколько ты уже перевел\n/admin - входите в режим амина\n/update - Скидывает все значения до 0{user_first_name}?")

    except Exception as e:
        logging.error(f'Ошибка в обработке комады help, start: {str(e)}')

@router_client.message(Command(commands=['work']))
async def work_hard(message : types.Message):
    try:
        user_id = message.from_user.id
        await message.delete()
        print(message.text, message.from_user.id, message.from_user.first_name)
        if user_id != id_admin_1 and user_id != id_admin_2:
            await bot.send_message(chat_id=user_id, text="Нет доступа")
        else:
            await bot.send_message(chat_id=user_id, text="Добро пожаловать на работу", reply_markup=key.kb_vibor_work)

    except Exception as e:
        logging.error(f'Ошибка в обработке комады work: {str(e)}')

@router_client.message(F.text == 'Заполнить таблицу')
async def choose(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(message.text, message.from_user.id, message.from_user.first_name)
    await state.set_state(Wait.name_item)
    await bot.send_message(chat_id=user_id, text="Напишите наименование товара, или услуги", reply_markup=key.kb_vibor_work_1)

@router_client.message(Wait.name_item)
async def choose_name_item(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(message.text, message.from_user.id, message.from_user.first_name)
    await state.update_data(vibor_name_item=message.text)
    await state.set_state(Wait.rub_item)
    await bot.send_message(chat_id=user_id, text="А теперь напишите цену, этого товара или услуги.\nНаписать нужно только число без запятых",reply_markup=key.kb_vibor_work_1)

@router_client.message(Wait.rub_item)
async def choose_rub_item(message: types.Message, state: FSMContext):
    count_sum_rub_item = 0
    user_id = message.from_user.id
    print(message.text, message.from_user.id, message.from_user.first_name)
    await state.update_data(vibor_rub_item=message.text)
    data = await state.get_data()
    db.cursor.execute('INSERT INTO all_in (name, rub) VALUES (?, ?)', (data['vibor_name_item'], data['vibor_rub_item'], ))
    db.conn.commit()
    await bot.send_message(chat_id=user_id, text="Все, карточка заполнена",reply_markup=key.kb_vibor_work)
    await state.clear()
    
    
    db.cursor.execute('SELECT rupii FROM main WHERE id = ?', (user_id, ))
    user_r = db.cursor.fetchone()
    user_r = user_r[0]
    if user_r == None and str(user_r) == 'None' and user_r == 0 and str(user_r) == '0':
        sum_numirik = data['vibor_rub_item']
    else:
        sum_numirik = int(data['vibor_rub_item'])+int(user_r)
    db.conn.commit()
    db.cursor.execute('UPDATE main set rupii = ? where id = ?', (sum_numirik, user_id, ))
    db.conn.commit()
    
    
    
    db.cursor.execute('SELECT id, first_name, rupii, dolg_rupii FROM main')
    user_count_all_user = db.cursor.fetchall()
    db.conn.commit()
    db.cursor.execute('SELECT name, rub FROM all_in')
    user_count_item = db.cursor.fetchall()
    db.conn.commit()
    for i in range(len(user_count_item)):
        count_sum_rub_item =count_sum_rub_item+ int(user_count_item[i][1])
    sum_rub_del = count_sum_rub_item / len(user_count_all_user)
    for i in range(len(user_count_all_user)):
        db.cursor.execute('UPDATE main set dolg_rupii = ? where id = ?', (sum_rub_del, user_count_all_user[i][0], ))
        db.conn.commit()

        
        
        
    
    
    
    
    

@router_client.message(Wait.name_item, F.text == 'Устала/Выйти')
async def choose_name_item_not(message: types.Message, state: FSMContext):
    print(message.text, message.from_user.id, message.from_user.first_name)
    print(message.text, message.from_user.id, message.from_user.first_name)
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text="Все, пора отдыхать",reply_markup=types.ReplyKeyboardRemove())

@router_client.message(Wait.rub_item, F.text == 'Устала/Выйти')
async def choose_rub_item_not(message: types.Message, state: FSMContext):
    print(message.text, message.from_user.id, message.from_user.first_name)
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text="Все, пора отдыхать",reply_markup=types.ReplyKeyboardRemove())

@router_client.message(F.text == 'Отдыхать')
async def choose_not(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text="Ну, если нет желания, то и ненадо",reply_markup=types.ReplyKeyboardRemove())

@router_client.message(F.text == 'Карточка товара')
async def choose_all_item(message: types.Message, state: FSMContext):
    count = 0
    user_id = message.from_user.id
    print(message.text, message.from_user.id, message.from_user.first_name)
    db.cursor.execute('SELECT name, rub FROM all_in')
    db.conn.commit()
    user_count = db.cursor.fetchall()
    print(type(user_count))
    if user_count == None or user_count == []:
        await bot.send_message(chat_id=user_id, text='<b>Ничего нет</b>')
    else:
        await bot.send_message(chat_id=user_id, text="Вот\n", reply_markup=key.kb_vibor_work)
        for i in range(len(user_count)):
            await bot.send_message(chat_id = user_id, text=f'<i>Название</i> - <b>{user_count[i][0]}</b>\n<i>Цена</i> - <b>{user_count[i][1]}</b>')
            count += int(user_count[i][1])
    await bot.send_message(chat_id=user_id, text=f'<i>Обьщая цена</i> - <b>{count}</b>')

@router_client.message(F.text == 'Сколько скинули')
async def choose_all_item_rub(message: types.Message, state: FSMContext):
    count = 0
    user_id = message.from_user.id
    db.cursor.execute('SELECT first_name, last_name, rupii FROM main')
    db.conn.commit()
    user_count = db.cursor.fetchall()
    print(message.text, message.from_user.id, message.from_user.first_name)
    await bot.send_message(chat_id=user_id, text="Вот\n\n\n",reply_markup=key.kb_vibor_work)
    for i in range(len(user_count)):
        if user_count[i][1] == None and str(user_count[i][1]) == 'None':
            await bot.send_message(chat_id=user_id, text=f'<b>{user_count[i][0]}</b>, <i>Скиунл/а</i> - <b>{user_count[i][2]}</b>')
        else:
            await bot.send_message(chat_id=user_id, text=f'<b>{user_count[i][0]}</b>, <b>{user_count[i][1]}</b>, <i>Скиунл/а</i> - <b>{user_count[i][2]}</b>')
        count+= int(user_count[i][2])
    await bot.send_message(chat_id=user_id, text=f'<i>Всего скинулись</i> - <b>{count}</b>')
        
        
@router_client.message(Command(commands=['show_me']))
async def show_me_command(message : types.Message):
    try:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
        print(message.text, message.from_user.id, message.from_user.first_name)
        await message.delete()
        db.cursor.execute('SELECT first_name, last_name, rupii, dolg_rupii FROM main WHERE id = ?', (user_id, ))
        db.conn.commit()
        user_count = db.cursor.fetchone()
        name_1 = user_count[0]
        name_2 = user_count[1]
        rub = user_count[2]
        rub_dolg = user_count[3]
        await bot.send_message(chat_id=user_id, text=f'<b>{name_1}</b> - Всего вы перевели (<i>{rub}</i>)\nа должны (<i>{rub_dolg}</i>).')

    except Exception as e:
        logging.error(f'Ошибка в обработке комады help, start: {str(e)}')
    
@router_client.message(Command(commands=['admin']))
async def show_me_command(message : types.Message):
    try:
        user_id = message.from_user.id
        if user_id != id_admin_1 and user_id != id_admin_2:
            await bot.send_message(chat_id=user_id, text='Охолеро, доступ сюда у Вас нет')
        else:
            await bot.send_message(chat_id=user_id, text='Добро пожаловать!', reply_markup=key.kb_vibor_admin)
            await bot.send_message(chat_id=user_id, text='Должники - показывает, кто сколько скинул и сколько должны или не должны\nВкл/Выкл Подсчет - Включает работу подсчета, Для обновления\nВыйти - Пока')
    except Exception as e:
        logging.error(f'Ошибка в обработке комады help, start: {str(e)}')
    
@router_client.message(F.text == 'Должники')
async def show_me_command(message : types.Message):
    count_all_user = 0
    count_all_user_rub = 0
    count_all_user_rub_dolg = 0
    try:
        user_id = message.from_user.id
        if user_id != id_admin_1 and user_id != id_admin_2:
            bot.send_message(chat_id=user_id, text='Охолеро, доступ сюда у Вас нет')
        else:
            db.cursor.execute('SELECT first_name, rupii FROM main WHERE id = ?', (user_id, ))
            user_count_rub = db.cursor.fetchone()
            user_count_rub = user_count_rub[0]
            db.conn.commit()
            
            db.cursor.execute('SELECT id, first_name, rupii, dolg_rupii FROM main')
            user_count_all = db.cursor.fetchall()
            db.conn.commit()
            # for i in range(len(user_count_all)):
            #     if int(user_count_all[i][0]) == user_id:
            #         user_count_all.pop(i)
            #         break
            
            for i in range(len(user_count_all)):
                count_all_user = count_all_user + 1
                count_all_user_rub = count_all_user_rub + user_count_all[i][2]
                count_all_user_rub_dolg = count_all_user_rub_dolg + user_count_all[i][3]
                await bot.send_message(chat_id=user_id, text=f'Имя - {user_count_all[i][1]}\nСколько он/она перевел - {user_count_all[i][2]}\nСколько он/она должен/на - {user_count_all[i][3]}')
            
            await bot.send_message(chat_id=user_id, text=f'Всего людей - {count_all_user}\nВсего перевели - {count_all_user_rub}\nСумма долга = {count_all_user_rub_dolg}')
    
    except Exception as e:
        logging.error(f'Ошибка в обработке комады admin: {str(e)}')
        
@router_client.message(F.text == 'Выйти')
async def choose_not_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text="Ну, если нет желания, то и ненадо",reply_markup=types.ReplyKeyboardRemove())
    
    
@router_client.message(F.text == 'Данные/перевел')
async def choose_not_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id != id_admin_1 and user_id != id_admin_2:
        bot.send_message(chat_id=user_id, text='Охолеро, доступ сюда у Вас нет')
    else:
        db.cursor.execute('SELECT id, first_name, last_name FROM main')
        user_count_all = db.cursor.fetchall()
        db.conn.commit()
        for i in range(len(user_count_all)):
            await bot.send_message(chat_id=user_id, text=f'{user_count_all[i][1]} {user_count_all[i][2]} - id\n{user_count_all[i][0]}')
        
        await state.set_state(Wait.admin)
        await bot.send_message(chat_id=user_id, text='Правила простые, бот прислал id пользователей зарегестированных в базе данных. С вашей сороны нужно написать id пользователя который брислал бот, для понимания к какому человек привязано id справа есть Имя\nРезюмируя\n1)Пишите id из списка выше\n2)Пишите сумму, сколько перевел человек\n3)Идти отдыхать')
        await bot.send_message(chat_id=user_id, text='На первом этапе жду id')


@router_client.message(Wait.admin)
async def choose_rub_item(message: types.Message, state: FSMContext):
    count_1 = 0
    user_id = message.from_user.id
    message_id = int(message.text)
    db.cursor.execute('SELECT id first_name FROM main')
    user_count_all = db.cursor.fetchall()
    db.conn.commit()
    print(user_count_all)
    for i in range(len(user_count_all)):
        print(int(user_count_all[i][0]), message_id)
        if message_id == int(user_count_all[i][0]):
            count_1 = 1
            break
    if count_1 == 0:
        await bot.send_message(chat_id=user_id, text='Такого id нет, попробуйте заново')
        
    else:
        await state.update_data(vibor_user_id=message.text)
        await state.set_state(Wait.admin_2)
        await bot.send_message(chat_id=user_id, text='На этом этапе жду сумму перевода, сколько человек перевел')
        
@router_client.message(Wait.admin_2)
async def choose_rub_item_2(message: types.Message, state: FSMContext):
    count_sum_rub_item = 0
    user_id = message.from_user.id
    await state.update_data(vibor_user_rub=message.text)
    data = await state.get_data()
    db.cursor.execute('SELECT rupii FROM main WHERE id = ?', (data['vibor_user_id'], ))
    user_count_rub = db.cursor.fetchone()
    user_count_rub = user_count_rub[0]
    user_count_rub = float(data['vibor_user_rub']) + user_count_rub
    db.cursor.execute('UPDATE main set rupii = ? where id = ?', (user_count_rub, data['vibor_user_id'], ))
    db.conn.commit()
    await bot.send_message(chat_id=user_id, text="Данные отправил",reply_markup=key.kb_vibor_admin)
    await state.clear()
    


@router_client.message(Command(commands=['update']))
async def work_hard(message : types.Message):
    try:
        user_id = message.from_user.id
        await message.delete()
        print(message.text, message.from_user.id, message.from_user.first_name)
        if user_id != id_admin_1 and user_id != id_admin_2:
            await bot.send_message(chat_id=user_id, text="Нет доступа")
        else:
            db.cursor.execute('UPDATE main set dolg_rupii = 0, rupii = 0')
            db.conn.commit()
    except Exception as e:
        logging.error(f'Ошибка в обработке комады work: {str(e)}')
        
        

@router_client.message(F.text == 'Данные/должен')
async def choose_not_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id != id_admin_1 and user_id != id_admin_2:
        bot.send_message(chat_id=user_id, text='Охолеро, доступ сюда у Вас нет')
    else:
        db.cursor.execute('SELECT id, first_name, last_name FROM main')
        user_count_all = db.cursor.fetchall()
        db.conn.commit()
        for i in range(len(user_count_all)):
            await bot.send_message(chat_id=user_id, text=f'{user_count_all[i][1]} {user_count_all[i][2]} - id\n{user_count_all[i][0]}')
        
        await state.set_state(Wait.admin_3)
        await bot.send_message(chat_id=user_id, text='Правила простые, бот прислал id пользователей зарегестированных в базе данных. С вашей сороны нужно написать id пользователя который брислал бот, для понимания к какому человек привязано id справа есть Имя\nРезюмируя\n1)Пишите id из списка выше\n2)Пишите сумму, сколько перевел человек\n3)Идти отдыхать')
        await bot.send_message(chat_id=user_id, text='На первом этапе жду id')


@router_client.message(Wait.admin_3)
async def choose_rub_item(message: types.Message, state: FSMContext):
    count_1 = 0
    user_id = message.from_user.id
    message_id = int(message.text)
    db.cursor.execute('SELECT id first_name FROM main')
    user_count_all = db.cursor.fetchall()
    db.conn.commit()
    print(user_count_all)
    for i in range(len(user_count_all)):
        print(int(user_count_all[i][0]), message_id)
        if message_id == int(user_count_all[i][0]):
            count_1 = 1
            break
    if count_1 == 0:
        await bot.send_message(chat_id=user_id, text='Такого id нет, попробуйте заново')
        
    else:
        await state.update_data(vibor_user_id=message.text)
        await state.set_state(Wait.admin_4)
        await bot.send_message(chat_id=user_id, text='На этом этапе жду сумму долга, сколько человек должен')
        
@router_client.message(Wait.admin_4)
async def choose_rub_item_2(message: types.Message, state: FSMContext):
    count_sum_rub_item = 0
    user_id = message.from_user.id
    await state.update_data(vibor_user_rub=message.text)
    data = await state.get_data()
    db.cursor.execute('SELECT dolg_rupii FROM main WHERE id = ?', (data['vibor_user_id'], ))
    user_count_rub = db.cursor.fetchone()
    user_count_rub = user_count_rub[0]
    user_count_rub = float(data['vibor_user_rub']) + user_count_rub
    db.cursor.execute('UPDATE main set dolg_rupii = ? where id = ?', (user_count_rub, data['vibor_user_id'], ))
    db.conn.commit()
    await bot.send_message(chat_id=user_id, text="Данные отправил",reply_markup=key.kb_vibor_admin)
    await state.clear()