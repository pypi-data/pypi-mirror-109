#!/usr/bin/env python3

"""Definition of class event."""

from . import EnumType


class Event(metaclass=EnumType):  # pylint: disable=R0903
    """Class Event enumerates all handled event types."""

    #  the node has been activated
    ON_ACTIVATE = 'on-activate'

    #  the value of the node has changed
    ON_CHANGE = 'on-change'

    #  the node get the clicked status
    ON_CLICKED = 'on-clicked'

    #  left-click up on the node
    ON_CLICKUP = 'on-click-up'

    #  left-click down on the node
    ON_CLICKDOWN = 'on-click-down'

    #  right-click down on the node
    ON_CLICKDOWNRIGHT = 'on-click-down-right'

    #  right-click up on the node
    ON_CLICKUPRIGHT = 'on-click-up-right'

    #  the node window is closed
    ON_CLOSE = 'on-close'

    #  the node has been disabled
    ON_DISABLE = 'on-disable'

    #  the node has been enabled
    ON_ENABLE = 'on-enable'

    #  the node received the focus
    ON_FOCUS = 'on-focus'

    #  a key has been pressed
    ON_KEY = 'on-key'

    #  the mouse wheel has been used over the node
    ON_MOUSEWHEEL = 'on-mouse-wheel'

    #  the node window is opened
    ON_OPEN = 'on-open'

    #  the cursor just moved over the node
    ON_OVER = 'on-over'

    #  the cursor was previously on the node, and is still over it
    ON_OVERAGAIN = 'on-over-again'

    #  the node has been selected
    ON_SELECT = 'on-select'

    #  the node has lost the focus
    ON_UNFOCUS = 'on-unfocus'

    #  the cursor is not over the node anymore
    ON_UNOVER = 'on-unover'

    #  the node has been unselected
    ON_UNSELECT = 'on-unselect'

    #  the node get the unclicked status
    ON_UNCLICKED = 'on-unclicked'
