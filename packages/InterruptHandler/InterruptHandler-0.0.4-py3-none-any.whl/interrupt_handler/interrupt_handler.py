import sys
import os
import signal
from .default_callback import default_callback

class InterruptHandler(object):
    _depth_cnt = 0

    def __init__(self, callback=default_callback(), sig=signal.SIGINT, propagate=False):
        if not callable(callback):
            raise ValueError(f'callback parameter is not support {type(callback)}.')
        self.callback = callback
        self.sig = sig
        self.propagate = propagate
        self.original_handler = None

    @classmethod
    def _increase_depth(cls):
        InterruptHandler._depth_cnt += 1
    
    @classmethod
    def _decrease_depth(cls):
        InterruptHandler._depth_cnt -= 1

    @property
    def is_child(self):
        return self._depth_cnt > 0

    @property
    def interrupted(self):
        return getattr(self, '_interrupted', False)

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, type, value, tb):
        return self.release()

    def initialize(self):
        if not self.original_handler:
            self._increase_depth()
            self._interrupted = False
            self.released = False
            self.original_handler = signal.getsignal(self.sig)
            def handler(signum, frame):
                if not self.callback():
                    self.release(True)
                self._interrupted = True
            signal.signal(self.sig, handler)
        else:
            raise RuntimeError('Already initialized.')

    def release(self, interrupted=False):
        if self.released:
            if self.propagate and self.is_child:
                os.kill(os.getpid(), self.sig)
            return True
        if self.original_handler:
            signal.signal(self.sig, self.original_handler)
            self.original_handler = None
        self.released = True
        self._decrease_depth()
        if interrupted: raise KeyboardInterrupt
        return False
