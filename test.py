from mgui.dev import framebuf
from mgui.mgui_class import MGuiContext
from mgui.mgui_parser import load_mgui, dump_mgui
try:
    import ujson as json
except:
    import json

with open("test.mgj.json", "rb") as f:
    load_tree = json.load(f)
load_mgui = load_mgui(load_tree, MGuiContext())
lv2v1 = load_mgui.find_view_by_vid("lv2view1")
print()
print(lv2v1)
print(lv2v1.config)
print()
dump_tree = dump_mgui(load_mgui)
dump_str = json.dumps(dump_tree, indent=2)
# print(dump_str)

import mgui.dev.framebuf as framebuf

buf = bytearray(16*8*2)
frame = framebuf.FrameBuffer(buf,16,8,framebuf.MONO_VMSB)
frame.pixel(0,0,65535)
frame.pixel(0,7,65535)
frame.pixel(15,0,65535)
frame.pixel(15,7,65535)
frame.rect(1,1,14,6,65535)
frame.line(0,7,15,0,65535)
frame.line(0,0,15,7,65535)
print(frame)
