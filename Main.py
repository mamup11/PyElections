from threading import Thread
import TwitterFeed
import atexit
import Predictor
import Menu

menu = "Seleccionar opcion:\n"\
       "1: Promedio de tweets por minuto\n"\
       "2: Ultima vez mencionado\n"\
       "3: Autores unicos\n"\
       "4: Analisis de sentimientos ultimos 3 minutos\n"\
       "5: Analisis de sentimientos ultimos 7 dias\n"\
       "0: Salir\n"

feed = None
predictor = None


def exit_handler():
    if feed is not None:
        feed.exit_handler()


def predictLast3Minutes():
    feed.exit_handler()
    Menu.pedictLast3Minutes()
    feed.stream()


def shutdown():
    exit_handler()
    exit(0)


switcher = {
    1: True,
    2: True,
    3: True,
    4: predictLast3Minutes,
    5: True,
    0: shutdown
}


def userInput():
    while True:
        print(menu)
        try:
            option=int(input('Input:'))

            funct = switcher.get(option, lambda: "Not an option")
            funct()
        except Exception as e:
            print("Invalid Input!")



if __name__ == '__main__':
    atexit.register(exit_handler)
    feed = TwitterFeed
    predictor = Predictor
    feed.stream()
    userInput()

