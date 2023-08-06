import requests
import re
from tkinter import *
import tkinter as tk
from tkinter import ttk


class CurrencyConverter:
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, f, t, am):
        if f != 'USD':
            am = am / self.currencies[f]
        amount = round(am * self.currencies[t], 4)
        return amount


class App(tk.Tk):
    def __init__(self, c):
        tk.Tk.__init__(self)
        self.title = 'Currency Converter'
        self.converter = c
        self.geometry('500x250')

        # Label head
        self.intro_label = tk.Label(self, text='Welcome to Currency Converter',
                                    fg='#636363', borderwidth=3,
                                    font=('Courier', 18, 'bold'))
        self.date_label = tk.Label(self,
                                   text=f'1 USD = {self.converter.convert("USD", "BYN", 1)}BYN\nDate: {self.converter.data["date"]}',
                                   fg='#636363', borderwidth=3,
                                   font=('Courier', 18, 'bold'))
        self.intro_label.place(x=10, y=5)
        self.date_label.place(x=100, y=50)

        # Entry box
        validation = (self.register(self.number_only), '%d', '%P')
        self.amount_field = Entry(self, justify=CENTER,
                                  validate='key', validatecommand=validation)
        self.converted_amount = Label(self, text='', fg='red', justify=CENTER,
                                      width=17, borderwidth=3)
        self.amount_field.place(x=36, y=150)
        self.converted_amount.place(x=250, y=150)

        # Dropdown menu
        self.from_currency_var = StringVar(self)
        self.from_currency_var.set('USD')  # default values for dropdown
        self.to_currency_var = StringVar(self)
        self.to_currency_var.set('BYN')  # default values for dropdown

        font = ('Courier', 15, 'bold')
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_dropdown = ttk.Combobox(
            self, textvariable=self.from_currency_var,
            values=list(self.converter.currencies.keys()),
            font=font, width=12, justify=CENTER
        )
        self.to_dropdown = ttk.Combobox(
            self, textvariable=self.to_currency_var,
            values=list(self.converter.currencies.keys()),
            font=font, width=12, justify=CENTER
        )
        self.from_dropdown.place(x=36, y=120)
        self.to_dropdown.place(x=250, y=120)

        # Button "convert"
        self.btn = Button(self, text="Convert", fg='red', font=font,
                          command=self.perform)
        self.btn.place(x=200, y=200)

    def perform(self):
        amount = float(self.amount_field.get())
        f_cur = self.from_currency_var.get()
        to_cur = self.to_currency_var.get()

        converted = self.converter.convert(f_cur, to_cur, amount)
        self.converted_amount.config(text=str(converted))

    def number_only(self, action, string):
        r = re.compile(r'[0-9]*?(\.)?[0-9]*$')
        # 0.93
        res = r.match(string)
        return string == '' or (string.count('.') <= 1 and res is not None)