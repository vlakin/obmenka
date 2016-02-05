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

version = '0.1.1'
city = config['city']
currency = config['currency']
kharkov_rates = 'https://kharkov.obmenka.ua/get_rates'
kharkov_url = 'https://obmenka.kharkov.ua'
kiev_rates = 'https://kiev.obmenka.ua/get_rates'
kiev_url = 'https://kiev.obmenka.ua'
if city == 'Киев':
    rates_url = kiev_rates
    obm_url = kiev_url
else: 
    rates_url = kharkov_rates
    obm_url = kharkov_url
last_rate = None



@rumps.clicked('Курсы валют')
def currency_rates(sender,_):
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


@rumps.clicked("НБУ")
def open_nbu_site(_):
    nbu_url = 'http://www.bank.gov.ua/control/uk/curmetal/detail/currency?period=daily'
    webbrowser.open_new_tab(nbu_url)


@rumps.timer(3600)
def update_bank_rates(sender):
    bank_rates_url = 'http://openrates.in.ua/rates'
    req = urllib2.Request(bank_rates_url, None, {'user-agent':'macos/toolbar'})
    opener = urllib2.build_opener()
    try:
        f = opener.open(req)
        global br
        br = json.load(f) #loading bank rates from json file 
    except Exception as e:
        print e
    else:
        nbu_usd.title = '\u0024 ' + str(br['USD']['nbu']['buy'])
        nbu_eur.title = '\u20A0 ' + str(br['EUR']['nbu']['buy'])
        nbu_rub.title = '\u20BD ' + str(br['RUB']['nbu']['buy'])
        mb_usd.title = '\u0024 ' + str(br['USD']['interbank']['buy']) + '-' + str(br['USD']['interbank']['sell'])
        mb_eur.title = '\u20A0 ' + str(br['EUR']['interbank']['buy']) + '-' + str(br['EUR']['interbank']['sell'])
        mb_rub.title = '\u20BD ' + str(br['RUB']['interbank']['buy']) + '-' + str(br['RUB']['interbank']['sell'])

        nbu_rates_button.title = 'НБУ: ' + str(br['USD']['nbu']['buy'])
        mb_rates_button.title = 'Межбанк: ' + str(br['USD']['interbank']['buy'])

@rumps.timer(60)
def update_rates(sender,_):
    req = urllib2.Request(rates_url, None, {'user-agent':'macos/toolbar.v.'+version})
    opener = urllib2.build_opener()

    try:
        f = opener.open(req)
        global c
        c = json.load(f) #trying to fetch obmenka's rates to json 
    except Exception as e:
        print e
        
        if str(last_rate) != 'None':
            sender.title = last_rate + "**"
        else:
            sender.title = 'Obmenka**'
            rates_button.set_callback(None)
            digital_rates_button.set_callback(None)
            city_button.set_callback(None)
    else:
        if sender.title == 'Obmenka**':
            rates_button.set_callback(currency_rates)
            digital_rates_button.set_callback(open_dcr_site)
            city_button.set_callback(default_city)
           
        global rate
        rate = str(c[currency]['retailBuy']) + "-" + str(c[currency]['retailSell'])
        if last_rate != rate:
            sender.title = str("*" + rate + "*")
            global last_rate
            if last_rate != None:
                rate_changed("last_rate")
            last_rate = rate
        else:
            sender.title = rate

        # Update interbank and NBU if they are not defined
        if nbu_rates_button.title == 'НБУ':
            update_bank_rates(app)

@rumps.timer(259200) # once per 3 days
def check_updates(sender,_):
    try:
        latest_version = urllib2.urlopen('http://vlak.us/~vlak/obmenka/latest-version').read()
    except Exception as e:
        print e
    else:
        latest_version = latest_version.rstrip()
        if str(version) < str(latest_version):
            print 'version!'+version+'!'
            print 'latest version!'+latest_version+'!'
            update_message = ('Необходимо обновление!\n'+
                'Последняя версия: Obmenka-'+latest_version+'\n'+
                'Последняя версия доступна на сайте:\n'+
                'http://vlak.us/~vlak/obmenka/Obmenka-latest.zip'
                )
            rumps.alert(message=update_message, title='Obmenka Status Bar v.'+version)

@rumps.clicked(city)
def default_city(sender):
    global city
    global rates_url
    global obm_url
    if city == 'Харьков':
        city = 'Киев' 
        rates_url = kiev_rates
        obm_url = kiev_url
    else: 
        city = 'Харьков'
        rates_url = kharkov_rates
        obm_url = kharkov_url
    city_button.title = city
    update_rates(app,city)

@rumps.clicked("О программе")
def about(sender, _):
    description = ('Программа показывает курсы в статус баре.\n'+
        'Обновление курсов происходит раз в минуту.\n'+
        'Если курс изменился, то он будет окружен зведочками - *курс*\n'+
        'Если курс не удалось получить, то он будет показан так: последний курс**\n'+
        'По умолчанию, город - Харьков, валюта - USD-UAH\n'+
        'Конфигурацию можно изменить в файле config.json\n'+
        'Исходный код: https://github.com/vlakin/obmenka'
        ) 
    rumps.alert(message=description, title='Obmenka Status Bar v.'+version)

@rumps.clicked('Выход')
def clean_up_before_quit(_):
    #print 'execute clean up code'
    rumps.quit_application()

#@rumps.clicked('Test') #fixed bug in rumps lib https://github.com/jaredks/rumps/issues/26
def rate_changed(sender):
    if config['notify']:
        notification_text = "Был: " + str(last_rate) + " стал: " + str(rate)
        rumps.notification("Obmenka", "Изменение курса!", notification_text, sound=config['sound'])


if __name__ == "__main__":
    app = rumps.App("Obmenka Status Bar", title='Obmenka', quit_button=None)
    app.menu = [
        'Курсы валют', 
        'Электронные валюты',
        {'НБУ':
            ['USD-UAH','EUR-UAH','RUB-UAH']},
        {'Межбанк':
            ['USD-UAH','EUR-UAH','RUB-UAH']},
        None,  # None functions as a separator in your menu
        city,
        None,
        'О программе',
        None
    ]
    # -----------------------------------------
    rates_button = app.menu['Курсы валют']
    digital_rates_button = app.menu['Электронные валюты']
    nbu_rates_button = app.menu['НБУ']
    nbu_usd = app.menu['НБУ']['USD-UAH']
    nbu_eur = app.menu['НБУ']['EUR-UAH']
    nbu_rub = app.menu['НБУ']['RUB-UAH']
    mb_rates_button = app.menu['Межбанк']
    mb_usd = app.menu['Межбанк']['USD-UAH']
    mb_eur = app.menu['Межбанк']['EUR-UAH']
    mb_rub = app.menu['Межбанк']['RUB-UAH']
 
    city_button = app.menu[city]
    # -----------------------------------------
    app.run()