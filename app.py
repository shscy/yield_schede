from bisect import insort
from collections import deque

from functools import partial

import asyncio

import types


def timed_fib(n):
    if n <= 1:
        yield n
    a = yield timed_fib(n - 1)
    b = yield timed_fib(n - 2)
    yield a+ b


async def fib(n):
    if n <=1:
        return n
    a = await fib(n -1)
    b = await fib(n - 2)
    return a + b

class Result:
    def __init__(self, n):
        self.n = n
    def __await__(self):
        yield self
        return self.n

async  def fib2(n):
    if n <= 1:
        ret = await Result(n)
        return ret
    a = await fib2(n - 1)
    b = await fib2(n - 2)
    return a + b

class EventLoop:

    def __init__(self,):
        self._running = True
        self._tasks = deque()

    def resume_task(self, coroutine, value=None, stack=()):
        try:
            result = coroutine.send(value)
        except:
            return
        if isinstance(result, types.GeneratorType):
            self.schedule(result, None, (coroutine, stack))
        elif stack:
            self.schedule(stack[0], result, stack[1])

    def schedule(self, coroutine, value=None, stack=()):

        task = partial(self.resume_task, coroutine, value, stack)
        self._tasks.append(task)

    def do_on_next_tick(self, func, *args, **kwargs):
        self._tasks.appendleft(partial(func, *args, **kwargs))

    def run_forever(self):
        while self._running:
            if self._tasks:
                task = self._tasks.popleft()
                task()


def tt(n):
    ret = yield timed_fib(n)
    print("result: ", ret)


def main():
    loop = EventLoop()
    loop.schedule(tt(10))
    loop.run_forever()


def run():
    obj = fib(10)
    ret = None
    while True:
        try:
            print("run")
            ret = obj.send(None)

        except StopIteration as ex:
            print("result: ", ex)
            break

def run2():
    obj = fib2(10)
    ret = None
    while True:
        try:
            print("run")
            ret = obj.send(None)

        except StopIteration as ex:
            print("result: ", ex)
            break

if __name__ == '__main__':
    # main()
    # run()
    # run2()
    pass