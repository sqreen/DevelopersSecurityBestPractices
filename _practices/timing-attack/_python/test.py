import time
import statistics

timer = time.perf_counter  # requires Python 3.3 or later


def check_password(password, second_password):
    return password == second_password

performance_times = []

too_long = "\1" * 10000


for i in range(20):

    equals_times = []
    not_equals_times = []

    for _ in range(10000):
        good_password = "A"*i
        bad_password = "B" + "0"*(i-1)
        t1 = timer()
        check_password(good_password, bad_password)
        t2 = timer()

        not_equals_times.append(t2 - t1)

    for _ in range(10000):
        good_password = "A"*i
        other_password = "A" + "0"*(i-1)
        t1 = timer()
        check_password(good_password, bad_password)
        t2 = timer()

        equals_times.append(t2 - t1)

    print("Size %d not equal: %s" % (i, statistics.mean(not_equals_times)))
    print("Size %d equal: %s" % (i, statistics.mean(equals_times)))
