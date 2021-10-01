# import requests
#
# from bot.keyboards import get_menu_keyboard, get_categories_list_keyboard, get_category_detail_keyboard, \
#     get_product_detail_keyboard
# from bot.utils import save_user
#
#
# def start(update, context):
#     user = update.effective_user
#     save_user(user)
#     update.message.reply_text('Menu', reply_markup=get_menu_keyboard())
#
#
# def categories_list(update, context):
#     query = update.callback_query
#
#     data = requests.get('http://127.0.0.1:8000/api/category/').json()
#
#     text = ''
#     for category in data:
#         text += f'{category["id"]}. {category["title"]}\n'
#
#     query.edit_message_text(text=text, reply_markup=get_categories_list_keyboard(data))
#
#
# def category_detail(update, context):
#     query = update.callback_query
#     pk = query.data.split('_')[1]
#
#     data = requests.get(f'http://127.0.0.1:8000/api/category/{pk}/').json()
#
#     if not data:
#         query.edit_message_text(text='No products yet',
#                                 reply_markup=get_category_detail_keyboard())
#         return
#
#     text = ''
#     for product in data:
#         text += f'{product["id"]}. {product["title"]}\n'
#
#     query.edit_message_text(text=text, reply_markup=get_category_detail_keyboard(data))
#
#
# def product_detail(update, context):
#     query = update.callback_query
#     pk = query.data.split('_')[1]
#
#     product = requests.get(f'http://127.0.0.1:8000/api/products/{pk}/').json()
#
#     text = f'Title: {product["title"]}\n' \
#            f'Price: {product["price"]}\n' \
#            f'Description: {product["description"]}'
#
#     context.bot.send_photo(
#         chat_id=query.message.chat.id,
#         photo=requests.get(product["image"]).content,
#         caption=text,
#         reply_markup=get_product_detail_keyboard(product)
#     )
#     context.bot.delete_message(chat_id=query.message.chat.id,
#                                message_id=query.message.message_id)
#
#
# def basket(update, context):
#     query = update.callback_query
#     print(query.data)
#     context.bot.delete_message(chat_id=query.message.chat.id,
#                                message_id=query.message.message_id)
#     # print(query.message.callback_data)
#
#     query.message.reply_text('Menu', reply_markup=get_menu_keyboard())
#
#
# def korzina(update, context):
#     query = update.callback_query
#     query.message.reply_text(message_id=5687, reply_markup=get_menu_keyboard())
#
#
# def buy(update, context):
#     query = update.callback_query
#     context.bot.delete_message(chat_id=query.message.chat.id,
#                                message_id=query.message.message_id)
#     # print(query.message.callback_data)
#     query.message.reply_text('Menu', reply_markup=get_menu_keyboard())
#
#
# def search(update, context):
#     pass
#
#
# def back(update, context):
#     query = update.callback_query
#
#     context.bot.delete_message(chat_id=query.message.chat.id,
#                                message_id=query.message.message_id)
#
#     query.message.reply_text(text='Menu', reply_markup=get_menu_keyboard())
