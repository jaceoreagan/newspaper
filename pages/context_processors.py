from .weather import get_weather


def weather(request):
    return {"weather": get_weather()}
    