# ---- config keys ----
# > layout config.
CONFIG_LAYOUT_ORIENTATION = "l_ori"
CONFIG_LAYOUT_PADDING = "l_pad"
CONFIG_LAYOUT_GAP = "l_gap"
# > view config, for layout to calc area.
CONFIG_LAYOUT_WIDTH = "l_w"
CONFIG_LAYOUT_HEIGHT = "l_h"
CONFIG_LAYOUT_WEIGHT = "l_wt"
# > view config, appearence.
CONFIG_BG_COLOR = "bg_c"
CONFIG_FG_COLOR = "fg_c"
CONFIG_FONT_NAME = "f_n" # FontDraw obj in context name
CONFIG_TEXT = "txt" # str
CONFIG_CENTER_TEXT = "txt_c" # bool
# > progress_view
CONFIG_PROGRESS_VALUE = "proc_v" # float, -1, [0, 1]
# ---- config values ----
CONFIG_VALUE_ORIENTATION_HORIZONTAL = 0
CONFIG_VALUE_ORIENTATION_VERTICAL = 1
# ---- context field ----
CONTEXT_BG_COLOR = "bg_c"
CONTEXT_FG_COLOR = "fg_c"
CONTEXT_FRAME_RATE = "fps"
CONTEXT_FRAME_DURATION = "durt"
CONTEXT_FONT_DRAW_OBJ = "fd_obj" # FontDrae
CONTEXT_ROOT = "root" # MGuiRoot
CONTEXT_ROOT_VIEW = "root_v" # MGuiView
# key event and touch event
CONTEXT_FOCUS_VIEW = "f_id" # MGuiView
