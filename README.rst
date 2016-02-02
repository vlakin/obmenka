# obmenka
Macos status bar which monitor currency exchange rates on obmenka.kharkov.ua and kiev.obmenka.ua sites 

.. image:: https://raw.github.com/vlakin/obmenka/master/statusbarscreenshot.png

Простой статус бар для пользователей маков, которым интересно мониторить курсы обмена в Харькове и Киеве.
Для написания был использован RUMPS - https://github.com/jaredks/rumps/blob/master/README.rst

Для установки необходимо скачать архив http://vlak.us/~vlak/obmenka/Obmenka-latest.zip , 
распаковать его и переместить в Application. После установки для добавления в автостарт откройте
System Prefences -> User & groups -> Login Items и добавить приложение Obmenka

.. image:: https://raw.github.com/vlakin/obmenka/master/autostart.png

По умолчанию в настройках стоит город Харьков и валюта для мониторинга USD-UAH. Если есть необходимость
изменить эти параметры - они хранятся в файле /Applications/Obmenka.app/Contents/Resources/config.json 


