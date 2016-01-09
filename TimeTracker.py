import argparse
import datetime
from TTM import *

parser = argparse.ArgumentParser(description="Track Time for Study/Work")

parser.add_argument('-b', action="store_true",
                    help = 'Set flag to begin tracking')

parser.add_argument('-d', nargs='?',
                    help='Set the default file to work on.')

parser.add_argument('--default', action='store_true',
                    help='Display the current default')

parser.add_argument('-e', action="store_true",
                    help='Set flag to stop tracking')

parser.add_argument('-f', nargs='?',
                    help='The filename for the data storage.')

parser.add_argument('-l', nargs='?',
                    help='The label associated with this time.')

parser.add_argument('--labels', action="store_true",
                    help='Display labels currently in use.')

parser.add_argument("-s", nargs="?",
                    help="""Return the sum total of time spent on the given
                              subject, in hours (rounded down)""")

parser.add_argument("-m", action="store_true",
                    help="""For sum total report, report in minutes (rounded
                               down)""")

args = parser.parse_args()

#----------------GET THE FILENAME---------------------------------#
filename = ''

if args.f:
    filename = args.f 
else:
    with open('.default', 'r') as fin:
        filename = fin.read().strip()
        

ttm = TimeTrackerManager(filename)
ttm.load()

#----------------GET THE LABEL------------------------------------#
label = ''
if args.l:
    label = args.l

if args.labels:
    s = set( e.topic for e in ttm.data )
    print('Topics: ' + ', '.join(s))

#----------------BEGIN TRACKING-----------------------------------#
# create a new data entry
if args.b:
    ttm.start(label)

#----------------STOP TRACKING------------------------------------#
# find the most recent data entry of type label, if no end, add it otherwise
# throw error
if args.e:
    ttm.end(label)

ttm.save()

#----------------SET THE DEFAULT FILE-----------------------------#
if args.d:
    with open('.default', 'w') as fin:
        fin.write(args.d)

if args.default:
    with open('.default', 'r') as fin:
        print(fin.read())

#----------------GET SUM TIME SPENT-------------------------------#
if args.s:
    print('Time spend on ' + args.s + ': ', end='')
    if args.m:
        print(ttm.report_time_delta_minutes(ttm.sum(args.s)), ' minute(s)')
    else:
        print(ttm.report_time_delta(ttm.sum(args.s)), ' hour(s)')
