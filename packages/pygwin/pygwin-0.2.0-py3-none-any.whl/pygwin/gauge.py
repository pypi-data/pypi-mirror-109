#!/usr/bin/env python3

"""Definition of class Gauge."""

from typing import Iterator, Any
import pygame as pg

from . import types, Draw, Node, Label


class Gauge(Node):
    """Gauge nodes are used to draw status bars (e.g., health bars in RPGs)."""

    AVAILABLE_STYLES = {
        'color',
        'gauge-label-class',
        'gauge-label-format'
    }

    def __init__(
            self,
            min_val: int,
            max_val: int,
            val: int,
            **kwargs: Any
    ):
        """Initialise a Gauge node.

        The value of the gauge ranges from min_val to max_val and
        is initialised to val.

        """
        Node.__init__(self, **kwargs)
        self.__min: int = min_val
        self.__max: int = max_val
        self.__val: int = val
        label_format = self.get_style('gauge-label-format')
        if label_format is None:
            self.__label = None
        else:
            self.__label = Label('', stc=self.get_style('gauge-label-class'))
            self.__set_label()
            self._add_child(self.__label)

    @property
    def value(self) -> int:
        """Get the current value of the gauge."""
        return self.__val

    def set_value(self, val: int) -> None:
        """Update the current value of the gauge."""
        self.__val = val
        self.__set_label()
        self._update_manager()

    def __set_label(self) -> None:
        if self.__label is not None:
            label_format = self.get_style('gauge-label-format')
            label = label_format.format(
                min=self.__min, value=self.__val, max=self.__max
            )
            self.__label.set_text(label)

    def _compute_inner_size(self) -> types.pos_t:
        if self.__label is not None:
            self.__label._compute_size()
        return (200, 40)

    def _position(self, pos: types.pos_t) -> None:
        if self.__label is not None:
            self.__label._set_container_size(self.get_inner_size_())
            self.__label.position(pos)

    def _draw(self, surface: pg.surface.Surface, pos: types.pos_t) -> None:
        w, h = self.get_inner_size_()
        color = self.get_style('color')
        pts = int(self.__val * w / (self.__max - self.__min))
        rect = (pos[0], pos[1], pts, h)
        Draw.rectangle(surface, color, rect)

    def _iter_tree(
            self, rec: bool = True, traverse: bool = False
    ) -> Iterator[Node]:
        if self.__label is not None:
            yield from self.__label.iter_tree(traverse=traverse)
