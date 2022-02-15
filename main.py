from os import stat
import telebot
import settings
from telebot import types
from SQLighter import delete_user, get_user_state, check_user_exists, set_user_state, init_db
bot = telebot.TeleBot(settings.TOKEN)

# bot.remove_webhook()


@bot.message_handler(commands=['start'])
def start(message):
    '''обработчик команды старт'''
    bot.send_message(message.chat.id, "Вітаю, {0}!".format(
        message.from_user.first_name))
    kb = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='ДЦВ', callback_data='dcv')
    kb.add(itembtn1)
    # itembtn2 = types.InlineKeyboardButton(text='ОСЦПВ', callback_data='oscpv')
    # itembtn3 = types.InlineKeyboardButton(
    #     text='НВ на транспорті', callback_data='nvnt')
    # kb.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(
        message.from_user.id, "Цей бот призначений для швидкого розрахунку страхової премії. Для початку роботи натисніть на кнопку.", reply_markup=kb)
    
    init_db()
    check_user_exists(user_id=message.from_user.id)
    

    log(message)


@bot.callback_query_handler(func=lambda call: 'dcv' in call.data)
def dcv_handler(call):
    '''обработчик нажатия на кнопку ДЦВ'''
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Зона 1', callback_data='zone1')
    btn2 = types.InlineKeyboardButton(text='Зона 2', callback_data='zone2')
    btn3 = types.InlineKeyboardButton(text='Зона 3', callback_data='zone3')
    kb.add(btn1, btn2, btn3)
    bot.send_message(
        call.from_user.id, "<b>УВАГА! За ДЦВ маршрутні автобуси та ТЗ, що використовуються в якості ТАКСІ, на страхування НЕ ПРИЙМАЮТЬСЯ.</b>", parse_mode='HTML')
    bot.send_message(
        call.from_user.id, "*Виберіть зону:* \nКиїв, Київська обл\. \- *1* \nХарків, Одеса, Дніпро, Львів, Запоріжжя, Кривий Ріг, ТЗ з іноземною реєстрацією \- *2* \nІнші населені пункти \- *3*",
        reply_markup=kb, parse_mode='MarkdownV2'
    )


@bot.callback_query_handler(func=lambda call: ('zone1' in call.data) or ('zone2' in call.data) or ('zone3' in call.data))
def dcv_zone_handler(call):
    '''обрабатывает выбор зоны для ДЦВ'''
    
    if 'zone1' in call.data:
        set_user_state(user_id=call.from_user.id,col='dcv_zone',state='zone1')
        set_user_state(user_id=call.from_user.id,col='zone_selected',state='Київ, Київська обл')
    elif 'zone2' in call.data:
        set_user_state(user_id=call.from_user.id,col='dcv_zone',state='zone2')
        set_user_state(user_id=call.from_user.id,col='zone_selected',state='Харків, Одеса, Дніпро, Львів, Запоріжжя, Кривий Ріг, ТЗ з іноземною реєстрацією')
    else:
        set_user_state(user_id=call.from_user.id,col='dcv_zone',state='zone3')
        set_user_state(user_id=call.from_user.id,col='zone_selected',state='Інші населені пункти')
    print("Вибрано зону: {}".format(get_user_state(user_id=call.from_user.id,col=3)))
    bot.send_message(call.from_user.id, "Вибрано зону: {}".format(get_user_state(user_id=call.from_user.id,col=3)))
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        text='A1, A2, F, B1, B2, B3, E', callback_data='type1')
    btn2 = types.InlineKeyboardButton(
        text='B4, C1, D1, C2, D2', callback_data='type2')
    kb.add(btn1, btn2)
    bot.send_message(
        call.from_user.id, "*Виберіть тип ТЗ*", reply_markup=kb, parse_mode='MarkdownV2'
    )


