#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib2
import json
import rumps
import webbrowser

from rumps import *

#rumps.debug_mode(True)

with open('config.json') as config_file:    
    config = json.load(config_file)

city = config['city']
currency = config['currency']
kharkov_rates = 'https://kharkov.obmenka.ua/get_rates'
kiev_rates = 'https://kiev.obmenka.ua/get_rates'
if city == 'Киев':
    rates_url = kiev_rates
    obm_url = 'https://kiev.obmenka.ua'
else: 
    rates_url = kharkov_rates
    obm_url = 'https://obmenka.kharkov.ua'
last_rate = None

class ObmenkaStatusBarApp(rumps.App):

    def __init__(self):
        super(ObmenkaStatusBarApp, self).__init__("Obmenka",quit_button=None)


    @rumps.clicked('Курсы валют')
    def currency_rates(self,_):
        crates = str("USD-UAH: " + str(c['usd_uah']['retailBuy']) + "-" + str(c['usd_uah']['retailSell']) + "\n"
                     "EUR-UAH: " + str(c['eur_uah']['retailBuy']) + "-" + str(c['eur_uah']['retailSell']) + "\n"
                     "RUB-UAH: " + str(c['rub_uah']['retailBuy']) + "-" + str(c['rub_uah']['retailSell']) + "\n"
                     "GBP-UAH: " + str(c['gbp_uah']['retailBuy']) + "-" + str(c['gbp_uah']['retailSell']) + "\n"
                     "EUR-USD: " + str(c['eur_usd']['retailBuy']) + "-" + str(c['eur_usd']['retailSell']) + "\n"
                     "USD-RUB: " + str(c['usd_rub']['retailBuy']) + "-" + str(c['usd_rub']['retailSell']) + "\n"
                     "GBP-USD: " + str(c['gbp_usd']['retailBuy']) + "-" + str(c['gbp_usd']['retailSell']) + "\n"
                 )
        if rumps.alert(message=crates, title='Текущие курсы в '+city+'е', ok='Open Site', cancel='Close') == 1:
            webbrowser.open_new_tab(obm_url)

    @rumps.clicked("Электронные валюты")
    def open_dcr_site(_):
        dcr_url = 'https://changeinfo.ru'
        webbrowser.open_new_tab(dcr_url)

    @rumps.timer(60)
    def update_rates(self,_):
        req = urllib2.Request(rates_url, None, {'user-agent':'macos/toolbar.v.0.1.0a'})
        opener = urllib2.build_opener()
        try:
            f = opener.open(req)
            global c
            c = json.load(f)
        except Exception as e:
            print e
            if type(last_rate) == str:
                self.title = last_rate + "**"
        else:
            global rate
            rate = str(c[currency]['retailBuy']) + "-" + str(c[currency]['retailSell'])
            if last_rate != rate:
                self.title = str("*" + rate + "*")
                global last_rate
                if last_rate != None:
                    self.rate_changed("last_rate")
                last_rate = rate
            else:
                self.title = rate

    @rumps.clicked(city)
    def button(self, sender):
        global city
        global rates_url
        if city == 'Харьков':
            city = 'Киев' 
            rates_url = kiev_rates
            obm_url = 'https://kiev.obmenka.ua'
        else: 
            city = 'Харьков'
            rates_url = kharkov_rates
            obm_url = 'https://obmenka.kharkov.ua'
        sender.title = city
        self.update_rates(city)

    @rumps.clicked("О программе")
    def prefs(self, _):
        description = ('Программа показывает курсы в статус баре.\n'+
            'Обновление курсов происходит раз в минуту.\n'+
            'Если курс изменился, то он будет окружен зведочками - *курс*\n'+
            'Если курс не удалось получить, то он будет показан так: последний курс**\n'+
            'По умолчанию, город - Харьков, валюта - USD-UAH\n'+
            'Конфигурацию можно изменить в файле config.json\n'
            ) 
        rumps.alert(message=description, title='Obmenka Status Bar v.0.1.0a')

    @rumps.clicked('Выход')
    def clean_up_before_quit(_):
        #print 'execute clean up code'
        rumps.quit_application()

    #@rumps.clicked('Test') #fixed bug in rumps lib https://github.com/jaredks/rumps/issues/26
    def rate_changed(self, _):
        if config['notify'] == 'on':
            notification_text = "Был: " + str(last_rate) + " стал: " + str(rate)
            rumps.notification("Obmenka", "Изменение курса!", notification_text)

if __name__ == "__main__":
    ObmenkaStatusBarApp().run()
