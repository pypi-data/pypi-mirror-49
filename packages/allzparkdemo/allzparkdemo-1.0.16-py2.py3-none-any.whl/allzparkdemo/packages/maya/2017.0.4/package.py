# -*- coding: utf-8 -*-

name = 'maya'

version = '2017.0.4'

tools = [
    'maya',
    'mayapy',
    'render',
    'mayabatch',
    'mayagui_lic'
]

requires = []

private_build_requires = ['rezutil-1']

def commands():
    global env
    global alias
    global system
    
    env.PATH.prepend("{root}/bin")

timestamp = 1564387502

_data = \
    {'color': '#251',
     'icon': '{root}/resources/icon_256x256.png',
     'label': 'Autodesk Maya'}

format_version = 2
