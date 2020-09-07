CONFIG_LAYOUT_WIDTH = "l_width"
CONFIG_LAYOUT_HEIGHT = "l_height"
CONFIG_LAYOUT_WEIGHT = "l_weight"
CONFIG_LAYOUT_MARGIN_UP = "lm_up"
CONFIG_LAYOUT_MARGIN_DOWN = "lm_down"
CONFIG_LAYOUT_MARGIN_LEFT = "lm_left"
CONFIG_LAYOUT_MARGIN_RIGHT = "lm_right"
CONFIG_PADDING_UP = "p_up"
CONFIG_PADDING_DOWN = "p_down"
CONFIG_PADDING_LEFT = "p_left"
CONFIG_PADDING_RIGHT = "p_right"
# context field
CONTEXT_FOCUS = "focus"
CONTEXT_EFFECT_AREAS = "effect_areas"
CONTEXT_BG_COLOR = "bg_color"
CONTEXT_FG_COLOR = "fg_color"
# if View can be focused, trigger blur event on last one, set self to the context['focus'], and return True, otherwise return False
EVENT_ON_FOCUS = "ev_on_focus"
# ignore return value, just a callback
EVENT_ON_BLUR = "ev_on_blur"
# NAV event are for layout only. when nav success (a view focused), return True.
EVENT_NAV_UP = "ev_nav_up"
EVENT_NAV_DOWN = "ev_nav_down"
EVENT_NAV_LEFT = "ev_nav_left"
EVENT_NAV_RIGHT = "ev_nav_right"