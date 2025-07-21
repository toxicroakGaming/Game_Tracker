import datetime
'''
for tracking the date and times in the file
you can use .days, .seconds, .month, .year 
Those will probably be the most applicable to us
'''


#these are just handy little macros in case we forget things
def current_time():
    return datetime.datetime.now()

def time_diff(prev, cur = current_time()):
    return cur - prev
