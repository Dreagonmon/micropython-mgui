from mgui.mgui_const import CONTEXT_BG_COLOR, CONTEXT_EFFECT_AREAS, CONTEXT_FG_COLOR, CONTEXT_FOCUS
from .mgui_class import MGuiContext
class MGuiRoot(object):
    def __init__(self):
        self.__context = MGuiContext()
        self.__context[CONTEXT_FOCUS] = None # type Optional[MGuiView]
        self.__context[CONTEXT_EFFECT_AREAS] = [] # type List[MGuiRect]
        self.__context[CONTEXT_BG_COLOR] = 0 # type Color
        self.__context[CONTEXT_FG_COLOR] = 1 # type Color
    def get_context(self):
        return self.__context