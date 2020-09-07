from .mgui_class import MGuiView, MGuiLayout

__KEY_TYPE = "vtype"
__KEY_ID = "vid"
__KEY_CONFIG = "config"
__KEY_CHILDREN = "children"
__class_map__ = {}

def register_mgui_component(_class_):
    global __class_map__
    if not issubclass(_class_, MGuiView):
        raise Exception("_class_ must be MGuiView`s subclass!")
    __class_map__[_class_.__name__] = _class_

def dump_mgui_tree(root):
    if not isinstance(root, MGuiView):
        return None
    root_dict = {}
    root_dict[__KEY_TYPE] = root.__class__.__name__
    root_dict[__KEY_ID] = root.vid
    root_dict[__KEY_CONFIG] = root.config
    root_dict[__KEY_CHILDREN] = []
    if isinstance(root, MGuiLayout):
        for view in root.children:
            root_dict[__KEY_CHILDREN].append(dump_mgui_tree(view))
    return root_dict

def load_mgui_tree(root_dict, context):
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
            root.append_child(load_mgui_tree(child_dict, context))
    return root

def __init__():
    register_mgui_component(MGuiView)
    register_mgui_component(MGuiLayout)
__init__()