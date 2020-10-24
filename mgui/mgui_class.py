# class module

# ======== Utils Class ========
class MGuiRect(object):
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class MGuiEvent(object):
    def __init__(self, event_type=0, event_data=None):
        self.event_type = event_type # Event Type
        self.event_data = event_data # Event Data

class MGuiContext(dict):
    pass

# ======== Core Class ========
class MGuiView(object):
    def __init__(self, context, vid=None):
        self.__parent = None
        # configure property
        self.vid = vid
        self.config = {}
        # runtime property
        self.context = context
        self.is_need_render = True
        pass
    def _set_parent(self, parent):
        self.__parent = parent
    def get_parent(self):
        return self.__parent
    def update_config(self, new_config):
        ''' used when change config '''
        self.config = new_config
        self.is_need_render = True
    def find_view_by_vid(self, vid:str):
        ''' check for vid. If equal, return self. Otherwise return None '''
        if self.vid != None and self.vid == vid:
            return self
        return None
    def need_render(self, context):
        ''' check if view need render '''
        return self.is_need_render
    def render(self, context, frame, area):
        ''' render on framebuf in area. return effected area list'''
        self.is_need_render = False
        return []
    def on_event(self, context, event):
        ''' event handler, when handled, return True if the event has been processed '''
        return False

class MGuiLayout(MGuiView):
    def __init__(self, context, vid=None):
        super().__init__(context, vid)
        self.children = []
        pass
    def append_child(self, view):
        if not isinstance(view, MGuiView):
            return # type check
        view._set_parent(self)
        self.children.append(view)
        self.is_need_render = True
    def remove_child(self, index):
        if index >= 0 and index < len(self.children):
            self.children[index]._set_parent(None)
            del self.children[index]
            self.is_need_render = True
    def index_child(self, view_or_vid):
        count = len(self.children)
        if isinstance(view_or_vid, MGuiView):
            for i in range(count):
                if view_or_vid == self.children[i]:
                    return i
        elif isinstance(view_or_vid, str):
            for i in range(count):
                if view_or_vid == self.children[i].vid:
                    return i
        return -1
    # override
    def find_view_by_vid(self, vid):
        ''' search for vid. If found, return view object. Otherwise return None '''
        if self.vid != None and self.vid == vid:
            return self
        for view in self.children:
            find = view.find_view_by_vid(vid)
            if find != None:
                return find
        return None
    def need_render(self, context):
        ''' check if view need render '''
        if self.is_need_render:
            return True
        for view in self.children:
            if (view.need_render(context)):
                return True
        return False
    def render(self, context, frame, area):
        effect_area = []
        # example, just render it all
        for view in self.children:
            effect_area.extend(view.render(context, frame, area))
        self.is_need_render = False
        return effect_area
    def on_event(self, context, event):
        if not isinstance(event, MGuiEvent):
            return False
        for view in self.children:
            if view.on_event(context, event):
                return True
        # default return super() method
        return super().on_event(context, event)
