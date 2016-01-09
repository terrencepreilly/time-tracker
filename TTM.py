from datetime import datetime
from datetime import timedelta


class Entry(object):

    def __init__(self, topic, start=None, end=None):
        """Create a new Entry object for use in a TimeTrackerManager."""
        self.topic = topic
        self.start = start
        self.end = end

        def parse_line(self, line):
                """Parse a line from a file for storage and use in data
                container. The line should be in the following format:
                        <topic>\t<start>\t<end>
                Where start and end are stored as Datetime Strings"""
                if line.strip().lower() == None:
                        return None
                topic, start, end = [a.strip() for a in line.split('\t')]
                return topic, start, end

        def parse_time(self, t):
                """Get datetime from a string, t."""
                if t.lower().strip() == "none":
                        return None
                date, time = t.split('T')
                date = [ int(a) for a in date.split('-')]
                time = time.split(':')
                time[2], millis = time[2].split('.')
                time.append(millis)
                time = [int(a) for a in time]
                return datetime(date[0], date[1], date[2],
                                time[0], time[1], time[2], time[3])

    def line_init(self, line):
        """Populate topic, start, and stop from the given line"""
        pline = self.parse_line(line)
        self.topic = pline[0]
        self.start = None if pline[1] == "None" else self.parse_time(pline[1])
        self.end = None if pline[2] == "None" else self.parse_time(pline[2])

    def __cmp__(self, other):
        """Compare self to another Entry on the basis of start time"""
        if self.start == None:
            return -1
        elif other.start == None:
            return 1
        else:
            return cmp(self.start, other.start)

    def __str__(self):

        start_str = "None"
        if self.start != None:
            start_str = datetime.isoformat(self.start)
        end_str = "None"
        if self.end != None:
            end_str = datetime.isoformat(self.end)
        return '\t'.join( [self.topic, start_str, end_str] )

    def matches(self, topic):

        return self.topic == topic

    def delta(self):

        return self.end - self.start


class TimeTrackerManager(object):
    def __init__(self, filename=".defaultTracker.txt"):
        self.filename = filename
        self.data = list() # a list of tuples: (topic, start, end)

    def load(self):
        """Load the database from filename"""
        fin = None
        try:
            fin = open(self.filename, 'r')
            lines = fin.readlines()
            for line in lines:
                entry = Entry('')
                entry.line_init(line)
                self.data.append( entry )
        except IOError:
            print("Data file does not exist. Creating new data file at " +
                  self.filename)
        finally:
            if fin != None:
                fin.close()

    def save(self):
        """Write the current data to filename"""
        fout = open(self.filename, 'w')
        for datum in self.data:
            fout.write(str(datum) + '\n')
        fout.close()

    def findRecentIndex(self, topic):
        """Super Slow Version"""
        all_instances = list()

        for d in range(len(self.data)):
            if self.data[d].matches(topic):
                all_instances.append((self.data[d], d))

        all_instances.sort()
        if len(all_instances) == 0:
            return None
        if (all_instances[-1][0].start == None or
            all_instances[-1][0].end != None):
            print("No start time defined. Creating empty start time")
            self.data.append( Entry(topic) )
            return len(self.data) - 1
        return all_instances[-1][1]

    def start(self, topic):
        """Record start time for this topic."""
        self.data.append( Entry(topic, datetime.now(), None) )

    def end(self, topic):
        """Record end time for this topic"""
        i = self.findRecentIndex(topic)
        if (i != None):
            self.data[i].end = datetime.now()

    def filter_topic(self, t):
        """Filter etries by topic"""
        f = lambda e : e.topic == t
        return filter(f, self.data)

    def report_time_delta(self, td):
        """Reports total time delta in hours (rounded down)"""
        hours = int(td.total_seconds() / 60 / 60)
        return hours

    def report_time_delta_minutes(self, td):
        """Report total time delta in minutes (rounded down)"""
        minutes = int(td.total_seconds() / 60)
        return minutes

    def sum(self, topic):
        """Report the total sum of time, in timedelta"""
        all_entries = self.filter_topic(topic)
        tot = timedelta(0, 0, 0)
        for entry in all_entries:
            tot += entry.delta()
        return tot

