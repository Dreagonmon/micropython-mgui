from mgui.mgui_class import MGuiContext
from mgui.mgui_parser import load_mgui_tree, dump_mgui_tree
try:
    import ujson as json
except:
    import json

with open("test.mgj.json", "rb") as f:
    load_tree = json.load(f)
load_mgui = load_mgui_tree(load_tree, MGuiContext())
print()
print(load_mgui)
print()
dump_tree = dump_mgui_tree(load_mgui)
dump_str = json.dumps(dump_tree, indent=2)
print(dump_str)