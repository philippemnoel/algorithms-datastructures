"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Map Reduce - Mapper Subroutine -- Python 3
Based on: http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import sys

def mapper():
    """ Map Subroutine of the Mapreduce Algorithm for Flight Delays """
    # STDIN input reading
    for line in sys.stdin:
        # remove leading & trailing whitespaces, if any
        line = line.strip()
        # split into words
        words = line.split(',')
        # counters
        if words[3] != 'NA' and words[14] != 'NA':
            day_of_week, arr_delay = int(words[3]), int(words[14])
            print('%s\t%s' % (day_of_week, arr_delay))


# test driver
mapper()
