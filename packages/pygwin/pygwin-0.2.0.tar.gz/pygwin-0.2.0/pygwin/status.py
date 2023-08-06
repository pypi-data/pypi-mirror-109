#!/usr/bin/env python3

"""Definition of class Status."""

from typing import Dict

from . import Event, EnumType


class Status(metaclass=EnumType):  # pylint: disable=R0903
    """Status class enumerates all the possible status of a node.

    Status can be used to define context dependent styles (e.g, node
    has color "red" if the cursor is over it).

    """

    #  base status
    BASE = 'base'

    #  the node is being left-clicked (i.e., the cursor is over it and
    #  the user has the left mouse button pressed)
    CLICKED = 'clicked'

    #  the node is disabled
    DISABLED = 'disabled'

    #  the node has the focus
    FOCUS = 'focus'

    #  the cursor is over the node
    OVERED = 'overed'

    #  the node is being selected
    SELECTED = 'selected'

    #  for each status s, ON[s] is the event that may turn this status
    #  on and OFF[s] is the event that may turn it off
    ON: Dict[str, str] = {
        BASE: Event.ON_OPEN,
        CLICKED: Event.ON_CLICKED,
        DISABLED: Event.ON_DISABLE,
        FOCUS: Event.ON_FOCUS,
        OVERED: Event.ON_OVER,
        SELECTED: Event.ON_SELECT
    }
    OFF: Dict[str, str] = {
        BASE: Event.ON_CLOSE,
        CLICKED: Event.ON_UNCLICKED,
        DISABLED: Event.ON_ENABLE,
        FOCUS: Event.ON_UNFOCUS,
        OVERED: Event.ON_UNOVER,
        SELECTED: Event.ON_UNSELECT
    }
