# from threading import Thread
#
# import requests
#
#
# def threaded(fn):
#     def wrapper(*args, **kwargs):
#         thread = Thread(target=fn, args=args, kwargs=kwargs)
#         thread.start()
#         return thread
#
#     return wrapper
#
#
# @threaded
# def save_user(user):
#     post_data = {
#         'tg_id': user.id,
#         'username': user.username,
#         'first_name': user.first_name,
#         'last_name': user.last_name
#     }
#     requests.post(url='http://127.0.0.1:8000/users/register/', data=post_data)