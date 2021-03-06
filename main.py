import pyglet
from pyglet.gl import *

import backgammon_config as cf
import table_graphic
import menu_graphic
import board
import statistic as st

class BackgammonWindow(pyglet.window.Window):
    def __init__(self, config):
        super(BackgammonWindow, self).__init__(resizable=True, config=config)
        self.set_minimum_size(cf.RELATIVE_WIDTH/2, cf.RELATIVE_HEIGHT/2)
        self.set_size(cf.RELATIVE_WIDTH + cf.BORDER_THICKNESS * 2,
                      cf.RELATIVE_HEIGHT + cf.BORDER_THICKNESS * 2)
        self.set_caption('Backgammon')

        self.cursor_hand = self.get_system_mouse_cursor(self.CURSOR_HAND)
        self.cursor_default = self.get_system_mouse_cursor(self.CURSOR_DEFAULT)

        self.BOARD = board.Board()
        self.STATISTIC = st.Statistic()
        self.GAME_TABLE = table_graphic.Table(self.width, self.height,
                                                self.BOARD, self.STATISTIC)
        self.MENU = menu_graphic.Menu(self.width, self.height, self.STATISTIC)

        #self.CURRENT_SCREEN = self.GAME_TABLE
        self.CURRENT_SCREEN = self.MENU


    def on_draw(self):
        self.clear()
        self.CURRENT_SCREEN.render()


    def on_resize(self, width, height):
        super(BackgammonWindow, self).on_resize(width, height)
        self.CURRENT_SCREEN.draw(w = width, h = height)


    def on_mouse_motion(self, x, y, dx, dy):
        if self.CURRENT_SCREEN.mouse_motion(x, y, dx, dy):
            self.set_mouse_cursor(self.cursor_hand)
        else:
            self.set_mouse_cursor(self.cursor_default)


    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.CURRENT_SCREEN.mouse_press_left(x, y)


    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            if self.CURRENT_SCREEN.mouse_release_left(x, y):
                self.close()


if __name__ == '__main__':
    try:
        config = Config(alpha_size = 8, sample_buffers = 1, samples = 4,
                        depth_size = 0, double_buffer = True)
        window = BackgammonWindow(config)
    except pyglet.window.NoSuchConfigException:
        print "Smooth contex could not be aquired."
        window = BackgammonWindow(None)

    pyglet.app.run()
