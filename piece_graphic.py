import pyglet
from pyglet.gl import *
from pyglet.graphics import *
import math

import primitives as pm
import gradient as gr

import backgammon_config as cf

class Piece(object):
    NONE = (0, 0, 0, 0)
    HOVER = cf.PIECE_SELECTOR_HOVER
    SELECTED = cf.PIECE_SELECTOR_SELECTED
    CURRENT = NONE

    hover = False
    selected = False
    selectable = False
    selector = None

    colors = { 'white' :
                        {'shadow_start' : cf.PIECE_WHITE_SHADOW_START_COLOR,
                         'shadow_end' : cf.PIECE_WHITE_SHADOW_END_COLOR,
                         'border' : cf.PIECE_WHITE_BORDER_COLOR,
                         'inner'  : cf.PIECE_WHITE_INNER_COLOR},
               'black' :
                        {'shadow_start' : cf.PIECE_BLACK_SHADOW_START_COLOR,
                         'shadow_end' : cf.PIECE_BLACK_SHADOW_END_COLOR,
                         'border' : cf.PIECE_BLACK_BORDER_COLOR,
                         'inner'  : cf.PIECE_BLACK_INNER_COLOR}}

    def __init__(self, x, y, width, color, selectable):
        self.color = color
        self.selectable = selectable
        self.draw(x, y, width, selectable, True)


    def render(self):
        for part in self.parts:
            part.render()


    def render_effects(self):
        self.shadow.render()


    def render_extras(self):
        if self.selectable:
            self.selector.render()


    def draw(self, x, y, width, selectable, init = False):
        self.x = x
        self.y = y
        self.selectable = selectable
        piece_width = []
        self.piece_shadow_thickness = width * cf.PIECE_SHADOW_THICKNESS
        piece_width.append(width - self.piece_shadow_thickness)
        self.width = piece_width[0]
        piece_shadow = width
        piece_border = piece_width[0] * cf.PIECE_BORDER_THICKNESS
        piece_width.append(piece_width[0] - piece_border * 2)
        piece_width.append(piece_width[0] * cf.PIECE_MIDDLE_THICKNESS)

        color_order = ['border', 'inner', 'border']

        if init:
            self.shadow = gr.CircularGradient(x, y,
                                        self.colors[self.color]['shadow_start'],
                                        self.colors[self.color]['shadow_end'],
                                        piece_width[0] / 2,
                                        piece_shadow / 2)
        else:
            self.shadow.draw(x, y, piece_shadow / 2, piece_width[0] / 2)


        if init:
            self.parts = []
            for i in range(3):
                self.parts.append(pm.Circle(x, y, piece_width[i] / 2,
                                        self.colors[self.color][color_order[i]]))
        else:
            for i in range(3):
                self.parts[i].draw(x, y, piece_width[i] / 2,
                                        self.colors[self.color][color_order[i]])

        self.draw_selector(init)


    def draw_selector(self, init = False):
        if self.selectable:
            start_radius = (self.width * (1 + cf.PIECE_SELECTOR_SPACING)) / 2
            delta_radius = self.width * cf.PIECE_SELECTOR_THICKNESS
            
            if init:
                self.selector = pm.CircleOutline(self.x, self.y, start_radius,
                                                    delta_radius, self.CURRENT)
            else:
                self.selector.draw(self.x, self.y, start_radius, delta_radius,
                                    self.CURRENT)


    def mouse_motion(self, x, y, dx, dy):
        if self.selectable:
            radius = (self.width / 2) ** 2
            dist = (x - self.x) * (x - self.x) + (y - self.y) * (y - self.y)

            if dist < radius:
                if not self.hover:
                    self.hover = True
                    if not self.selected:
                        self.CURRENT = Piece.HOVER
                        self.draw_selector()
            else:
                if self.hover:
                    self.hover = False
                    if not self.selected:
                        self.CURRENT = Piece.NONE
                        self.draw_selector()

            if self.hover: return True
            else: return False
        return False


    def mouse_press_left(self, x, y):
        if self.selectable:
            radius = (self.width / 2) ** 2
            dist = (x - self.x) * (x - self.x) + (y - self.y) * (y - self.y)

            if dist < radius:
                if not self.selected:
                    self.selected = True
                    self.CURRENT = Piece.SELECTED
                    self.draw_selector()
                else:
                    self.selected = False
                    self.CURRENT = Piece.HOVER
                    self.draw_selector()
            else:
                if self.selected:
                    self.selected = False
                    self.CURRENT = Piece.NONE
                    self.draw_selector()

            if self.hover: return True
            else: return False
        return False


if __name__ == '__main__':
    print "Please import me, do not run me directly!"
