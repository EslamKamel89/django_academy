from django.conf import settings


def pr[T](val: T, title: str = "") -> T:
    if settings.DEBUG:
        print(f" -------------{title}------------- ")
        print("type = ", type(val))
        print("val = ", val)
    return val
