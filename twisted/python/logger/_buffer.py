# -*- test-case-name: twisted.python.logger.test.test_buffer -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Log observer that maintains a buffer.
"""

from collections import deque

from zope.interface import implementer

from twisted.python.logger._observer import ILogObserver

_DEFAULT_BUFFER_MAXIMUM = 64*1024

@implementer(ILogObserver)
class LimitedHistoryLogObserver(object):
    """
    L{ILogObserver} that stores events in a buffer of a fixed size::

        >>> from twisted.python.logger import LimitedHistoryLogObserver
        >>> history = LimitedHistoryLogObserver(5)
        >>> for n in range(10): history({'n': n})
        ...
        >>> repeats = []
        >>> history.replayTo(repeats.append)
        >>> len(repeats)
        5
        >>> repeats
        [{'n': 5}, {'n': 6}, {'n': 7}, {'n': 8}, {'n': 9}]
        >>>
    """

    def __init__(self, size=_DEFAULT_BUFFER_MAXIMUM):
        """
        @param size: The maximum number of events to buffer.  If C{None}, the
            buffer is unbounded.
        @type size: L{int}
        """
        self._buffer = deque(maxlen=size)


    def __call__(self, event):
        """
        When invoked, store the log event.
        """
        self._buffer.append(event)


    def replayTo(self, otherObserver):
        """
        Re-play the buffered events to another log observer.
        """
        for event in self._buffer:
            otherObserver(event)