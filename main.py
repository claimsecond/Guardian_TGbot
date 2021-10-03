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
    # log(message)


@bot.callback_query_handler(func=lambda call:'dcv' in call.data)
def dcv_zone_handler(call):
    '''обработчик нажатия на кнопку ДЦВ'''
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Зона 1', callback_data='z1')
    btn2 = types.InlineKeyboardButton(text='Зона 2', callback_data='z2')
    btn3 = types.InlineKeyboardButton(text='Зона 3', callback_data='z3')
    kb.add(btn1, btn2, btn3)
    bot.send_message(
        call.from_user.id, "<b>За ДЦВ маршрутні автобуси та ТЗ, що використовуються в якості ТАКСІ, на страхування НЕ ПРИЙМАЮТЬСЯ.</b>", parse_mode='HTML')
    bot.send_message(
        call.from_user.id, "*Виберіть зону:* \nКиїв, Київська обл\. \- *1* \nХарків, Одеса, Дніпро, Львів, Запоріжжя, Кривий Ріг, ТЗ з іноземною реєстрацією \- *2* \nІнші населені пункти \- *3*",
        reply_markup=kb, parse_mode='MarkdownV2'
    )
    # log(call)

@bot.callback_query_handler(func=lambda call: 'z1' or 'z2' or 'z3' in call.data)
def dcv_auto_type_handler(call):
    '''обрабатывает выбор зоны для ДЦВ'''
    global dcv_zone
    if 'z1' in call.data:
        dcv_zone = 1
    elif 'z2' in call.data:
        dcv_zone = 2
    else:
        dcv_zone = 3
    # print("Вибрано зону " + dcv_zone)
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        text='A1, A2, F, B1, B2, B3, E', callback_data='t1')
    btn2 = types.InlineKeyboardButton(
        text='B4, C1, D1, C2, D2', callback_data='t2')
    kb.add(btn1, btn2)
    bot.send_message(
        call.from_user.id, "*Виберіть тип ТЗ*", reply_markup=kb, parse_mode='MarkdownV2'
    )

@bot.callback_query_handler(func=lambda call: 't1' or 't2' in call.data)
def dcv_suminsured_handler(call):
    '''обрабатывает ввод типа ТС для ДЦВ'''
    global dcv_auto_type
    if 't1' in call.data:
        dcv_auto_type = 1
    else:
        dcv_auto_type = 2
    # print("Вибрано тип авто " + dcv_auto_type)
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='50 000', callback_data='50000')
    btn3 = types.InlineKeyboardButton(text='100 000', callback_data='100000')
    btn4 = types.InlineKeyboardButton(text='200 000', callback_data='200000')
    btn5 = types.InlineKeyboardButton(text='300 000', callback_data='300000')
    btn6 = types.InlineKeyboardButton(text='400 000', callback_data='400000')
    btn7 = types.InlineKeyboardButton(text='500 000', callback_data='500000')
    kb.add(btn1, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(call.from_user.id, "*Виберіть страхову суму*", reply_markup=kb, parse_mode='MarkdownV2')


# def log(message):
#     print("\n ------")
#     from datetime import datetime
#     print(datetime.now())
#     print("Сообщение от {0} {1}. (id = {2}) \nТекст = {3}".format(message.from_user.first_name,
#                                                                   message.from_user.last_name,
#                                                                   str(message.from_user.id), message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
    
