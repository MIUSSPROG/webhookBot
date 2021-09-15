import os
import telebot
from telebot import types
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid
from datetime import date
import json

TOKEN = '1967324593:AAHj6V46s11TddOdpPQEfZGZtpZB5tIY9G8'
# '1967324593:AAHj6V46s11TddOdpPQEfZGZtpZB5tIY9G8'
APP_URL = f'https://school2120heroku.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
# some changes

name = ''
building = ''
subject = ''
question = ''
# answer = ''
questionId = ''
userId = ''

cred = credentials.Certificate("key.json")

default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://telegrambot-7c961-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://telegrambot-7c961.appspot.com/'
})


@bot.message_handler(commands=['start'])
def start(message):
    global userId
    userId = str(message.from_user.id)
    print("userId: " + userId)
    print("------------------------")
    sti = open('logo2120.png', 'rb')
    # sti = bucket.blob('AnimatedSticker.tgs')
    bot.send_photo(message.chat.id, sti)
    bot.send_message(message.from_user.id,
                     "✋ Добро пожаловать в Школу 2120!\n🤖 Меня зовут SchoolBot2120\n🧞‍♂ Я смогу Вам помочь!\n👇Вот что "
                     f"я умею!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('👔 Записаться на прием')
    item2 = types.KeyboardButton('🎓 Получить справку об обучении')
    # item3 = types.KeyboardButton('📄 Список каналов Школы 2120')
    item4 = types.KeyboardButton('📞 Контакты администрации')
    item5 = types.KeyboardButton('🙋‍♀️🙋‍♂️ Задать свой вопрос')
    item6 = types.KeyboardButton('📌 Полезные ссылки')
    item7 = types.KeyboardButton('❓ ЧаВО')
    item8 = types.KeyboardButton('📒 История вопросов')
    item9 = types.KeyboardButton('🙈 Не нашли что хотели!?')
    markup.add(item1, item2, item4, item5, item6, item7, item8, item9)
    bot.send_message(message.chat.id,
                     'Здравствуйте, <b>{0.first_name}</b>! Выберите интересующий вас раздел =>'.format(
                         message.from_user),
                     reply_markup=markup, parse_mode='html')
    # bot.register_next_step_handler(message, reg_name)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    # global userId
    userId = str(message.from_user.id)
    if message.chat.type == 'private':
        if message.text == '🙋‍♀️🙋‍♂️ Задать свой вопрос':
            bot.send_message(message.from_user.id, "Напишите свой вопрос...")
            bot.register_next_step_handler(message, add_question)
        elif message.text == '📒 История вопросов':
            all_questions_json = str(db.reference(f"telegrambot-7c961-default-rtdb/{userId}").get()).replace("\'", "\"")
            question_ids_data = json.loads(all_questions_json)
            for q_id in question_ids_data:
                question_info_json = str(db.reference(f"telegrambot-7c961-default-rtdb/{userId}/{q_id}").get()).replace(
                    "\'", "\"")
                question_info_data = json.loads(question_info_json)
                cur_answer = str(question_info_data["answer"])
                cur_question = str(question_info_data["question"])
                cur_date = str(question_info_data["date"])
                if cur_answer == '':
                    cur_answer = 'Ответа пока нет...'
                bot.send_message(message.chat.id, f'{cur_question}\n<i>{cur_date}</i>\n<b>{cur_answer}</b>',
                                 parse_mode='html')

        elif message.text == '🙈 Не нашли что хотели!?':
            bot.send_message(message.chat.id,
                             "Мы постоянно наделяем нашего бота новыми знаниями 👨‍🎓 и поэтому просим Вас написать чего ему не хватает?")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Добавить свои пожелания')
            item2 = types.KeyboardButton('◀️ Назад')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, '🙈 Не нашли что хотели!?', reply_markup=markup)
        elif message.text == 'Добавить свои пожелания':
            bot.send_message(message.chat.id, 'Напишите, что бы Вы еще хотели увидеть у нашего бота?')
            bot.register_next_step_handler(message, add_wish)
        elif message.text == '❓ ЧаВО':
            bot.send_message(message.chat.id,
                             '<a href="https://sch2120tn.mskobr.ru/important-answers">Ответы, важные для всех</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
        elif message.text == '🎓 Получить справку об обучении':
            bot.send_message(message.chat.id,
                             '<a href="https://docs.google.com/forms/d/1Zu0Q18MWmNVp9mYkkV-Bqn6jHAoNZhss2Mcrnn-fVKE'
                             '/viewform?edit_requested=true">Получить справку об обучении</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
        elif message.text == '📌 Полезные ссылки':
            bot.send_message(message.chat.id,
                             '<a href="http://window.edu.ru/">Информационная система "Единое окно доступа к '
                             'образовательным ресурсам"</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="http://fcior.edu.ru/">Федеральный центр информационно-образовательных '
                             'ресурсов</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="http://www.edu.ru/">Федеральный портал «Российское образование»</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="https://edu.gov.ru/">Министерство образования и науки РФ</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="https://www.mos.ru/uslugi/">Раздел "Услуги и сервисы" на mos.ru</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="http://school-collection.edu.ru/">Единая коллекция цифровых образовательных '
                             'ресурсов</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="https://www.mos.ru/">Официальный сайт Правительства г. Москвы</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="https://school.moscow/">Школа Большого Города</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="https://www.mos.ru/donm/">Информационный портал</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="https://mcko.ru/">Государственное автономное образовательное '
                                              'учреждение дополнительного профессионального образования города Москвы '
                                              '«Московский центр качества образования»</a>\n ', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="https://mcko.ru/pages/center_for_independent_diagnostic_null'
                             '">Центр независимой диагностики</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="http://rcoi.mcko.ru/">Региональный центр обработки информации города Москвы</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/rcoi/contacts/">Горячая линия ГИА</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="http://rcoi.mcko.ru/docs/">Нормативные документы ГИА-11, ГИА-9</a>\n',
                             parse_mode='html', disable_web_page_preview=True)

            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/gia-11-ege-gve/exam-schedule/">Расписание '
                                              'ГИА-11</a>\n', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/gia-11-ege-gve/final-composition'
                                              '-presentation/registration-and-conduct/">Итоговое сочинение ('
                                              'изложение)</a>\n', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/gia-11-ege-gve/">Информация для '
                                              'участников ГИА-11</a>\n', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/gia-11-ege-gve/special-conditions'
                                              '/">Организация специализированных условий для проведения ГИА-11</a>\n'
                             , parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/gia-11-ege-gve/exam-schedule/">Результаты '
                                              'ГИА и подача апелляций ГИА-11</a>\n', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/conflict-commission-gia-11/general'
                                              '-information/">Конфликтная комиссия ГИА-11</a>\n', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/gia-9-oge-gve/examination-schedule'
                                              '/">Расписание ГИА-9</a>\n', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/gia-9-oge-gve/">Информация для участников '
                                              'ГИА-9</a>\n', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/gia-9-oge-gve/special-conditions'
                                              '/">Организация специализированных условий ГИА-9</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="http://rcoi.mcko.ru/conflict-commission-gia-9/general'
                                              '-information/">Конфликтная комиссия ГИА-9</a>\n', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="https://mcko.ru/pages/medalists">Медаль "За особые успехи в '
                                              'обучении"</a>\n', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="https://mcrkpo.ru/%D0%BF%D0%BE%D0%BB%D0%B5%D0%B7%D0%BD%D1%8B'
                                              '%D0%B5%20%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D1%8B/">Полезные ссылки '
                                              'учителям</a>\n', parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="https://www.instagram.com/school2120/">Instagram Школа 2120</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="https://www.youtube.com/channel/UCuqRgk0XgHS0UR6oX3rb2Dg">Youtube Школа 2120</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id, '<a href="https://vk.com/sch2120">Vkontakte Школа 2120</a>\n',
                             parse_mode='html', disable_web_page_preview=True)
            bot.send_message(message.chat.id,
                             '<a href="https://www.facebook.com/school2120/">Facebook Школа 2120</a>\n',
                             parse_mode='html', disable_web_page_preview=True)

        elif message.text == '👔 Записаться на прием':
            bot.send_message(message.chat.id,
                             '<a href="https://forms.yandex.ru/u/60b09fc172d9ebd3f53d9af1/">Заявка на посещение</a>',
                             parse_mode='html')
        elif message.text == '📞 Контакты администрации':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Социальная служба')
            item2 = types.KeyboardButton('Библиотека')
            item3 = types.KeyboardButton('Секретарь учебной части(школа)')
            item4 = types.KeyboardButton('Секретарь учебной части(детский сад)')
            item5 = types.KeyboardButton('Организация питания')
            item6 = types.KeyboardButton('Отдел кадров')
            item7 = types.KeyboardButton('Бухгалтерия')
            item8 = types.KeyboardButton('Директор')
            item9 = types.KeyboardButton('Заместитель директора по управлению ресурсами')
            item10 = types.KeyboardButton('Заместитель директора по воспитательной работе, социализации и дополнительному образованию')
            item11 = types.KeyboardButton('Заместитель директора по содержанию дошкольного и школьного образования')
            item12 = types.KeyboardButton('Заместитель директора по контролю качества образования')
            item13 = types.KeyboardButton('Проблемы с электронным дневником')
            item14 = types.KeyboardButton('Прием в школу и группы реализующие программы дошкольного образования')
            back = types.KeyboardButton('◀️ Назад')
            markup.add(item8, item9, item10, item11, item12, item13, item14, item1, item2, item3, item4, item5, item6, item7, back)
            bot.send_message(message.chat.id, '📞 Контакты администрации', reply_markup=markup)

        elif message.text == 'Директор':
            bot.send_message(message.chat.id, 'Ланщиков Дмитрий Николаевич\n<b>+79687490078</b>', parse_mode='html')
        elif message.text == 'Заместитель директора по управлению ресурсами':
            bot.send_message(message.chat.id, 'Коренков Сергей Николаевич\n<b>+79265964431</b>', parse_mode='html')
        elif message.text == 'Заместитель директора по воспитательной работе, социализации и дополнительному образованию':
            bot.send_message(message.chat.id, 'Пономаренко Елена Викторовна\n<b>+79853173563</b>', parse_mode='html')
        elif message.text == 'Заместитель директора по содержанию дошкольного и школьного образования':
            bot.send_message(message.chat.id, 'Оганесова Елена Артемовна\n<b>+79857899741</b>', parse_mode='html')
        elif message.text == 'Заместитель директора по контролю качества образования':
            bot.send_message(message.chat.id, 'Шурухина Алла Юрьевна\n<b>+79857642316</b>', parse_mode='html')
        elif message.text == 'Проблемы с электронным дневником':
            bot.send_message(message.chat.id, 'Мостовая Вера Алексеевна\n<b>+79661878014</b>\n\nГригорьева Ирина Геннадьевна\n<b>+74591233346(доб. 2024)</b>\n\nБоева Анастасия Викторовна\n<b>+79857899668</b>', parse_mode='html')
        elif message.text == 'Прием в школу и группы реализующие программы дошкольного образования':
            bot.send_message(message.chat.id, 'Соловейчик Екатерина Геннадьевна\n<b>+79857642971</b>', parse_mode='html')
        elif message.text == 'Социальная служба':
            bot.send_message(message.chat.id, 'Синев Юрий Алексеевич\nВремя работы: <i>пн-пт 8:00-17:00</i>\nтел.: '
                                              '<b>+79857899649</b>', parse_mode='html')
        elif message.text == 'Библиотека':
            bot.send_message(message.chat.id, 'Пономарева Светлана Юрьевна\nВремя работы: <i>пн-пт '
                                              '8:00-17:00</i>\nтел.: '
                                              '<b>+79269428766</b>\n'
                                              '<b>+74951233346</b>, '
                                              'доб. 2002', parse_mode='html')
        elif message.text == 'Секретарь учебной части(школа)':
            bot.send_message(message.chat.id, 'Соловейчик Екатерина Геннадьевна\nДалиева Сурая Адамовна\nВремя '
                                              'работы: <i>Пн 9:00-12:00, Чт 16:00-19:00</i>\nтел.: '
                                              '<b>+79857642971</b>\n<b>+79852800465</b>\n<b>+74951233346 доб. 2007, '
                                              '2008</b>', parse_mode='html')
        elif message.text == 'Секретарь учебной части(детский сад)':
            bot.send_message(message.chat.id, 'Соловейчик Екатерина Геннадьевна\nДалиева Сурая Адамовна\nВремя '
                                              'работы: <i>Пн 16:00-19:00, Ср 16:00-20:00, Пт 8:00-12:00</i>\nтел.:'
                                              '<b>+79852800465</b>\n<b>+79857642971</b>', parse_mode='html')
        elif message.text == 'Организация питания':
            bot.send_message(message.chat.id, 'Соловьева Оксана Николаевна\nВремя работы: <i>Пн-Пт 8.00-17.00</i>\n'
                                              'тел.: <b>+79857642317</b>', parse_mode='html')
        elif message.text == 'Отдел кадров':
            bot.send_message(message.chat.id, 'Васильева Елена Александровна\nВремя работы: <i>Пн-Пт 8.00-17.00</i>\n'
                                              'тел.: <b>+74951233346, доб. 2015, 2016</b>', parse_mode='html')
        elif message.text == 'Бухгалтерия':
            bot.send_message(message.chat.id, 'Мамыкина Татьяна Валентиновна\nВремя работы: <i>Пн-Пт 9.00-17.00 Обед: '
                                              '13.00-14.00</i>\n '
                                              'тел.: <b>+74951233346, доб. 2015, 2016</b>', parse_mode='html')
        elif message.text == '◀️ Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('👔 Записаться на прием')
            item2 = types.KeyboardButton('🎓 Получить справку об обучении')
            # item3 = types.KeyboardButton('📄 Вывести список каналов Школы 2120')
            item4 = types.KeyboardButton('📞 Контакты администрации')
            item5 = types.KeyboardButton('🙋‍♀️🙋‍♂️ Задать свой вопрос')
            item6 = types.KeyboardButton('📌 Полезные ссылки')
            item7 = types.KeyboardButton('❓ ЧаВО')
            item8 = types.KeyboardButton('📒 История вопросов')
            item9 = types.KeyboardButton('🙈 Не нашли что хотели!?')
            markup.add(item1, item2, item4, item5, item6, item7, item8, item9)
            bot.send_message(message.chat.id, 'Выберите подходящий пункт =>', reply_markup=markup)
        elif message.text == 'nimdanimda2120!':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🧾 Список вопросов')
            item2 = types.KeyboardButton('🗣 Пожелания пользователей')
            item3 = types.KeyboardButton('◀️ Назад')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, 'Добро пожаловать в Админ панель!', reply_markup=markup)
        elif message.text == '🗣 Пожелания пользователей':
            db_info = db.reference("telegrambot-7c961-default-rtdb/wishes/").get()
            if db_info is not None:
                user_wishes_json = str(db_info).replace("\'", "\"")
                user_wishes_ids = json.loads(user_wishes_json)
                number = 0
                for id in user_wishes_ids:
                    wish_data_json = str(db.reference(f"telegrambot-7c961-default-rtdb/wishes/{id}").get()).replace("\'", "\"")
                    wish_data = json.loads(wish_data_json)
                    cur_wish = str(wish_data["wish"])
                    number += 1
                    bot.send_message(message.chat.id, f'{number}. {cur_wish}')
            else:
                bot.send_message(message.chat.id, '👐 Пока новых пожеланий нет!')
        elif message.text == '🧾 Список вопросов':
            user_ids_json = str(db.reference("telegrambot-7c961-default-rtdb/").get()).replace("\'", "\"")
            ids = json.loads(user_ids_json)
            try:
                count_not_answered = 0
                for uid in ids:
                    all_questions_json = str(db.reference(f"telegrambot-7c961-default-rtdb/{uid}").get()).replace("\'",
                                                                                                                  "\"")
                    question_ids_data = json.loads(all_questions_json)
                    for q_id in question_ids_data:
                        question_info_json = str(
                            db.reference(f"telegrambot-7c961-default-rtdb/{uid}/{q_id}").get()).replace("\'", "\"")
                        question_info_data = json.loads(question_info_json)
                        cur_answer = str(question_info_data["answer"])
                        cur_question = str(question_info_data["question"])
                        cur_date = str(question_info_data["date"])
                        if cur_answer == "":
                            keyboard = types.InlineKeyboardMarkup()
                            key_yes = types.InlineKeyboardButton(text='Ответить',
                                                                 callback_data=f'{str(uid)}&{str(q_id)}')
                            keyboard.add(key_yes)
                            bot.send_message(message.chat.id, f'<b>{cur_question}</b>\n<i>{cur_date}</i>',
                                             reply_markup=keyboard, parse_mode='html')
                            count_not_answered += 1
                if count_not_answered == 0:
                    bot.send_message(message.chat.id, "Нет новых неотвеченных вопросов 🥳")
            except Exception as ex:
                print(ex)

        else:
            bot.send_message(message.chat.id, 'Выберите интересующий Вас раздел')


