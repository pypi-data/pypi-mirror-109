#!/usr/bin/env python3

"""Definition of some types for mypy."""


#  pylint: disable=invalid-name

from typing import Optional, Tuple, Callable, Any, List, Union, Literal
from typing import TYPE_CHECKING
import pygame as pg
if TYPE_CHECKING:
    from . import Node, Style


rect_t = Tuple[int, int, int, int]
anchor_t = Tuple[
    Literal['left', 'center', 'right'],
    Literal['top', 'center', 'bottom']
]
floating_pos_type_t = Literal['relative', 'absolute']
pos_t = Tuple[int, int]
floating_pos_t = Tuple[floating_pos_type_t, anchor_t, pos_t]
opt_pos_t = Optional[pos_t]
pos_opt_t = Tuple[Optional[int], Optional[int]]
opt_pos_opt_t = Optional[pos_opt_t]
node_pred_t = Callable[['Node'], bool]
event_proc_t = Callable[[pg.event.Event], bool]
style_class_ctx_t = Tuple[Tuple[str, Any], ...]
style_class_def_t = Tuple[style_class_ctx_t, List[node_pred_t], 'Style', int]
user_key_proc_t = Callable[[], None]
color_t = Union[Tuple[int, int, int], Tuple[int, int, int, int]]
padding_t = Union[int, Tuple[int, int]]
font_size_rel_t = Literal[
    'xx-small', 'x-small', 'small', 'normal', 'large', 'x-large', 'xx-large'
]
font_size_t = Union[int, font_size_rel_t]
animation_t = Literal['fade', 'fadein', 'fadeout', 'grow', 'glow', 'scroll']
valign_t = Literal['bottom', 'center', 'top']
halign_t = Literal['center', 'left', 'right']
background_t = Literal['color', 'image']
border_t = Literal['color', 'image']
orientation_t = Literal['vertical', 'horizontal']
push_dest_t = Literal['bottom', 'top']
abs_size_t = Tuple[int, int]
size_t = Tuple[Optional[Union[str, int]], Optional[Union[str, int]]]
animation_callback_t = Callable[[], None]
