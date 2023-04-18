import time
import mmap


def test_speed(n, func: callable = None, args: tuple = ()):
    start = time.time()
    for i in range(0, n):
        func(*args)
    end = time.time() - start
    print(f"Result: ({func.__name__})", end)
    return end


def buf_count(filename):
    f = open(filename, "rb")
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read  # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)

    return lines


def op_count(filename):
    with open(filename, "rb") as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def simple_count(filename):
    lines = 0
    for line in open(filename, "rb"):
        lines += 1
    return lines


def map_count(filename):
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines


def split_count(filepath):
    with open(filepath, 'rb') as f:
        return len(f.read().split(b'\n'))


N = 100000
PATH = "./README.md"


def main():
    funcs = [split_count, buf_count, simple_count, op_count, map_count]
    result = {}
    for func in funcs:
        result[test_speed(N, func=func, args=(PATH,))] = func.__name__

    print(result)

