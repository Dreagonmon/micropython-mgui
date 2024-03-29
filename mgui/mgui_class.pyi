from typing import Any, Dict, Optional, List, Tuple, Union, Callable
from .dev import framebuf

# mgui class
MGuiRect = Tuple[int, int, int, int] # x, y, w, h
MGuiEvent = Tuple[int, Any]
MGuiContext = Dict[str, Any]
EventHandler = Union[None, Callable[[MGuiView, MGuiContext, MGuiEvent], bool]]

class MGuiView(object):
    __parent: MGuiView
    vid: Optional[str]
    config: dict
    context: MGuiContext
    event_handler: EventHandler
    is_need_render: bool
    def __init__(self, context: Optional[MGuiContext], vid: str = ...) -> None: ...
    def _set_parent(self, parent: Optional[MGuiView]) -> None: ...
    def get_parent(self) -> Optional[MGuiView]: ...
    def set_event_handler(self, handler: EventHandler) -> None: ...
    def update_config(self, new_config: dict) -> None: ...
    def find_view_by_vid(self, vid: str) -> Optional[MGuiView]: ...
    def need_render(self, context: MGuiContext) -> bool: ...
    async def render(self, context: MGuiContext, frame: framebuf.FrameBuffer, area: MGuiRect) -> List[MGuiRect]:...
    async def on_event(self, context: MGuiContext, event: MGuiEvent) -> bool: ...

class MGuiLayout(MGuiView):
    children: List[MGuiView]
    def append_child(self, view: Optional[MGuiView]) -> None: ...
    def remove_child(self, index: int) -> None: ...
    def index_child(self, view_or_vid: Union[MGuiView, str]) -> int: ...

class MGuiScreen(object):
    def get_size(self) -> Tuple[int, int]: ...
    def get_framebuffer(self) -> framebuf.FrameBuffer: ...
    async def refresh(self, context: MGuiContext, effect_area: List[MGuiRect]) -> None: ...
