from PIL import Image, ImageDraw
from . import framebuf

def showFrameBuffer(buffer, width:int, height:int, format:int, scale=4):
    if format == framebuf.RGB565:
        img = Image.frombytes("I;16", (width, height), bytes(buffer))
    elif format == framebuf.MONO_HLSB:
        img = Image.frombytes("1", (width, height), bytes(buffer))
    elif format == framebuf.MONO_HMSB or format == framebuf.MONO_VLSB or format == framebuf.MONO_VMSB:
        img = Image.new("1", (width, height), 0)
        draw = ImageDraw.Draw(img)
        fbuf = framebuf.FrameBuffer(buffer, width, height, format)
        for y in range(height):
            for x in range(width):
                color = fbuf.pixel(x, y)
                draw.point([x,y], fill=color)
    else:
        img = Image.new("L", (width, height), 0)
    img = img.resize((width*scale, height*scale), Image.NEAREST)
    img.show()
    pass