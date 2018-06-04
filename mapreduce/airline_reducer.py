"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Map Reduce - Reducer Subroutine -- Python 3
Based on: http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import sys
from operator import itemgetter

def reducer():
    """ Reduce Subroutine of the Mapreduce Algorithm for Flight Delays """
    # variables init
    curr_day, curr_sum_delays, curr_num_days = None, 0, 0

    # STDIN input reading
    for line in sys.stdin:
        # remove leading & trailing whitespaces, if any
        line = line.strip()
        # parse the input from the Map subroutine of Mapreduce (mapper.py)
        day, delay = line.split('\t', 1)
        delay = int(delay) # type conversion
        # note: this IF-switch works because Hadoop sorts map output by key
        if curr_day == day:
            curr_sum_delays += delay
            curr_num_days += 1
        else:
            # case where day read != curr_day, so we output & reset
            print('Day = %s, Number of Delays = %s, Sum of Delays = %s ' +
                  'Average Delay = %s' % (curr_day, curr_num_days,
                  curr_sum_delays, float(curr_sum_delays) / float(curr_num_days)))
            # reset counters
            curr_sum_delays, curr_num_days, curr_day = delay, 1, day

    # final day output
    if curr_day == day:
        print('Day = %s, Number of Delays = %s, Sum of Delays = %s ' +
              'Average Delay = %s' % (curr_day, curr_num_days,
              curr_sum_delays, float(curr_sum_delays) / float(curr_num_days)))


# driver test
reducer()
