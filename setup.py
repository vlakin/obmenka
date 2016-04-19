# -*- coding: utf-8 -*-
from setuptools import setup

APP = ['obmenka.py']
APP_NAME = "Obmenka"
DATA_FILES = ['config.json', 'obmenka.icns']
OPTIONS = {
    'argv_emulation': True,
    'iconfile':'obmenka.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Obmenka Status Bar",
        'CFBundleIdentifier': "com.metachris.osx.obmenka",
        'CFBundleVersion': "0.1.3",
        'CFBundleShortVersionString': "0.1.3",
        'NSHumanReadableCopyright': u"Copyright © 2016, Vlak"
    },
    'packages': ['rumps'],
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
