import dong
import dong.auth as auth

def login_required(message="Can't find any credential information, please login first."):

    def decorator(fun):

        def wrapper(*args, **kwargs):
            netrc = auth.load_netrc()
            login = netrc[dong.SERVER_NAME]['login']
            password = netrc[dong.SERVER_NAME]['password']

            if login is None or password is None:
                print(message)
            else:
                fun(*args, **kwargs)

        return wrapper

    return decorator
