MONO_VLSB = 0
MONO_VMSB = 7
RGB565 = 1
GS2_HMSB = 5
GS4_HMSB = 2
GS8 = 6
MONO_HLSB = 3
MONO_HMSB = 4
class FrameBuffer(object):
    def __init__(self, buffer, width, height, format, stride = None): pass
    def fill(self, c): pass
    def pixel(self, x, y, c=None): pass
    def hline(self, x, y, w, c): pass
    def vline(self, x, y, h, c): pass
    def line(self, x1, y1, x2, y2, c): pass
    def rect(self, x, y, w, h, c): pass
    def fill_rect(self, x, y, w, h, c): pass
    def text(self, s: str, x, y, c=0): pass
    def scroll(self, xstep, ystep): pass
    def blit(self, fbuf, x, y, key=None): pass