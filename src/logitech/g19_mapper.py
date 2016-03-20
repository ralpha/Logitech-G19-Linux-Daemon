from g19_receivers import G19Receiver
from logitech.g19 import *
from logitech.g19_keys import Key
from logitech.g19_receivers import *

import virtkey

class G19Mapper():
    def __init__(self, lg19):
        self.__lg19 = lg19
        self.__inputProcessor = MapperInputProcessor(self)
     
    def get_input_processor(self):
        return self.__inputProcessor    
    

class MapperInputProcessor(InputProcessor):
    '''Map the keys to the functions'''

    def __init__(self, mapper):
        self.__mapper = mapper
        self.__virtkey = virtkey.virtkey()


    def process_input(self, inputEvent):
        processed = False
        if Key.PLAY in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(172)
                self.__virtkey.release_keycode(172)
            finally:
                processed = True

        if Key.NEXT in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(171)
                self.__virtkey.release_keycode(171)
            finally:
                processed = True
            
        if Key.PREV in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(173)
                self.__virtkey.release_keycode(173)
            finally:
                processed = True
            
        if Key.STOP in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(174)
                self.__virtkey.release_keycode(174)
            finally:
                processed = True
            
        if Key.MUTE in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(121)
                self.__virtkey.release_keycode(121)
            finally:
                processed = True
            
        if Key.SCROLL_UP in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(123)
                self.__virtkey.release_keycode(123)
            finally:
                processed = True
            
        if Key.SCROLL_DOWN in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(122)
                self.__virtkey.release_keycode(122)
            finally:
                processed = True
            
        if Key.G01 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(247)
                self.__virtkey.release_keycode(247)
            finally:
                processed = True
            
        if Key.G02 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(248)
                self.__virtkey.release_keycode(248)
            finally:
                processed = True
            
        if Key.G03 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(194)
                self.__virtkey.release_keycode(194)
            finally:
                processed = True
            
        if Key.G04 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(198)
                self.__virtkey.release_keycode(198)
            finally:
                processed = True
            
        if Key.G05 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(195)
                self.__virtkey.release_keycode(195)
            finally:
                processed = True
            
        if Key.G06 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(196)
                self.__virtkey.release_keycode(196)
            finally:
                processed = True
            
        if Key.G07 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(197)
                self.__virtkey.release_keycode(197)
            finally:
                processed = True
            
        if Key.G08 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(254)
                self.__virtkey.release_keycode(254)
            finally:
                processed = True
            
        if Key.G09 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(255)
                self.__virtkey.release_keycode(255)
            finally:
                processed = True
            
        if Key.G10 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(230)
                self.__virtkey.release_keycode(230)
            finally:
                processed = True
            
        if Key.G11 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(228)
                self.__virtkey.release_keycode(228)
            finally:
                processed = True
            
        if Key.G12 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(226)
                self.__virtkey.release_keycode(226)
            finally:
                processed = True
        