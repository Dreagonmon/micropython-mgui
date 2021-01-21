from mgui.utils.bmfont import get_text_line
from mgui import mgui_const as C
try:
    from typing import Any, Coroutine, List, Union, Tuple, Optional
    from mgui.utils.bmfont import FontDraw
    from mgui.mgui_class import MGuiRect, MGuiContext, MGuiView
    from mgui.dev.framebuf import FrameBuffer, Color
except: pass

def get_config(config, name, fallback=None):
    # type: (dict, str, Union[str|int|float|bool|None]) -> Union[str|int|float|bool|None]
    value = config[name] if name in config else fallback
    return value

def get_context(context, name, fallback=None):
    # type: (MGuiContext, str, Any) -> Any
    value = context[name] if name in context else fallback
    return value

def get_text_size(txt, font_size, max_width):
    # type: (str, Tuple(int, int), int) -> Tuple(int, int)
    fw, fh = font_size
    lines = get_text_line(txt, max_width, fw)
    if lines == 1:
        real_w = fw * len(txt)
        real_h = fh
    else:
        real_w = max_width - (max_width % fw)
        real_h = lines * fh
    return real_w, real_h

def get_center_box(area, size):
    # type: (MGuiRect, Tuple[int, int]) -> MGuiRect
    x, y, w, h = area
    real_w, real_h = size
    x += (w - real_w) // 2
    y += (h - real_h) // 2
    w, h = real_w, real_h
    return x, y, w, h

def get_padding_box(area, padding):
    # type: (MGuiRect, int) -> MGuiRect
    x, y, w, h = area
    x += padding
    y += padding
    w -= padding * 2
    h -= padding * 2
    return x, y, w, h

def get_flex_children_areas(area, children, gap=None, is_horizontal=True):
    # type: (MGuiRect, List[MGuiView], Optional[int], bool) -> List[MGuiRect]
    area_x, area_y, area_w, area_h = area
    nums = len(children)
    gap_nums = nums - 1
    children_infos = []
    for c in children:
        w = get_config(c.config, C.CONFIG_LAYOUT_WIDTH, -1)
        h = get_config(c.config, C.CONFIG_LAYOUT_HEIGHT, -1)
        wt = get_config(c.config, C.CONFIG_LAYOUT_WEIGHT, 1)
        children_infos.append((w, h, wt))
    areas = []
    # if is_horizontal:
    #     # sum fixed size
    #     fixed = 0
    #     weights = 0
    #     all_fixed = True
    #     for i in range(nums):
    #         areas.append([-1, area_y, -1, area_h])
    #         w = children_infos[i][0]
    #         wt = children_infos[i][2]
    #         areas[i][2] = w
    #         if w >= 0:
    #             fixed += w
    #         else:
    #             all_fixed = False
    #             weights += wt
    #     if all_fixed and gap == None:
    #         # free gap
    #         gap_total = area_w - fixed
    #         free_space = 0
    #     else:
    #         # fixed gap
    #         gap_total = gap_nums * gap
    #         free_space = area_w - fixed - gap_total
    #     # calc pos
    #     used_width = 0
    #     used_weight = 0
    #     for i in range(nums):
    #         areas[i][0] = int(area_x + used_width + (gap_total * i / gap_nums) + (free_space * used_weight / weights))
    #         w = areas[i][2]
    #         if w < 0:
    #             wt = children_infos[i][2]
    #             w = int(free_space * wt / weights)
    #             areas[i][2] = w
    #             used_weight += wt
    #         else:
    #             used_width += w
    # else:
    #     pass
    if is_horizontal:
        v_pos_c=0
        v_pos_a=2
        p_pos_a=0
        area_w_h = area_w
        init_rect=[-1, area_y, -1, area_h]
    else:
        v_pos_c=1
        v_pos_a=3
        p_pos_a=1
        area_w_h = area_h
        init_rect=[area_x, -1, area_w, -1]
    areas = []
    # sum fixed size
    fixed = 0
    weights = 0
    all_fixed = True
    for i in range(nums):
        areas.append(list(init_rect))
        w_h = children_infos[i][v_pos_c]
        wt = children_infos[i][2]
        areas[i][v_pos_a] = w_h
        if w_h >= 0:
            fixed += w_h
        else:
            all_fixed = False
            weights += wt
    if all_fixed and gap == None:
        # free gap
        gap_total = area_w_h - fixed
        free_space = 0
    else:
        # fixed gap
        gap_total = gap_nums * gap
        free_space = area_w_h - fixed - gap_total
    # calc pos
    used_w_h = 0
    used_weight = 0
    for i in range(nums):
        areas[i][p_pos_a] = int(area_x + used_w_h + (gap_total * i / gap_nums) + (free_space * used_weight / weights))
        w_h = areas[i][v_pos_a]
        if w_h < 0:
            wt = children_infos[i][2]
            w_h = int(free_space * wt / weights)
            areas[i][v_pos_a] = w_h
            used_weight += wt
        else:
            used_w_h += w_h
    # convert resault
    resault = []
    for c_area in areas:
        resault.append(tuple(c_area))
    return resault