@bot.callback_query_handler(func=lambda call: ('type1' in call.data) or ('type2' in call.data))
def dcv_autotype_handler(call):
    '''обрабатывает ввод типа ТС для ДЦВ'''
    
    if 'type1' in call.data:
        set_user_state(user_id=call.from_user.id,col='dcv_auto_type',state='type1')
        set_user_state(user_id=call.from_user.id,col='type_selected',state='A1, A2, F, B1, B2, B3, E')
    else:
        set_user_state(user_id=call.from_user.id,col='dcv_auto_type',state='type2')
        set_user_state(user_id=call.from_user.id,col='type_selected',state='B4, C1, D1, C2, D2')
    print("Вибрано тип авто {}".format(get_user_state(user_id=call.from_user.id,col=5)))
    bot.send_message(call.from_user.id, "Вибрано зону: {} та тип авто {}".format(
        get_user_state(user_id=call.from_user.id,col=3), get_user_state(user_id=call.from_user.id,col=5)))
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='50 000', callback_data='50000')
    btn3 = types.InlineKeyboardButton(text='100 000', callback_data='100000')
    btn4 = types.InlineKeyboardButton(text='200 000', callback_data='200000')
    btn5 = types.InlineKeyboardButton(text='300 000', callback_data='300000')
    btn6 = types.InlineKeyboardButton(text='400 000', callback_data='400000')
    btn7 = types.InlineKeyboardButton(text='500 000', callback_data='500000')
    kb.add(btn1, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(call.from_user.id, "*Виберіть страхову суму*",
                     reply_markup=kb, parse_mode='MarkdownV2')


@bot.callback_query_handler(func=lambda call: ('50000' in call.data) or ('100000' in call.data) or ('200000' in call.data) or ('300000' in call.data) or ('400000' in call.data) or ('500000' in call.data))
def dcv_suminsured_handler(call):
    '''обрабатывает ввод страховой суммы для ДЦВ'''
    
    if '500000' in call.data:
        set_user_state(user_id=call.from_user.id,col='dcv_suminsured',state='500000')
    elif '100000' in call.data:
        set_user_state(user_id=call.from_user.id,col='dcv_suminsured',state='100000')
    elif '200000' in call.data:
        set_user_state(user_id=call.from_user.id,col='dcv_suminsured',state='200000')
    elif '300000' in call.data:
        set_user_state(user_id=call.from_user.id,col='dcv_suminsured',state='300000')
    elif '400000' in call.data:
        set_user_state(user_id=call.from_user.id,col='dcv_suminsured',state='400000')
    elif '50000' in call.data:
        set_user_state(user_id=call.from_user.id,col='dcv_suminsured',state='50000')
    print("Вибрано страхову суму {}".format(get_user_state(user_id=call.from_user.id,col=6)))
    bot.send_message(call.from_user.id,
                     "Вибрано страхову суму {}".format(get_user_state(user_id=call.from_user.id,col=6)))

    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        text='Так, все вірно', callback_data='yesDCV')
    btn2 = types.InlineKeyboardButton(text='Почати заново', callback_data='noDCV')
    kb.add(btn1, btn2)

    bot.send_message(call.from_user.id, "Вибрано зону: {},\n тип авто: {}\n та страхову суму: {}".format(
        get_user_state(user_id=call.from_user.id,col=3), 
        get_user_state(user_id=call.from_user.id,col=5), 
        get_user_state(user_id=call.from_user.id,col=6)
        ), 
        reply_markup=kb, parse_mode='MarkdownV2')


