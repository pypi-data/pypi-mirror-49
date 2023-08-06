# -*- coding: utf-8 -*-

name = 'dev_maya2'

version = '2018.1.0'

tools = [
    'maya',
    'mayapy',
    'render',
    'mayabatch'
]

requires = []

private_build_requires = ['rezutil-1']

def commands():
    global env
    env.PATH.prepend("{root}/bin")

timestamp = 1564387504

_data = \
    {'color': '#251',
     'hidden': True,
     'icon': '{root}/resources/icon_{width}x{height}.png',
     'label': 'Autodesk Maya'}

format_version = 2
