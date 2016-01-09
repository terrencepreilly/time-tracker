# time-tracker

A terminal utility for tracking time spent on a given activity.  Tracks time 
based on labels stored in files.

Example:
    $ touch Math_Study
    $ python3 TimeTracker.py -d Math_Study
    $ python3 TimeTracker.py -l Notetaking -b
    ...
    $ python3 TimeTracker.py -l Notetaking -e
    $ python3 TimeTracker.py -s Notetaking -m 
      Time spent on Notetaking: 45 minutes
    $ python3 TimeTracker.py --labels
      Labels: Notetaking
    $ python3 TimeTracker.py --default
      Math_Study
    $ python3 TimeTracker.py -d .defaultTracker.txt
