from mgui.mgui_const import CONTEXT_BG_COLOR, CONTEXT_FG_COLOR, CONTEXT_FRAME_RATE
from .mgui_class import MGuiContext
class MGuiRoot(object):
    def __init__(self, context=None):
        self.__context = MGuiContext()
        self.__context[CONTEXT_BG_COLOR] = 0 # type Color
        self.__context[CONTEXT_FG_COLOR] = 1 # type Color
        self.__context[CONTEXT_FRAME_RATE] = 15 # type integer
        if context != None:
            for k in context.keys():
                self.__context[k] = context[k]
    def get_context(self):
        return self.__context