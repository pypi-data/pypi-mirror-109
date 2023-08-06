#!/usr/bin/env python3

"""Definition of class Animation."""

from __future__ import annotations
from typing import Any, Callable, List, Dict, Optional, TYPE_CHECKING
import itertools
import pygame as pg

from . import types
if TYPE_CHECKING:
    from . import Window


class Animation:
    #  pylint: disable=too-many-instance-attributes
    """An Animation is some function that is executed periodically.

    An animation has a period (in ms) ; and an handler which is a
    function taking as argument some progression value and returning
    an updated progress value.  The animation keeps executing as long
    as the progress value returned by the handler function is not
    None.

    """

    __ALL: Dict['Window', List[Animation]] = dict()

    def __init__(
            self,
            prog: Any,
            period: int,
            handler: Callable[[Any], Any],
            win: 'Window'
    ):
        """Initialise an Animation with the given period and handler.

        prog is the initial progression value of the animation.  The
        animation is attached to Window win.  This means that the
        animation is stopped when win is closed.

        """
        self.__prog: Any = prog
        self.__period: int = period
        self.__handler: Callable[[Any], Any] = handler
        self.__last: int = pg.time.get_ticks()
        self.__paused: bool = False
        self.__win: 'Window' = win
        self.__callback: Optional[types.animation_callback_t] = None
        self.__started: bool = False
        self.__stopped: bool = False

    @property
    def prog(self) -> Any:
        """Get the current progression value of the animation."""
        return self.__prog

    @property
    def period(self) -> int:
        """Get the period, in ms, of the animation."""
        return self.__period

    def pause(self) -> None:
        """Pause the animation."""
        self.__paused = True

    def start(self, start_now: bool = True) -> None:
        """Start the animation.

        If start_now is True, the animation handler is executed right
        now.  Otherwise it first occurs in self.period ms.

        """
        if self.__started:
            return
        self.__started = True
        self.__paused = False
        if start_now:
            self.__prog = self.__handler(self.__prog)
        if self.__prog is not None:
            Animation.__ALL.setdefault(self.__win, [])
            Animation.__ALL[self.__win].append(self)

    def set_callback(self, callback: types.animation_callback_t) -> None:
        """Set the callback of the animation."""
        self.__callback = callback

    def has_terminated(self) -> bool:
        """Check if the animation has terminated."""
        return self.__prog is None

    def check_run(self) -> bool:
        """Check if the animation must be runned now.

        Return True if the handler function must be called now, False
        otherwise.  The handler must be called if (1) the animation
        has been started (2) not paused and (3) more than period time
        has elapsed since the last time it has been runned.

        """
        return (
            not self.__paused
            and self.__prog is not None
            and pg.time.get_ticks() - self.__last >= self.__period
        )

    def run(self) -> None:
        """Run the animation now.

        The handler of the animation is called and its progression
        value is updated.

        """
        self.__prog = self.__handler(self.__prog)
        self.__last = pg.time.get_ticks()

    @classmethod
    def run_all(cls, wins: Optional[List[Window]] = None) -> bool:
        """Run all animations that must be run now.

        Returns True if at least one animation has been runned, False
        otherwise.  If wins is not None, then only the animations of
        Windows in wins must be run.

        """
        result = False
        if wins is None:
            wins = list(Animation.__ALL.keys())
        for win in wins:
            done = []
            for anim in Animation.__ALL.get(win, []):
                if anim.check_run():
                    anim.run()
                    result = True
                if anim.has_terminated():
                    done.append(anim)
                    anim.stop()
            for anim in done:
                #  the animation execution or callback may have closed
                #  the window.  hence we must check it still in __ALL
                if win in Animation.__ALL:
                    Animation.__ALL[win].remove(anim)
                    if Animation.__ALL[win] == []:
                        del Animation.__ALL[win]
        return result

    def stop(self) -> None:
        """Stop the animation."""
        self.__prog = None
        stopped = self.__stopped
        self.__stopped = True
        if not stopped and self.__callback is not None:
            self.__callback()

    @classmethod
    def stop_all(cls, wins: Optional[List[Window]] = None) -> None:
        """Stop all animations.

        If wins is not None, then only the animations of Windows in
        wins are stopped.

        """
        if wins is None:
            stopped = itertools.chain(*Animation.__ALL.values())
            new_all = dict()
        else:
            stopped = itertools.chain(
                [val for win in wins for val in Animation.__ALL.get(win, [])]
            )
            new_all = {
                win: Animation.__ALL[win]
                for win in Animation.__ALL
                if win not in wins
            }
        Animation.__ALL = new_all
        for anim in stopped:
            anim.stop()