def get_price_and_tariff_for(user_id: int):
    import json
    with open('DCV.json', encoding='utf-8') as f:
        data = json.load(f)
    zone = str(get_user_state(user_id=user_id,col=2))
    type = str(get_user_state(user_id=user_id,col=4))
    sum_insured = str(get_user_state(user_id=user_id,col=6))
    
    if zone == 'zone1':
        if type == 'type1':
            if sum_insured == '50000':
                print(str(data['zone1']['type1']['50000']['KV'][0]) +
                      ' ' + str(data['zone1']['type1']['50000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type1']['50000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type1']['50000']['KV'][1])
            elif sum_insured == '100000':
                print(str(data['zone1']['type1']['100000']['KV'][0]) +
                      ' ' + str(data['zone1']['type1']['100000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type1']['100000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type1']['100000']['KV'][1])
            elif sum_insured == '200000':
                print(str(data['zone1']['type1']['200000']['KV'][0]) +
                      ' ' + str(data['zone1']['type1']['200000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type1']['200000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type1']['200000']['KV'][1])
            elif sum_insured == '300000':
                print(str(data['zone1']['type1']['300000']['KV'][0]) +
                      ' ' + str(data['zone1']['type1']['300000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type1']['300000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type1']['300000']['KV'][1])
            elif sum_insured == '400000':
                print(str(data['zone1']['type1']['400000']['KV'][0]) +
                      ' ' + str(data['zone1']['type1']['400000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type1']['400000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type1']['400000']['KV'][1])
            elif sum_insured == '500000':
                print(str(data['zone1']['type1']['500000']['KV'][0]) +
                      ' ' + str(data['zone1']['type1']['500000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type1']['500000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type1']['500000']['KV'][1])
        elif type == 'type2':
            if sum_insured == '50000':
                print(str(data['zone1']['type2']['50000']['KV'][0]) +
                      ' ' + str(data['zone1']['type2']['50000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type2']['50000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type2']['50000']['KV'][1])
            elif sum_insured == '100000':
                print(str(data['zone1']['type2']['100000']['KV'][0]) +
                      ' ' + str(data['zone1']['type2']['100000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type2']['100000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type2']['100000']['KV'][1])
            elif sum_insured == '200000':
                print(str(data['zone1']['type2']['200000']['KV'][0]) +
                      ' ' + str(data['zone1']['type2']['200000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type2']['200000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type2']['200000']['KV'][1])
            elif sum_insured == '300000':
                print(str(data['zone1']['type2']['300000']['KV'][0]) +
                      ' ' + str(data['zone1']['type2']['300000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type2']['300000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type2']['300000']['KV'][1])
            elif sum_insured == '400000':
                print(str(data['zone1']['type2']['400000']['KV'][0]) +
                      ' ' + str(data['zone1']['type2']['400000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type2']['400000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type2']['400000']['KV'][1])
            elif sum_insured == '500000':
                print(str(data['zone1']['type2']['500000']['KV'][0]) +
                      ' ' + str(data['zone1']['type2']['500000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone1']['type2']['500000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone1']['type2']['500000']['KV'][1])
    elif zone == 'zone2':
        if type == 'type1':
            if sum_insured == '50000':
                print(str(data['zone2']['type1']['50000']['KV'][0]) +
                      ' ' + str(data['zone2']['type1']['50000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type1']['50000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type1']['50000']['KV'][1])
            elif sum_insured == '100000':
                print(str(data['zone2']['type1']['100000']['KV'][0]) +
                      ' ' + str(data['zone2']['type1']['100000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type1']['100000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type1']['100000']['KV'][1])
            elif sum_insured == '200000':
                print(str(data['zone2']['type1']['200000']['KV'][0]) +
                      ' ' + str(data['zone2']['type1']['200000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type1']['200000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type1']['200000']['KV'][1])
            elif sum_insured == '300000':
                print(str(data['zone2']['type1']['300000']['KV'][0]) +
                      ' ' + str(data['zone2']['type1']['300000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type1']['300000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type1']['300000']['KV'][1])
            elif sum_insured == '400000':
                print(str(data['zone2']['type1']['400000']['KV'][0]) +
                      ' ' + str(data['zone2']['type1']['400000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type1']['400000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type1']['400000']['KV'][1])
            elif sum_insured == '500000':
                print(str(data['zone2']['type1']['500000']['KV'][0]) +
                      ' ' + str(data['zone2']['type1']['500000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type1']['500000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type1']['500000']['KV'][1])
        elif type == 'type2':
            if sum_insured == '50000':
                print(str(data['zone2']['type2']['50000']['KV'][0]) +
                      ' ' + str(data['zone2']['type2']['50000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type2']['50000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type2']['50000']['KV'][1])
            elif sum_insured == '100000':
                print(str(data['zone2']['type2']['100000']['KV'][0]) +
                      ' ' + str(data['zone2']['type2']['100000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type2']['100000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type2']['100000']['KV'][1])
            elif sum_insured == '200000':
                print(str(data['zone2']['type2']['200000']['KV'][0]) +
                      ' ' + str(data['zone2']['type2']['200000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type2']['200000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type2']['200000']['KV'][1])
            elif sum_insured == '300000':
                print(str(data['zone2']['type2']['300000']['KV'][0]) +
                      ' ' + str(data['zone2']['type2']['300000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type2']['300000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type2']['300000']['KV'][1])
            elif sum_insured == '400000':
                print(str(data['zone2']['type2']['400000']['KV'][0]) +
                      ' ' + str(data['zone2']['type2']['400000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type2']['400000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type2']['400000']['KV'][1])
            elif sum_insured == '500000':
                print(str(data['zone2']['type2']['500000']['KV'][0]) +
                      ' ' + str(data['zone2']['type2']['500000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone2']['type2']['500000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone2']['type2']['500000']['KV'][1])
    elif zone == 'zone3':
        if type == 'type1':
            if sum_insured == '50000':
                print(str(data['zone3']['type1']['50000']['KV'][0]) +
                      ' ' + str(data['zone3']['type1']['50000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type1']['50000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type1']['50000']['KV'][1])
            elif sum_insured == '100000':
                print(str(data['zone3']['type1']['100000']['KV'][0]) +
                      ' ' + str(data['zone3']['type1']['100000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type1']['100000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type1']['100000']['KV'][1])
            elif sum_insured == '200000':
                print(str(data['zone3']['type1']['200000']['KV'][0]) +
                      ' ' + str(data['zone3']['type1']['200000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type1']['200000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type1']['200000']['KV'][1])
            elif sum_insured == '300000':
                print(str(data['zone3']['type1']['300000']['KV'][0]) +
                      ' ' + str(data['zone3']['type1']['300000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type1']['300000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type1']['300000']['KV'][1])
            elif sum_insured == '400000':
                print(str(data['zone3']['type1']['400000']['KV'][0]) +
                      ' ' + str(data['zone3']['type1']['400000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type1']['400000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type1']['400000']['KV'][1])
            elif sum_insured == '500000':
                print(str(data['zone3']['type1']['500000']['KV'][0]) +
                      ' ' + str(data['zone3']['type1']['500000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type1']['500000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type1']['500000']['KV'][1])
        elif type == 'type2':
            if sum_insured == '50000':
                print(str(data['zone3']['type2']['50000']['KV'][0]) +
                      ' ' + str(data['zone3']['type2']['50000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type2']['50000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type2']['50000']['KV'][1])
            elif sum_insured == '100000':
                print(str(data['zone3']['type2']['100000']['KV'][0]) +
                      ' ' + str(data['zone3']['type2']['100000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type2']['100000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type2']['100000']['KV'][1])
            elif sum_insured == '200000':
                print(str(data['zone3']['type2']['200000']['KV'][0]) +
                      ' ' + str(data['zone3']['type2']['200000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type2']['200000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type2']['200000']['KV'][1])
            elif sum_insured == '300000':
                print(str(data['zone3']['type2']['300000']['KV'][0]) +
                      ' ' + str(data['zone3']['type2']['300000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type2']['300000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type2']['300000']['KV'][1])
            elif sum_insured == '400000':
                print(str(data['zone3']['type2']['400000']['KV'][0]) +
                      ' ' + str(data['zone3']['type2']['400000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type2']['400000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type2']['400000']['KV'][1])
            elif sum_insured == '500000':
                print(str(data['zone3']['type2']['500000']['KV'][0]) +
                      ' ' + str(data['zone3']['type2']['500000']['KV'][1]))
                return 'Тариф та вартість поліса\n для КВ 45% - ' + str(data['zone3']['type2']['500000']['KV'][0]) + '\n для КВ 50% - ' + str(data['zone3']['type2']['500000']['KV'][1])
    

@bot.callback_query_handler(func=lambda call: ('yesDCV' in call.data))
def price_and_tariff_handler(call):
    '''выдает стоимость и КВ по введенным ранее данным и выводит кнопку нового расчета'''
      
    kb = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='Новий розрахунок ДЦВ', callback_data='dcv')
    # itembtn2 = types.InlineKeyboardButton(text='ОСЦПВ', callback_data='oscpv')
    # itembtn3 = types.InlineKeyboardButton(
    #     text='НВ на транспорті', callback_data='nvnt')
    kb.add(itembtn1)

    bot.send_message(call.from_user.id, get_price_and_tariff_for(user_id=call.from_user.id), reply_markup=kb)
    
    delete_user(user_id=call.from_user.id)

@bot.callback_query_handler(func=lambda call: ('noDCV' in call.data))
def getback_to_start_handler(call):
    '''удаляет статусы для данного userID и возвращает к команде /start'''

    delete_user(user_id=call.from_user.id)
    print("Розрахунок розпочато заново.")

    kb = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='ДЦВ', callback_data='dcv')
    # itembtn2 = types.InlineKeyboardButton(text='ОСЦПВ', callback_data='oscpv')
    # itembtn3 = types.InlineKeyboardButton(
    #     text='НВ на транспорті', callback_data='nvnt')
    kb.add(itembtn1)
    bot.send_message(
        call.from_user.id, "Цей бот призначений для швидкого розрахунку страхової премії. Для початку роботи натисніть на кнопку.", reply_markup=kb)
    init_db()
    check_user_exists(user_id=call.from_user.id)
    

def log(message):
    print("\n ------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \nТекст = {3}".format(message.from_user.first_name,
                                                                  message.from_user.last_name,
                                                                  str(message.from_user.id),
                                                                  message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
    