def add_wish(message):
    user_wish = str(message.text)
    new_wish_id = uuid.uuid4().hex
    new_wish = {
        "wish": user_wish,
    }
    db.reference("telegrambot-7c961-default-rtdb/wishes/" + new_wish_id).set(new_wish)
    bot.send_message(message.from_user.id,
                     'Ваш вклад бесценен! 💎 Благодаря Вам мы станем лучше!')


def add_question(message):
    # global question
    question = str(message.text)
    # global userId
    uId = str(message.from_user.id)
    lines = ''
    with open('words.txt') as f:
        lines = f.readlines()
        words = []
    for word in lines:
        words.append(word.replace('\n', ''))

    is_bad_word = False
    for word in words:
        if word in question:
            is_bad_word = True
            break

    today = date.today()
    d = today.strftime("%d/%m/%Y")
    if not is_bad_word:
        new_question_id = uuid.uuid4().hex
        new_question = {
            "question": question,
            "answer": "",
            "date": d
        }
        db.reference("telegrambot-7c961-default-rtdb/" + uId + "/" + new_question_id).set(new_question)
        bot.send_message(message.from_user.id,
                         'Ваш вопрос принят! Вы сможете найти на него ответ в разделе "История вопросов" ')
    else:
        bot.send_message(message.from_user.id, "Ваш вопрос не ясен")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global questionId
    global question
    global userId
    try:
        info = str(call.data).split("&")
        userId = info[0]
        questionId = info[1]
        # userId = str(call.message.from_user.id)
        # userId = '498046504'
        # questionId = str(call.data)
        # question = str(db.reference(f"telegrambot-7c961-default-rtdb/{userId}/{questionId}").get()).split("'")[11]
        # question = str(db.reference(f"telegrambot-7c961-default-rtdb/{userId}/{questionId}").get())
        # print("userId ######### " + userId)
        # print("questionId ########### " + questionId)
        # questionId = data.split('&')[0]
        # question = data.split('&')[1]
        question_to_answer_json = str(
            db.reference(f"telegrambot-7c961-default-rtdb/{userId}/{questionId}").get()).replace("\'", "\"")
        question = json.loads(question_to_answer_json)["question"]
        bot.send_message(call.message.chat.id, f"Введите ответ на вопрос:\n<b>{question}</b> => ", parse_mode='html')
        bot.register_next_step_handler(call.message, get_answer)
    except Exception as ex:
        print(ex)


def get_answer(message):
    # global answer
    # global question
    # global questionId
    answer = message.text
    today = date.today()
    d = today.strftime("%d/%m/%Y")
    new_answer = {
        "question": question,
        "answer": answer,
        "date": d
    }
    db.reference(f"telegrambot-7c961-default-rtdb/{userId}/{questionId}").set(new_answer)
    bot.send_message(message.chat.id, "Ответ сохранен!")


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
