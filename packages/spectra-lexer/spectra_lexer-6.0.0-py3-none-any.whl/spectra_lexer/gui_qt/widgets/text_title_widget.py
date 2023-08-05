from typing import Iterator

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLineEdit

# Minimum number of trailing dots required to start animation.
MIN_DOTS = 3


class TextTitleWidget(QLineEdit):
    """ Title bar widget with simple text animations for loading messages. """

    _anim: Iterator[str] = iter(str, ...)  # Animation string iterator. Should repeat.
    _timer: QTimer = None                  # Animation timer for loading messages.

    def __init__(self, *args) -> None:
        """ Set up the title bar animation timer. """
        super().__init__(*args)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate_title)

    def set_text(self, s:str, dynamic:bool=True) -> None:
        """ If the text ends in an ellipsis and is marked dynamic, animate it until new text is shown. """
        if self._timer is not None:
            self._timer.stop()
            n = len(s) - len(s.rstrip("."))
            if dynamic and n >= MIN_DOTS:
                self._anim = _title_generator(s, n)
                self._timer.start(200)
        self._setText_safe(s)

    def _animate_title(self) -> None:
        """ Set the title to be the next item in the string generator. """
        self._setText_safe(next(self._anim))

    def _setText_safe(self, s:str):
        """ Programmatically set the text content of the title bar. Suppress signals to keep from tripping events. """
        self.blockSignals(True)
        self.setText(s)
        self.blockSignals(False)


def _title_generator(s:str, n:int) -> Iterator[str]:
    """ Generate a series of strings with cascading dots of length <n> replacing the end of string <s>. """
    while True:
        for i in range(n)[::-1]:
            yield s[:-1-i] + "•" + ("." * i)
        yield s
