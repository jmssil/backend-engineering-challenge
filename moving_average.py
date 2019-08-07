#!/usr/bin/python

"""This script computes the moving average of the duration of events
over a given window size. The events are read from an input file in
JSON format.

"""

import argparse
import datetime
import json
import sys

def print_average(time, average):
    """Prints moving average in JSON format."""
    print json.dumps({"date": str(time), "average_delivery_time": average})

def main():
    """The approach used for computing the moving average of events'
    duration over a window size is to parse the list of events and
    create a new list with additional mirror events. An event of
    duration d in time t will lead to the creation of a mirror event
    of duration -d in time t+ws, where ws is the window size. By using
    this data structure we can simply compute the accumulated average
    for all the time interval. Any original event will thus be
    subtracted from the accumulated average when it goes out the
    window by assimilating its mirror (symmetric duration value).

    """

    # create list of original events from JSON file
    events = []
    for line in open(ARGS.input_file, 'r'):
        events.append(json.loads(line))

    # get start and end times: start_time is the minute of the first
    # event and end_time is the minute next to the last event
    timestamp_format = '%Y-%m-%d %H:%M:%S.%f'
    start_time = datetime.datetime.strptime(events[0]['timestamp'], timestamp_format)
    start_time = start_time.replace(second=0, microsecond=0)
    end_time = datetime.datetime.strptime(events[-1]['timestamp'], timestamp_format)
    end_time = end_time.replace(minute=end_time.minute + 1, second=0, microsecond=0)

    # create mirror events: for each original event we create a mirror
    # one after "window_size" time and with a symmetric duration
    events_mirrored = []
    for event in events:
        event_timestamp = datetime.datetime.strptime(event['timestamp'], timestamp_format)
        event_duration = event['duration']
        events_mirrored.append({'timestamp': event_timestamp, 'duration': event_duration})
        mirror_timestamp = event_timestamp + datetime.timedelta(minutes=ARGS.window_size)
        if mirror_timestamp <= end_time:
            events_mirrored.append({
                'timestamp': mirror_timestamp,
                'duration': -event_duration
            })

    # sort list of original and mirror events, so that we can iterate
    # them in chronological order
    events_mirrored_sorted = sorted(events_mirrored, key=lambda event: event['timestamp'])

    # iterate the list of events chronologically
    time = start_time
    average = 0.0
    num_events = 0
    for event in events_mirrored_sorted:
        event_timestamp = event['timestamp']

        # print average up to this event
        while time < event_timestamp:
            print_average(time, average)
            time = time + datetime.timedelta(minutes=1)

        # update average value
        event_duration = event['duration']
        average = (average * num_events + event_duration)
        if event_duration >= 0:
            # it's an original event
            num_events = num_events + 1
        else:
            # it's a mirror event
            num_events = num_events - 1
        if num_events == 0:
            average = 0.0
        else:
            average = average / num_events

    # there are no more original or mirror events: print average until
    # the end of the interval
    while time <= end_time:
        print_average(time, average)
        time = time + datetime.timedelta(minutes=1)

if __name__ == '__main__':

    # define program syntax
    PARSER = argparse.ArgumentParser(description='Calculate moving average.')
    PARSER.add_argument('--input_file', required=True, type=str, dest='input_file',
                        help='input file in JSON format')
    PARSER.add_argument('--window_size', required=True, type=int, dest='window_size',
                        help='window size in minutes')

    # parse input arguments
    ARGS = PARSER.parse_args()
    if ARGS.window_size < 1:
        print >> sys.stderr, "Window size must be a positive integer (minutes)."
        sys.exit(-1)

    main()
