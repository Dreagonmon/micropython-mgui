# component module
from mgui.mgui_class import MGuiLayout
from mgui import mgui_const as C
from mgui.mgui_utils import get_center_box, get_config, get_context, get_text_size, get_padding_box, get_flex_children_areas

try:
    from typing import Any, Coroutine, List, Union
    from mgui.mgui_class import MGuiRect, MGuiContext
    from mgui.dev.framebuf import FrameBuffer, Color
except:
    import traceback
    traceback.print_exc()
    pass

class MGuiLinearLayout(MGuiLayout):
    async def render(self, context, frame, area):
        # type: (MGuiContext, FrameBuffer, MGuiRect) -> Coroutine[Any, Any, List[MGuiRect]]
        x, y, w, h = area
        effect_area = []
        bgc = get_config(self.config, C.CONFIG_BG_COLOR, context[C.CONTEXT_BG_COLOR]) # type: Color
        padding = get_config(self.config, C.CONFIG_LAYOUT_PADDING, 0) # type: int
        gap = get_config(self.config, C.CONFIG_LAYOUT_GAP, None) # type: int
        is_hor = get_config(self.config, C.CONFIG_LAYOUT_ORIENTATION, C.CONFIG_VALUE_ORIENTATION_HORIZONTAL)
        is_hor = True if is_hor == C.CONFIG_VALUE_ORIENTATION_HORIZONTAL else False
        area = get_padding_box(area, padding)
        areas = get_flex_children_areas(area, self.children, gap, is_hor)
        if self.is_need_render:
            # clear area
            frame.fill_rect(x, y, w, h, bgc)
        for i in range(len(self.children)):
            if self.is_need_render or self.children[i].need_render(context):
                # draw all, or only draw needed
                effect_area.extend(await self.children[i].render(context, frame, areas[i]))
        if self.is_need_render:
            # update all
            effect_area = [(x, y, w, h)]
        self.is_need_render = False
        return effect_area

class MGuiStackLayout(MGuiLayout):
    async def need_render(self, context: MGuiContext) -> bool:
        if self.is_need_render:
            return True
        return False
