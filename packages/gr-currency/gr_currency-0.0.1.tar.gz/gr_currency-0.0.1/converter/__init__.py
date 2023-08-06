from converter.currency import *


if __name__ == '__main__':
    c = CurrencyConverter('https://api.exchangerate-api.com/v4/latest/USD')
    App(c)
    mainloop()