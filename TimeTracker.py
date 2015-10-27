import argparse
import datetime
from TTM import *

parser = argparse.ArgumentParser(description = "Track Time for Study/Work")

parser.add_argument('-f', nargs = '?', help = "The filename for the data storage.")

parser.add_argument('-l', nargs = '?', help = "The label associated wit this time.")

parser.add_argument('-b', action = "store_true", help = "Set flag to begin tracking")

parser.add_argument("-e", action = "store_true", help = "Set flag to stop tracking")

parser.add_argument("-s", nargs = "?", help = "Return the sum total of time spent on the given subject, in hours (rounded down)")

parser.add_argument("-m", action = "store_true", help = "For sum total report, report in minutes (rounded down)")

args = parser.parse_args()

#----------------GET THE FILENAME---------------------------------#
filename = args.f if args.f else ".defaultTracker.txt"
ttm = TimeTrackerManager(filename)
ttm.load()

#----------------GET THE LABEL------------------------------------#
label = args.l if args.l else None

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

#----------------GET SUM TIME SPENT-------------------------------#
if args.s:
	print "Time spend on", args.s, ": ",
	if args.m:
		print ttm.report_time_delta_minutes(ttm.sum(args.s))
	else:
		print ttm.report_time_delta(ttm.sum(args.s))
