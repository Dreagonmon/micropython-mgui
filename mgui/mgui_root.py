from mgui.mgui_const import CONTEXT_BG_COLOR, CONTEXT_FG_COLOR, CONTEXT_FRAME_RATE, CONTEXT_FRAME_DURATION, CONTEXT_FONT_DRAW_OBJ
from mgui.utils.bmfont import FontDrawAscii
try:
    import uasyncio as asyncio
    from utime import ticks_ms as time_ms
    from usys import print_exception
except:
    import asyncio
    from time import time_ns as _time_ns
    def time_ms():
        return _time_ns() // 1_000_000
    from traceback import print_exc as _p_e
    def print_exception(*args, **kws):
        _p_e()
# useless import for type hints
try:
    from typing import NoReturn, Coroutine, Any, Optional
    from mgui.mgui_class import MGuiView, MGuiScreen, MGuiContext
    from mgui.dev.framebuf import Color
    from mgui.utils.bmfont import FontDraw
except: pass

class MGuiRoot(object):
    def __init__(self, context=None):
        # type: (Optional[MGuiContext]) -> None
        if context == None:
            context = dict()
        context[CONTEXT_BG_COLOR] = context[CONTEXT_BG_COLOR] if CONTEXT_BG_COLOR in context else 0 # type Color
        context[CONTEXT_FG_COLOR] = context[CONTEXT_FG_COLOR] if CONTEXT_FG_COLOR in context else 1 # type Color
        context[CONTEXT_FRAME_RATE] = context[CONTEXT_FRAME_RATE] if CONTEXT_FRAME_RATE in context else 15 # type int
        context[CONTEXT_FRAME_DURATION] = context[CONTEXT_FRAME_DURATION] if CONTEXT_FRAME_DURATION in context else 1 # type int
        context[CONTEXT_FONT_DRAW_OBJ] = context[CONTEXT_FONT_DRAW_OBJ] if CONTEXT_FONT_DRAW_OBJ in context else FontDrawAscii() # type FontDraw
        self.__context = context
        self.__running = False

    def get_context(self):
        return self.__context

    def mainloop(self, root_view, screen):
        loop = asyncio.get_event_loop()
        if loop == None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        self.__running = True
        loop.create_task(self.render_loop(root_view, screen))
        loop.run_forever()

    def stop(self):
        self.__running = False
        loop = asyncio.get_event_loop()
        if loop != None:
            loop.stop()

    async def render_loop(self, root_view, screen):
        # type: (MGuiView, MGuiScreen) -> Coroutine[Any, Any, NoReturn]
        try:
            s_w, s_h = screen.get_size()
            frame = screen.get_framebuffer()
            lasttime = time_ms()
            target_duration = 1000 // self.__context[CONTEXT_FRAME_RATE]
            while self.__running:
                now = time_ms()
                if now - lasttime < target_duration:
                    await asyncio.sleep(0.0)
                    continue
                self.__context[CONTEXT_FRAME_DURATION] = now - lasttime
                lasttime = now
                # print(self.__context[CONTEXT_FRAME_DURATION])
                try:
                    if root_view.need_render(self.__context):
                        effect_area = await root_view.render(self.__context, frame, (0, 0, s_w, s_h))
                        await screen.refresh(self.__context, effect_area)
                except Exception as e:
                    print_exception(e)
        except KeyboardInterrupt:
            # print("Abort.")
            self.stop()
            pass
