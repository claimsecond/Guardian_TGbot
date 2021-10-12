import telebot
from telebot import types
bot = telebot.TeleBot('1850015418:AAEt9BE1gVcAdGhfyElKl2GRtN8Qt7i9Mws')
# bot.remove_webhook()

dcv_zone = 0
dcv_auto_type = 0
dcv_suminsured = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Вітаю, {0}!".format(
        message.from_user.first_name))
    kb = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='ДЦВ',callback_data='dcv')
    itembtn2 = types.InlineKeyboardButton(text='ОСЦПВ', callback_data='oscpv')
    itembtn3 = types.InlineKeyboardButton(text='НВ на транспорті', callback_data='nvnt')
    kb.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(
        message.from_user.id, "Цей бот призначений для швидкого розрахунку страхової премії. Для початку роботи натисніть на кнопку.", reply_markup=kb)
    log(message)


@bot.callback_query_handler(func=lambda call:'dcv' in call.data)
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
    global dcv_zone
    if 'zone1' in call.data:
        dcv_zone = 'zone1'
    elif 'zone2' in call.data:
        dcv_zone = 'zone2'
    else:
        dcv_zone = 'zone3'
    print("Вибрано зону: {}".format(dcv_zone))
    bot.send_message(call.from_user.id, "Вибрано зону: {}".format(dcv_zone))
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
    global dcv_auto_type
    if 'type1' in call.data:
        dcv_auto_type = 'type1'
    else:
        dcv_auto_type = 'type2'
    print("Вибрано тип авто {}".format(dcv_auto_type))
    bot.send_message(call.from_user.id, "Вибрано зону: {} та тип авто {}".format(dcv_zone, dcv_auto_type))
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='50 000', callback_data='50000')
    btn3 = types.InlineKeyboardButton(text='100 000', callback_data='100000')
    btn4 = types.InlineKeyboardButton(text='200 000', callback_data='200000')
    btn5 = types.InlineKeyboardButton(text='300 000', callback_data='300000')
    btn6 = types.InlineKeyboardButton(text='400 000', callback_data='400000')
    btn7 = types.InlineKeyboardButton(text='500 000', callback_data='500000')
    kb.add(btn1, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(call.from_user.id, "*Виберіть страхову суму*", reply_markup=kb, parse_mode='MarkdownV2')


@bot.callback_query_handler(func=lambda call:('50000' in call.data) or ('100000' in call.data) or ('200000' in call.data) or ('300000' in call.data) or ('400000' in call.data) or ('500000' in call.data))
def dcv_suminsured_handler(call):
    '''обрабатывает ввод страховой суммы для ДЦВ'''
    global dcv_suminsured
    if '50000' in call.data:
        dcv_suminsured = '50000'
    elif '100000' in call.data:
        dcv_suminsured = '100000'
    elif '200000' in call.data:
        dcv_suminsured = '200000'
    elif '300000' in call.data: 
        dcv_suminsured = '300000'
    elif '400000' in call.data:
        dcv_suminsured = '400000'
    elif '500000' in call.data:
        dcv_suminsured = '500000'

def get_price_and_tariff(zone=dcv_zone, type=dcv_auto_type, sum_insured=dcv_suminsured):
    import json
    with open('DCV.json') as f:
        data = json.load(f)
    if zone == 'zone1':
        if type == 'type1':
            if sum_insured == '50000':
                return data['zone1']['type1']['50000']['KV'][0]
            elif sum_insured == '100000':
                pass
            elif sum_insured == '200000':
                pass
            elif sum_insured == '300000':
                pass
            elif sum_insured == '400000':
                pass
            elif sum_insured == '500000':
                pass
        elif type == 'type2':
            if sum_insured == '50000':
                return data['zone1']['type1']['50000']['KV'][1]
            elif sum_insured == '100000':
                pass
            elif sum_insured == '200000':
                pass
            elif sum_insured == '300000':
                pass
            elif sum_insured == '400000':
                pass
            elif sum_insured == '500000':
                pass
    elif zone == 'zone2':
        if type == 'type1':
            if sum_insured == '50000':
                pass
            elif sum_insured == '100000':
                pass
            elif sum_insured == '200000':
                pass
            elif sum_insured == '300000':
                pass
            elif sum_insured == '400000':
                pass
            elif sum_insured == '500000':
                pass
        elif type == 'type2':
            if sum_insured == '50000':
                pass
            elif sum_insured == '100000':
                pass
            elif sum_insured == '200000':
                pass
            elif sum_insured == '300000':
                pass
            elif sum_insured == '400000':
                pass
            elif sum_insured == '500000':
                pass
    elif zone == 'zone3':
        if type == 'type1':
            if sum_insured == '50000':
                pass
            elif sum_insured == '100000':
                pass
            elif sum_insured == '200000':
                pass
            elif sum_insured == '300000':
                pass
            elif sum_insured == '400000':
                pass
            elif sum_insured == '500000':
                pass
        elif type == 'type2':
            if sum_insured == '50000':
                pass
            elif sum_insured == '100000':
                pass
            elif sum_insured == '200000':
                pass
            elif sum_insured == '300000':
                pass
            elif sum_insured == '400000':
                pass
            elif sum_insured == '500000':
                pass

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
    
