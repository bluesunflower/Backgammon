import pyglet

import primitives as pm
import gradient as gr

import menu_graphic_config as cf


class Menu(object):
    offset_x = {}
    offset_y = {}
    temp_width = {}
    temp_height = {}

    def __init__(self, width, height):
        self.draw(width, height, True)


    def mouse_motion(self, x, y, dx, dy):
        return False


    def mouse_press_left(self, x, y):
        return False


    def render(self):
        self.background.render()
        self.menu_border.render()
        self.content_bg.render()
        self.title.draw()
        self.subtitle.draw()


    def draw(self, w, h, init = False):
        self.width = w
        self.height = h
        self.resize()

        self.draw_canvas(init)
        self.draw_border(init)
        self.draw_content_bg(init)
        self.draw_title(init)


    def resize(self):
        temp_width = self.width - cf.BORDER_THICKNESS * 2
        temp_height = temp_width * cf.RELATIVE_HEIGHT / cf.RELATIVE_WIDTH
        if temp_height > self.height:
            temp_height = self.height - cf.BORDER_THICKNESS * 2
            temp_width = temp_height * cf.RELATIVE_WIDTH / cf.RELATIVE_HEIGHT

        self.menu_width = temp_width
        self.menu_height = temp_height


    def draw_canvas(self, init = False):
        if init:
            self.background = pm.Rect(0, 0, self.width, self.height, cf.BG_COLOR)
        else:
            self.background.draw(0, 0, self.width, self.height, cf.BG_COLOR)


    def draw_border(self, init = False):
        self.offset_x['global'] = (self.width - self.menu_width) / 2
        self.offset_y['global'] = (self.height - self.menu_height) / 2
        self.global_border_width = (self.menu_width * cf.MENU_BORDER_THICKNESS)

        if init:
            self.menu_border = pm.Rect(self.offset_x['global'],
                                        self.offset_y['global'],
                                        self.menu_width,
                                        self.menu_height,
                                        cf.MENU_BORDER_COLOR)
        else:
            self.menu_border.draw(self.offset_x['global'],
                                    self.offset_y['global'],
                                    self.menu_width,
                                    self.menu_height,
                                    cf.MENU_BORDER_COLOR)

    def draw_content_bg(self, init = False):
        self.offset_x['content_bg'] = (self.offset_x['global'] + self.global_border_width)
        self.offset_y['content_bg'] = (self.offset_y['global'] + self.global_border_width)
        self.temp_width['content_bg'] = self.menu_width - self.global_border_width * 2
        self.temp_height['content_bg'] = self.menu_height - self.global_border_width * 2

        if init:
            self.content_bg = gr.BandGradient(self.offset_x['content_bg'],
                                                self.offset_y['content_bg'],
                                                self.temp_width['content_bg'],
                                                self.temp_height['content_bg'],
                                                cf.MENU_BG_START_COLOR,
                                                cf.MENU_BG_END_COLOR)
        else:
            self.content_bg.draw(self.offset_x['content_bg'],
                                    self.offset_y['content_bg'],
                                    self.temp_width['content_bg'],
                                    self.temp_height['content_bg'])

    def draw_title(self, init = False):
        self.offset_x['title'] = (self.width / 2)
        self.offset_y['title'] = (self.offset_y['content_bg'] + self.temp_height['content_bg'] * (1 - cf.TITLE_TOP_SPACER))
        title_size = self.temp_height['content_bg'] * cf.TITLE_PROPORTION

        self.offset_x['subtitle'] = (self.width / 2 + self.temp_width['content_bg'] * cf.SUBTITLE_OFFSET)
        self.offset_y['subtitle'] = (self.offset_y['title'] - title_size - self.temp_height['content_bg'] * cf.SUBTITLE_TOP_SPACER)
        subtitle_size = self.temp_height['content_bg'] * cf.SUBTITLE_PROPORTION

        self.title = pyglet.text.Label(cf.TITLE_TEXT, font_name = cf.TITLE_FONT,
                                        font_size = title_size, bold = True,
                                        color = cf.TITLE_COLOR,
                                        x = self.offset_x['title'],
                                        y = self.offset_y['title'],
                                        anchor_x = 'center', anchor_y = 'top')

        self.subtitle = pyglet.text.Label(cf.SUBTITLE_TEXT, font_name = cf.SUBTITLE_FONT,
                                        font_size = subtitle_size, bold = True,
                                        color = cf.SUBTITLE_COLOR,
                                        x = self.offset_x['subtitle'],
                                        y = self.offset_y['subtitle'],
                                        anchor_x = 'center', anchor_y = 'top')

if __name__ == '__main__':
    "Please do not run this file directly, include it."