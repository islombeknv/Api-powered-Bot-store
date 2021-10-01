import requests
import telebot
from telebot import types

from keyboards import welcome, menu_keyboard, category, order, get_back_keyboard, get_order, saveorder, get_order_basket
from utils import save_user, save_order

bot = telebot.TeleBot('Token')

users = dict()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global user_order_id
    user_order_id = message.chat.id

    users[message.from_user.id] = dict()
    bot.send_message(message.chat.id,
                     'Ro\'yxatdan o\'tish uchun kerakli ma\'limotlarni yuboring',
                     reply_markup=welcome()
                     )

    bot.register_next_step_handler(message, first_name)


def first_name(message):
    try:
        if message.contact.phone_number:
            users[message.from_user.id]['number'] = message.contact.phone_number
            bot.send_message(message.chat.id,
                             'Manzilingizni kiriting', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, menu)
    except:
        bot.send_message(message.chat.id,
                         'Xato!')
        bot.register_next_step_handler(message, first_name)


def menu(message):
    users[message.from_user.id]['address'] = message.text
    data = users[message.from_user.id]
    number = data.get('number', '-')
    address = data.get('address', '-')
    save_user(message, number, address)
    bot.send_message(message.chat.id,
                     f'Salom *{message.from_user.first_name} {message.from_user.last_name}* '
                     f'ro\'yxatdan o\'tish muvafiyaqatli o\'tdingiz.',
                     reply_markup=menu_keyboard(), parse_mode='Markdown'
                     )
    bot.register_next_step_handler(message, buttons)


@bot.message_handler(content_types=['text'])
def buttons(message):
    if message.text == '🛍 Bo\'limlar va mahsulotlar':
        data = requests.get('http://127.0.0.1:8000/api/category/').json()
        bot.send_message(message.chat.id, '_', reply_markup=get_back_keyboard())
        bot.send_message(message.chat.id, 'Kerakli categoryani tanlang', reply_markup=category(data))
        bot.delete_message(message.chat.id, message.id)
        bot.register_next_step_handler(message, products)

    elif message.text == 'ℹ️ Biz haqimizda':
        bot.send_message(message.chat.id, "📞 *Aloqa markazi*: +998712310880 \n\n👨🏻‍💻 *Telegram*: @IslombekNv",
                         parse_mode='Markdown')

    elif message.text == '👤 Mening ma\'limotlarim':
        data = requests.get(f'http://127.0.0.1:8000/api/user/{message.from_user.id}/').json()
        for i in data:
            data = i
        firstname = data['first_name']
        number = data['number']
        address = data['address']
        bot.send_message(message.chat.id, f'*👤 Ism:* {firstname},\n\n'
                                          f'*📞 Nomer:* {number},\n'
                                          f'\n*📍 Manzil:* {address}',
                         parse_mode='Markdown')

    elif message.text == '📦 Buyurtmalarim':
        bot.send_message(message.chat.id, 'Buyurtmalarim')
        data = requests.get(f'http://127.0.0.1:8000/api/order/{message.from_user.id}/').json()
        if data:
            for order in data:
                bot.send_message(message.chat.id,
                                 f'*ID:* {order["id"]},\n'
                                 f'\n*Tovar:* {order["product"]},\n\n'
                                 f'*Narxi:* {order["price"]}{"$"},\n'
                                 f'\n*Manzil:* {order["address"]}'
                                 f'\n\n*Holati:* {order["order"] or ["Tastiqlanman"]}',
                                 parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, 'Sizda buyurtmalar yo\'q')

    elif message.text == '⬅️ Orqaga':
        bot.send_message(message.chat.id,
                         '🏠 Bosh menyu',
                         reply_markup=menu_keyboard())
        bot.delete_message(message.chat.id, message.id)

    elif message.text == '🛒 Korzina':
        try:
            for i in users.values():
                for i in i.get('basket'):
                    product = requests.get(f'http://127.0.0.1:8000/api/products/{i}/').json()
                    text = f'Title: {product["title"]}\n' \
                           f'Price: {product["price"]}{"$"}\n' \
                           f'Description: {product["description"]}'

                    bot.send_photo(message.chat.id, photo=requests.get(product["image"]).content,
                                   caption=text, reply_markup=get_order_basket(product))
        except Exception:
            bot.send_message(message.chat.id, 'Tovarlar qo\'shilmagan')
            bot.register_next_step_handler(message, buttons)


@bot.callback_query_handler(func=lambda call: call.data.startswith('product_'))
def products(call):
    try:
        pk = call.data.split('_')[1]

        data = requests.get(f'http://127.0.0.1:8000/api/category/{pk}/').json()

        if not data:
            bot.edit_message_text('No products yet',
                                  call.message.chat.id,
                                  call.message.id)
            return products

        text = ''
        x = 1
        for product in data:
            text += f'{x}. {product["title"]}\n'
            x += 1
        bot.edit_message_text(text, call.message.chat.id,
                              call.message.id,
                              reply_markup=order(data))
    except:
        return


@bot.callback_query_handler(func=lambda call: call.data.startswith('delproduct_'))
def product_detail(call):
    try:
        pk = call.data.split('_')[1]

        product = requests.get(f'http://127.0.0.1:8000/api/products/{pk}/').json()

        text = f'Title: {product["title"]}\n' \
               f'Price: {product["price"]}{"$"}\n' \
               f'Description: {product["description"]}'

        bot.send_photo(call.message.chat.id, photo=requests.get(product["image"]).content,
                       caption=text, reply_markup=get_order(product))
        bot.delete_message(call.message.chat.id, call.message.id)

    except:
        return


@bot.callback_query_handler(func=lambda call: call.data.startswith('toorder_'))
def product_detail(call):
    try:
        product = call.data.split('_')[1]
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Buyurtmangizni soni yozing.',
                         reply_markup=saveorder(product))
    except:
        return


@bot.callback_query_handler(func=lambda call: call.data.startswith('count_'))
def order_comment(call):
    try:
        pk = call.data.split('_')[1]
        product = requests.get(f'http://127.0.0.1:8000/api/products/{pk}/').json()
        user = requests.get(f'http://127.0.0.1:8000/api/user/{call.from_user.id}/').json()
        for i in user:
            user = i
        order = {"p_id": product["id"],
                 "user_id": user_order_id,
                 "user": f'{user["first_name"]} {user["last_name"]} '
                         f'(username: {user["username"]})',
                 "product": product["title"],
                 "price": product["price"],
                 "number": user["number"],
                 "address": f'{user["address"]}',
                 }
        save_order(order)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id,
                         f'Buyurtmangiz yuborildi ✅\n'
                         f'ID: {product["id"]}\n'
                         f'Tovar: {product["title"]}\n'
                         f'Narxi: {product["price"]}{"$"}\n'
                         f'Miqdori: {call.data.split("_")[2]}\n',
                         reply_markup=menu_keyboard())
    except:
        return


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart_'))
def order_c(call):
    user_pk = call.message.chat.id
    pk = call.data.split('_')[3]

    if 'basket' not in users[user_pk].keys():
        users[user_pk]['basket'] = [pk]
    else:
        users[user_pk]['basket'].append(pk)

    bot.answer_callback_query(callback_query_id=call.id, text='Savatga qo\'shildi')
    bot.send_message(call.message.chat.id, 'Savatga qo\'shildi', reply_markup=menu_keyboard())
    bot.delete_message(call.message.chat.id, call.message.id)


bot.polling()
