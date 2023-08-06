# Author: Patan Musthakheem
# Version: 1.0
# Licence: Apache 2.0
import os
import sys


class Colors:
    __doc__ = r"""I Have Also made similar project for linux with name python-colors-linux
                 which also supply colors to beautify your output since it doesn't support
                 windows i have re-created the project for Supporting the Windows
                 But the disadvantage is we want to change the whole terminal color temporary
                 since the Program runs and every color is defined as a function!"""
    __author__ = 'Patan Musthakheem Khan'
    __version__ = 1.0
    if sys.platform != 'win32':
        print("[-] This Package Is for Windows.")
        print("[-] Please Use Python-colors-linux for Linux (OR) Mac")
        sys.exit(1)

    available_colors = ['RESET', 'BLUE', 'GREEN', 'AQUA', 'RED', 'PURPLE', 'YELLOW', 'WHITE', 'GRAY', 'LI_BLUE',
                        'LI_GREEN', 'LI_AQUA', 'LI_RED', 'LI_PURPLE', 'LI_YELLOW', 'BR_WHITE']

    def __init__(self):
        self.Color_Dict = {
            'RESET': 'COLOR',
            'BLUE': 'COLOR 1',
            'GREEN': 'COLOR 2',
            'AQUA': 'COLOR 3',
            'RED': 'COLOR 4',
            'PURPLE': 'COLOR 5',
            'YELLOW': 'COLOR 6',
            'WHITE': 'COLOR 7',
            'GRAY': 'COLOR 8',
            'LI_BLUE': 'COLOR 9',
            'LI_GREEN': 'COLOR A',
            'LI_AQUA': 'COLOR B',
            'LI_RED': 'COLOR C',
            'LI_PURPLE': 'COLOR D',
            'LI_YELLOW': 'COLOR E',
            "BR_WHITE": 'COLOR F'
        }

    def reset(self):
        os.system(self.Color_Dict.get('RESET'))

    def blue(self):
        os.system(self.Color_Dict.get('BLUE'))

    def green(self):
        os.system(self.Color_Dict.get('GREEN'))

    def aqua(self):
        os.system(self.Color_Dict.get('AQUA'))

    def red(self):
        os.system(self.Color_Dict.get('RED'))

    def purple(self):
        os.system(self.Color_Dict.get('PURPLE'))

    def yellow(self):
        os.system(self.Color_Dict.get('YELLOW'))

    def white(self):
        os.system(self.Color_Dict.get('WHITE'))

    def gray(self):
        os.system(self.Color_Dict.get('GRAY'))

    def light_blue(self):
        os.system(self.Color_Dict.get('LI_BLUE'))

    def light_green(self):
        os.system(self.Color_Dict.get('LI_GREEN'))

    def light_aqua(self):
        os.system(self.Color_Dict.get('LI_AQUA'))

    def light_red(self):
        os.system(self.Color_Dict.get('LI_RED'))

    def light_purple(self):
        os.system(self.Color_Dict.get('LI_PURPLE'))

    def light_yellow(self):
        os.system(self.Color_Dict.get('LI_YELLOW'))
