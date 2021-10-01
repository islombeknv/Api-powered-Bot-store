# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
#
#
# def get_menu_keyboard():
#     keyboard = [
#         [
#             InlineKeyboardButton('Categories', callback_data='categories'),
#             InlineKeyboardButton('Search', callback_data='search')
#         ],
#         [
#             InlineKeyboardButton('Korzina', callback_data='korzina')
#         ],
#     ]
#
#     return InlineKeyboardMarkup(keyboard)
#
#
# def get_categories_list_keyboard(data):
#     keyboard = []
#     temp = []
#     x = 1
#     for i in data:
#         temp.append(
#             InlineKeyboardButton(x, callback_data=f'category_{i["id"]}'),
#         )
#         x += 1
#     keyboard.append(temp)
#
#     keyboard.append(
#         [
#             InlineKeyboardButton('Back', callback_data='back'),
#         ]
#     )
#
#     return InlineKeyboardMarkup(keyboard)
#
#
# def get_category_detail_keyboard(data=None):
#     keyboard = []
#     if data:
#         temp = []
#         for i in data:
#             temp.append(
#                 InlineKeyboardButton(i["id"], callback_data=f'product_{i["id"]}'),
#             )
#         keyboard.append(temp)
#
#     keyboard.append(
#         [
#             InlineKeyboardButton('Back', callback_data='back'),
#         ]
#     )
#
#     return InlineKeyboardMarkup(keyboard)
#
#
# def get_product_detail_keyboard(product):
#     keyboard = [
#         [
#             InlineKeyboardButton('Add basket', callback_data=f'basket_{product}'),
#             InlineKeyboardButton('Buy', callback_data=f'buy_{product["id"]}'),
#         ],
#         [
#             InlineKeyboardButton('Back', callback_data='back'),
#         ],
#     ]
#
#     return InlineKeyboardMarkup(keyboard)