from mgui import mgui_const as C
from mgui.mgui_utils import get_context
from mgui.utils.bmfont import FontDrawAscii
try:
    import uasyncio as asyncio
    from utime import ticks_ms as time_ms
    from usys import print_exception
    is_debug = False
except:
    import asyncio
    from time import time_ns as _time_ns
    def time_ms():
        return _time_ns() // 1_000_000
    from traceback import print_exc as _p_e
    def print_exception(*args, **kws):
        _p_e()
    is_debug = True
# useless import for type hints
try:
    from typing import NoReturn, Coroutine, Any, Optional
    from mgui.mgui_class import MGuiView, MGuiScreen, MGuiContext, MGuiEvent
    from mgui.dev.framebuf import Color
    from mgui.utils.bmfont import FontDraw
except: pass

class MGuiRoot(object):
    def __init__(self, context=None):
        # type: (Optional[MGuiContext]) -> None
        if context == None:
            context = dict()
        context[C.CONTEXT_BG_COLOR] = get_context(context, C.CONTEXT_BG_COLOR, 0) # type Color
        context[C.CONTEXT_FG_COLOR] = get_context(context, C.CONTEXT_FG_COLOR, 1) # type Color
        context[C.CONTEXT_FRAME_RATE] = get_context(context, C.CONTEXT_FRAME_RATE, 15) # type int
        context[C.CONTEXT_FRAME_DURATION] = get_context(context, C.CONTEXT_FRAME_DURATION, 1) # type int
        context[C.CONTEXT_FONT_DRAW_OBJ] = get_context(context, C.CONTEXT_FONT_DRAW_OBJ, FontDrawAscii()) # type FontDraw
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
        self.__context[C.CONTEXT_ROOT] = self
        self.__context[C.CONTEXT_ROOT_VIEW] = root_view
        try:
            s_w, s_h = screen.get_size()
            frame = screen.get_framebuffer()
            lasttime = time_ms()
            target_duration = 1000 // self.__context[C.CONTEXT_FRAME_RATE]
            while self.__running:
                now = time_ms()
                if now - lasttime < target_duration:
                    await asyncio.sleep(0.0)
                    continue
                self.__context[C.CONTEXT_FRAME_DURATION] = now - lasttime
                lasttime = now
                # print(self.__context[CONTEXT_FRAME_DURATION])
                try:
                    if root_view.need_render(self.__context):
                        effect_area = await root_view.render(self.__context, frame, (0, 0, s_w, s_h))
                        await screen.refresh(self.__context, effect_area)
                except Exception as e:
                    print_exception(e)
                    if is_debug:
                        self.stop()
                        break
        except KeyboardInterrupt:
            # print("Abort.")
            self.stop()
            pass

    def send_event(self, event):
        # type: (MGuiEvent) -> bool
        view = get_context(self.__context, C.CONTEXT_ROOT_VIEW, None)
        if not isinstance(view, MGuiView):
            return False
        else:
            return view.on_event(self.__context, event)
