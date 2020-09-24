from .mgui_class import MGuiView, MGuiLayout

__KEY_TYPE = "t"
__KEY_ID = "i"
__KEY_CONFIG = "cf"
__KEY_CHILDREN = "cd"
__class_map__ = {}

def register_mgui_component(_class_, name):
    global __class_map__
    if not issubclass(_class_, MGuiView):
        raise Exception("_class_ must be MGuiView`s subclass!")
    __class_map__[name] = _class_
    __class_map__[_class_] = name

def dump_mgui(root):
    if not isinstance(root, MGuiView):
        return None
    root_dict = {}
    root_dict[__KEY_TYPE] = __class_map__[type(root)]
    root_dict[__KEY_ID] = root.vid
    root_dict[__KEY_CONFIG] = root.config
    root_dict[__KEY_CHILDREN] = []
    if isinstance(root, MGuiLayout):
        for view in root.children:
            root_dict[__KEY_CHILDREN].append(dump_mgui(view))
    return root_dict

def load_mgui(root_dict, context):
    if not __KEY_TYPE in root_dict:
        return None
    if not root_dict[__KEY_TYPE] in __class_map__:
        return None
    vid = None
    if __KEY_ID in root_dict:
        vid = root_dict[__KEY_ID]
    root = __class_map__[root_dict[__KEY_TYPE]](context, vid)
    if __KEY_CONFIG in root_dict:
        root.config = root_dict[__KEY_CONFIG]
    if isinstance(root, MGuiLayout) and __KEY_CHILDREN in root_dict:
        for child_dict in root_dict[__KEY_CHILDREN]:
            root.append_child(load_mgui(child_dict, context))
    return root

def __init__():
    register_mgui_component(MGuiView, "MGuiView")
    register_mgui_component(MGuiLayout, "MGuiLayout")
__init__()