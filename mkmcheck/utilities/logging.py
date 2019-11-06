import time


class Timer(object):

    def __init__(self):
        self._start_time = time.time()
        self.current_time = self._start_time

    def middle_time(self):
        v = time.time() - self.current_time
        self.current_time = time.time()
        return v

    def update(self, *args, **kwargs):
        print(*args, self.middle_time(), **kwargs)

    def time(self) -> float:
        return time.time() - self._start_time