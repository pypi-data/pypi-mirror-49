import csv
import timeit
import sys

from time import sleep


class Timer:
    """Print a descending timer for a given delay

    A message can be printed next to the timer, and if in an iteration loop,
    the current iteration can be printed also.

    :param delay: time to wait (in seconds)
    :type delay: int
    :param message: (default ``''``) message to print
    :type message: str
    :param counter: (default ``None``) iteration number to print next to message
    :type counter: int
    :param ms: (default ``False``) use a delay in milliseconds rather than seconds
    :type ms: bool
    :param overwrite: (default ``False``) do not print a new line when the timer is finished
    :type overwrite: bool
    
    :Example:
    
    >>> Timer(delay = 10, message = "Waiting for 10 seconds")
    
    """
    def __init__(self, delay: int, message: str = '', counter: int = None,
                 ms: bool = False, overwrite: bool = False) -> None:
        sleep_time = 1 / 1000 if ms else 1
        for n in range(delay):
            remaining_time = str(delay - n).zfill(len(str(delay)))
            self.print(time = remaining_time, counter = counter, message = message)
            sleep(sleep_time)
        self.close(message = message, counter = counter, overwrite = overwrite)
        return

    @staticmethod
    def print(time: str, counter: int, message: str) -> None:
        """Print the counter for a given time, counter and message"""
        if counter is not None:
            sys.stdout.write('\r%s | %s * %s' % (time, str(counter), message))
        else:
            sys.stdout.write('\r%s | %s' % (time, message))
        sys.stdout.flush()
        return
    
    def close(self, counter: int, message: str, overwrite: bool):
        """Print '0' when time has passed (last iteration is '1')"""
        self.print(time = '0', counter = counter, message = message)
        if not overwrite:
            sys.stdout.write('\n')
            sys.stdout.flush()


class Chronos:
    """Time chunks of code in a script
    
    The class works as a stopwatch during a race on track : after starting it,
    for each 'lap', a button is pushed that record time at this moment, using
    ``timeit.default_timer()``.
    
    Those times have not a meaning yet since they do not correspond to durations
    and depends on the previous recorded times.
    
    When you want to know duration of recorded laps, you use
    ``compute_durations()``, which give durations for each lap and total duration.
    
    Results can be exported as tsv with ``write_tsv()``.
    
    :Example:
    
    >>> from time import sleep
    >>> chrono = Chronos()
    >>> sleep(2)
    >>> chrono.lap(name = 'lap 1')
    >>> sleep(5)
    >>> chrono.lap(name = 'lap 2')
    >>> chrono.compute_durations().durations
    
    """
    def __init__(self):
        self.lap_times = [timeit.default_timer()]
        self.lap_names = ['start']
        self.durations = {}
        self.results = None
    
    def __repr__(self):
        named_laps = ["%s : %s" % (name, time) for name, time in zip(self.lap_names, self.lap_times)]
        return '\n'.join(named_laps)
    
    def lap(self, name: str):
        """Record time for this lap, a name must be provided"""
        self.lap_names.append(name)
        self.lap_times.append(timeit.default_timer())
        return self
    
    def compute_durations(self, ms: bool = False):
        """Compute laps duration

        Duration is the difference between two adjacent laps. Results
        are stored in ``self.durations``, in seconds by default, can be stored
        in milliseconds. The total duration is also added

        :param ms: Express durations in milliseconds rather than seconds
        :type ms: bool

        :return: ``self``
        """
        for i in range(len(self.lap_names)):
            if i == 0:
                self.durations['start'] = 0
            else:
                duration = round(self.lap_times[i] - self.lap_times[i - 1], 3)
                if ms:
                    duration *= 1e3
                self.durations[self.lap_names[i]] = duration
        self.durations['total'] = round(sum(self.durations.values()), 3)
        return self
    
    def write_tsv(self, run_name: str, path: str, col_names: tuple = None):
        """Export durations in tsv file
        
        Write three columns, the first containing ``run_name`` : a string describing
        which execution the durations came from. This way you can append several
        execution times to the same file.
        
        Default values for column names are : Execution, Step, Duration (secs)
        
        :param run_name: name to give to execution for column Execution
        :type run_name: str
        :param path: full path to file to write
        :type path: str
        :param col_names: (default ``None``) column names of length 3
        :type col_names: tuple
        
        :return: ``self``
        """
        if len(self.durations) == 0:
            raise ValueError('durations attribute is empty (have you compute_durations before ?')
        if col_names is None:
            col_names = ('Execution', 'Step', 'Duration (secs')
        elif len(col_names) < 3 | len(col_names) > 3:
            raise ValueError('column names must be of length 3, was %s' % col_names)
        table = [(run_name, step, str(time)) for step, time in self.durations.items()]
        with open(path, 'a') as out_table:
            tsv_writer = csv.writer(out_table, delimiter = '\t')
            tsv_writer.writerow(col_names)
            for row in table:
                tsv_writer.writerow(row)
        return self
