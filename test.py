try:
    import ujson as json
    import uasyncio as asyncio
except:
    import json
    import asyncio

if __name__ == "__main__":
    from mgui.dev.ssd1306pygame import SSD1306_Emu
    from mgui.mgui_class import MGuiScreen
    from mgui.mgui_root import MGuiRoot
    from mgui.mgui_component import MGuiTextView, MGuiBlankView, MGuiFilledView, MGuiProgressView
    from mgui.mgui_layout import MGuiLinearLayout
    from mgui import mgui_const as C
    class SSD1306Screen(MGuiScreen):
        def __init__(self, ssd1306):
            self._screen = ssd1306
        async def refresh(self, context, effect_area):
            self._screen.show()
        def get_framebuffer(self):
            return self._screen
        def get_size(self):
            return self._screen.width, self._screen.height
    ssd1306 = SSD1306_Emu(128, 64)
    screen = SSD1306Screen(ssd1306)
    root = MGuiRoot()
    context = root.get_context()
    context[C.CONTEXT_FRAME_RATE] = 15
    # [test]
    filled_view = MGuiFilledView(context)
    blank_view = MGuiBlankView(context)
    text_view = MGuiTextView(context)
    text_view.update_config({
        C.CONFIG_FG_COLOR: 0,
        C.CONFIG_BG_COLOR: 1,
        C.CONFIG_TEXT: 'Dragon',
        C.CONFIG_CENTER_TEXT: True,
        C.CONFIG_LAYOUT_WIDTH: 48,
    })
    progress_view = MGuiProgressView(context)
    progress_view.update_config({
        C.CONFIG_PROGRESS_VALUE: -1,
        C.CONFIG_LAYOUT_HEIGHT: 4,
    })
    linear_layout = MGuiLinearLayout(context)
    linear_layout.update_config({
        C.CONFIG_LAYOUT_ORIENTATION: C.CONFIG_VALUE_ORIENTATION_VERTICAL,
        C.CONFIG_LAYOUT_PADDING: 4,
        C.CONFIG_LAYOUT_GAP: 4,
    })
    linear_layout2 = MGuiLinearLayout(context)
    linear_layout2.update_config({
        C.CONFIG_LAYOUT_ORIENTATION: C.CONFIG_VALUE_ORIENTATION_HORIZONTAL,
        C.CONFIG_LAYOUT_GAP: 4,
    })
    linear_layout2.append_child(filled_view)
    linear_layout2.append_child(text_view)
    linear_layout2.append_child(filled_view)
    linear_layout.append_child(progress_view)
    linear_layout.append_child(text_view)
    linear_layout.append_child(linear_layout2)
    linear_layout.append_child(filled_view)
    linear_layout.append_child(progress_view)
    root.mainloop(linear_layout, screen)
    print("\n\n\n\n")
    from mgui.mgui_parser import dump_mgui
    tree = dump_mgui(linear_layout)
    js = json.dumps(tree, indent=2)
    print(js)
