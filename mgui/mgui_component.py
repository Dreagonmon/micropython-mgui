# component module
from mgui.mgui_class import MGuiView
from mgui import mgui_const as C
from mgui.mgui_utils import get_center_box, get_config, get_context, get_text_size

try:
    from typing import Any, Coroutine, List, Union
    from mgui.utils.bmfont import FontDraw
    from mgui.mgui_class import MGuiRect, MGuiContext
    from mgui.dev.framebuf import FrameBuffer, Color
except: pass

class MGuiBlankView(MGuiView):
    async def render(self, context, frame, area):
        # type: (MGuiContext, FrameBuffer, MGuiRect) -> Coroutine[Any, Any, List[MGuiRect]]
        x, y, w, h = area
        effect_area = [area]
        bgc = get_config(self.config, C.CONFIG_BG_COLOR, context[C.CONTEXT_BG_COLOR]) # type: Color
        frame.fill_rect(x, y, w, h, bgc)
        effect_area.extend(await super().render(context, frame, area)) # example using super() function, there will only set self.is_need_render to False.
        return effect_area

class MGuiFilledView(MGuiView):
    async def render(self, context, frame, area):
        # type: (MGuiContext, FrameBuffer, MGuiRect) -> Coroutine[Any, Any, List[MGuiRect]]
        x, y, w, h = area
        effect_area = [area]
        fgc = get_config(self.config, C.CONFIG_FG_COLOR, context[C.CONFIG_FG_COLOR]) # type: Color
        frame.fill_rect(x, y, w, h, fgc)
        effect_area.extend(await super().render(context, frame, area)) # example using super() function, there will only set self.is_need_render to False.
        return effect_area

class MGuiTextView(MGuiView):
    async def render(self, context, frame, area):
        # type: (MGuiContext, FrameBuffer, MGuiRect) -> Coroutine[Any, Any, List[MGuiRect]]
        x, y, w, h = area
        effect_area = [area]
        txt = get_config(self.config, C.CONFIG_TEXT, '') # type: str
        fd = get_context(context, get_config(self.config, C.CONFIG_FONT_NAME, C.CONTEXT_FONT_DRAW_OBJ)) # type: FontDraw
        fgc = get_config(self.config, C.CONFIG_FG_COLOR, context[C.CONTEXT_FG_COLOR]) # type: Color
        bgc = get_config(self.config, C.CONFIG_BG_COLOR, context[C.CONTEXT_BG_COLOR]) # type: Color
        centered = get_config(self.config, C.CONFIG_CENTER_TEXT, False) # type: bool
        frame.fill_rect(x, y, w, h, bgc)
        # center text
        if centered:
            size = get_text_size(txt, fd.get_font_size(), w)
            x, y, w, h = get_center_box(area, size)
        fd.draw_on_frame(txt, frame, x, y, fgc, w, h)
        effect_area.extend(await super().render(context, frame, area)) # example using super() function, there will only set self.is_need_render to False.
        return effect_area

class MGuiProgressView(MGuiView):
    def __init__(self, context, vid=None):
        super().__init__(context, vid)
        self.animation = 0

    def need_render(self, context) -> bool:
        # type: (MGuiContext) -> bool
        return True

    async def render(self, context, frame, area):
        # type: (MGuiContext, FrameBuffer, MGuiRect) -> Coroutine[Any, Any, List[MGuiRect]]
        x, y, w, h = area
        effect_area = [area]
        fgc = get_config(self.config, C.CONFIG_FG_COLOR, context[C.CONTEXT_FG_COLOR]) # type: Color
        bgc = get_config(self.config, C.CONFIG_BG_COLOR, context[C.CONTEXT_BG_COLOR]) # type: Color
        pc = get_config(self.config, C.CONFIG_PROGRESS_VALUE, -1) # float
        frame.fill_rect(x, y, w, h, bgc)
        offset = self.animation * w
        if pc < 0:
            # inf loop
            # display 8 block
            block_w = w // 8
            for p in range(16):
                start_x = int(w * ((p - 8) / 8) + offset)
                if p % 2 == 0 or start_x + block_w < 0 or start_x > w:
                    continue
                tmp_w = block_w
                if start_x < 0:
                    tmp_w += start_x
                    start_x = 0
                if start_x + tmp_w > w:
                    tmp_w = w - start_x
                frame.fill_rect(x + start_x, y, tmp_w, h, fgc)
        else:
            block_w = w * pc
            final_x = offset + block_w
            p1_w = int(block_w) if final_x < w else int(w - offset) # first part
            p2_w = 0 if final_x < w else int(final_x - w) # oversize part
            frame.fill_rect(int(x + offset), y, p1_w, h, fgc)
            frame.fill_rect(x, y, p2_w, h, fgc)
            # print(p1_w, p2_w)
        self.animation += context[C.CONTEXT_FRAME_DURATION] / 10000 # moving 10% / s
        self.animation = 0 if self.animation > 1.0 else self.animation
        # effect_area.extend(await super().render(context, frame, area)) # let self.is_need_render keep True
        return effect_area
