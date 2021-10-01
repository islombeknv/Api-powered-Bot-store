from threading import Thread

import requests

users = dict()


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


@threaded
def save_user(message, number, address):
    post_data = {
        'tg_id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'number': number,
        'address': address,
    }
    requests.post(url='http://127.0.0.1:8000/users/register/', data=post_data)


@threaded
def save_order(order):
    requests.post(url='http://127.0.0.1:8000/api/order/', data=order)
