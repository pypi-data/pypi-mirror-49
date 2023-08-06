# -*- coding: utf-8 -*-

name = 'texteditor'

version = '2.1.1'

tools = ['texteditor']

requires = []

private_build_requires = ['rezutil-1']

def commands():
    global env
    
    env.PATH.append("{root}/bin")

timestamp = 1564124563

_data = {'icon': '{root}/resources/icon_128.png', 'label': 'Text Editor'}

format_version = 2
