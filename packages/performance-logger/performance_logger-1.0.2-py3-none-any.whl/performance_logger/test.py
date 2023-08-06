from main import perf_logger
import random


def linear_search(target, data):
    i = 0
    while i < len(data):
        if data[i] == target:
            return i
        i += 1
    return "Fail"


def binary_search(target, data):
    start = 0
    end = len(data) - 1
    while start <= end:
        mid = (start + end) // 2

        if data[mid] == target:
            return mid  # 함수를 끝내버린다.
        elif data[mid] < target:
            start = mid + 1
        else:
            end = mid - 1
    return 'Fail'


@perf_logger("ns")
def test_fun():
    print(linear_search(999, [random.randrange(1000) for _ in range(10_000_000)]))


@perf_logger("ns")
def test_fun2():
    print(binary_search(999, [i for i in range(10_000_000)]))


test_fun()
test_fun2()