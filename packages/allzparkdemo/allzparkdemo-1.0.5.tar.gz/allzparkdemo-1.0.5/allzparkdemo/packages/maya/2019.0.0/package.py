# -*- coding: utf-8 -*-

name = 'maya'

version = '2019.0.0'

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

timestamp = 1564154701

_data = \
    {'color': '#251',
     'icon': '{root}/resources/icon_{width}x{height}.png',
     'label': 'Autodesk Maya'}

format_version = 2
