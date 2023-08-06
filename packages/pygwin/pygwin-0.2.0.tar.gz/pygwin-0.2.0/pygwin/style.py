#!/usr/bin/env python3

"""Definition of class Style."""

from typing import Any, Set, Dict, List, Tuple

import logging
import pygame as pg

from . import StaticDict, types


class Style(StaticDict):
    """A style is a dictionary encoding possible style attributes of a Node."""

    DEFAULT = {
        'animation': None,
        'animation-arguments': None,
        'background': None,
        'background-color': (0, 0, 0),
        'background-image': None,
        'border': None,
        'border-color': (100, 100, 100),
        'border-images': None,
        'border-width': 0,
        'color': (255, 255, 255),
        'corner': None,
        'cursor-image': None,
        'expand': False,
        'font': pg.font.get_default_font(),
        'font-size': 16,
        'frame-bar-background-color': (100, 100, 100, 150),
        'frame-bar-color': (150, 150, 150, 150),
        'frame-bar-corner': 4,
        'frame-bar-width': 8,
        'frame-vbar-images': None,
        'gauge-label-class': None,
        'gauge-label-format': '{value} / {max}',
        'grid-row-size': None,
        'halign': 'left',
        'hspacing': 10,
        'input-text-allowed': r'A-Za-z\d \_\-\'\"\.',
        'input-text-max-size': 20,
        'input-text-placeholder': None,
        'opacity': None,
        'orientation': 'vertical',
        'padding': 0,
        'pos': None,
        'pos-list': None,
        'range-acceleration': 10,
        'range-bar-color': (150, 150, 150, 150),
        'range-bar-corner': 0,
        'range-bar-size': (200, 4),
        'range-bullet-color': (150, 150, 150, 150),
        'range-bullet-radius': 6,
        'range-label-class': None,
        'range-label-distance': 6,
        'range-label-format': '{value}',
        'rule-images': None,
        'scale': None,
        'select-cyclic': False,
        'select-hide-links': True,
        'select-next-class': None,
        'select-next-label': '&gt;&gt;',
        'select-prev-class': None,
        'select-prev-label': '&lt;&lt;',
        'select-wheel-units': 1,
        'size': None,
        'sound': None,
        'text-board-push-dest': 'bottom',
        'text-board-rows': None,
        'underline': False,
        'valign': 'top',
        'vspacing': 10,
        'window-cross-image': None
    }

    TYPE: Dict[str, Any] = {
        'animation': types.animation_t,
        'animation-arguments': Dict[str, Any],
        'background': types.background_t,
        'background-color': types.color_t,
        'background-image': str,
        'border': types.border_t,
        'border-color': types.color_t,
        'border-images': Tuple[str, str, str, str, str, str],
        'border-width': int,
        'color': types.color_t,
        'corner': int,
        'cursor-image': str,
        'expand': bool,
        'font': str,
        'font-size': types.font_size_t,
        'frame-bar-background-color': types.color_t,
        'frame-bar-color': types.color_t,
        'frame-bar-corner': int,
        'frame-bar-width': int,
        'frame-vbar-images': Tuple[str, str, str, str, str, str],
        'gauge-label-class': str,
        'gauge-label-format': str,
        'grid-row-size': int,
        'halign': types.halign_t,
        'hspacing': int,
        'input-text-allowed': str,
        'input-text-max-size': int,
        'input-text-placeholder': str,
        'opacity': float,
        'orientation': types.orientation_t,
        'padding': types.padding_t,
        'pos': types.floating_pos_t,
        'pos-list': List[types.floating_pos_t],
        'range-acceleration': int,
        'range-bar-color': types.color_t,
        'range-bar-corner': int,
        'range-bar-size': types.abs_size_t,
        'range-bullet-color': types.color_t,
        'range-bullet-radius': int,
        'range-label-class': str,
        'range-label-distance': int,
        'range-label-format': str,
        'rule-images': Tuple[str, str, str],
        'scale': float,
        'select-cyclic': bool,
        'select-hide-links': bool,
        'select-next-class': str,
        'select-next-label': str,
        'select-prev-class': str,
        'select-prev-label': str,
        'select-wheel-units': int,
        'size': types.size_t,
        'sound': str,
        'text-board-push-dest': types.push_dest_t,
        'text-board-rows': int,
        'underline': bool,
        'valign': types.valign_t,
        'vspacing': int,
        'window-cross-image': str
    }

    INHERITED: Set[str] = {
        'font',
        'font-size'
    }

    def __setitem__(self, attr: str, value: Any) -> None:
        """Change the value of style attribute attr.

        No update is done if attr is not an existing style attribute
        or if value is not valid for this style attribute.

        """
        try:
            StaticDict.__setitem__(self, attr, value)
        except KeyError:
            logging.warning('undefined style: %s', attr)
        except ValueError:
            logging.warning('invalid value for style %s: %s', attr, value)

    def __getitem__(self, attr: str) -> Any:
        """Get the value of style attribute attr.

        Return None if attr is not an existing style attribute.

        """
        try:
            return StaticDict.__getitem__(self, attr)
        except KeyError:
            logging.warning('undefined style: %s', attr)
            return None
