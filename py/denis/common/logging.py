import sys
import time

class log:
    logfile=sys.stdout
    stopped=False
    tracker=None
    timer=None
    autoflush=True

    @staticmethod
    def start(message=None, logfile=None, args=None):
        if logfile and type(logfile) == type('a'):
            log.logfile=open(logfile, 'w')
        if message and type(message) == type(lambda x: x):
            if args: message(args)
            else: message()
    @staticmethod
    def stop():
        if log.logfile != sys.stdout: 
            log.logfile.close()
        log.stopped = True
    @staticmethod
    def getstream():
        return log.logfile
    @staticmethod
    def write(message, stdoutOnly=False):
        if stdoutOnly and log.getstream() != sys.stdout:
            return
        if not log.stopped:
            log.getstream().write(message)
            if log.autoflush: log.getstream().flush()
        else:
            raise Exception("Log has stopped!")
    @staticmethod
    def writeln(message='', stdoutOnly=False):
        log.write(message, stdoutOnly=stdoutOnly); log.write('\n', stdoutOnly=stdoutOnly)
    @staticmethod
    def progress(current, total, numDots=0, stdoutOnly=False):
        line = str.format('\r{0}{1}%', numDots*'.', int((float(current)/total)*100))
        log.write(line, stdoutOnly=stdoutOnly)
    @staticmethod
    def yesno(bln):
        if bln: return 'Yes'
        else: return 'No'

    @staticmethod
    def track(total=None, msgFormatter='{0}%', writeInterval=1, stdoutOnly=True):
        # if msgFormatter was given as a string, convert it to a lambda function
        if type(msgFormatter) == type('str'):
            msgFormat = msgFormatter
            # default to percentage with a total
            if total: msgFormatter = lambda current, total: str.format(msgFormat, int((float(current)/total)*100))
            # default to printing current with no total
            else: msgFormatter = lambda current: str.format(msgFormat, current)

        # set up the onIncrement lambda for current/total or current only
        if total:
            onIncrement = lambda current, total: log.write(
                str.format('\r{0}', msgFormatter(current, total)), stdoutOnly=stdoutOnly
            )
        else:
            onIncrement = lambda current: log.write(
                str.format('\r{0}', msgFormatter(current)), stdoutOnly=stdoutOnly
            )

        log.tracker = ProgressTracker(total, onIncrement=onIncrement, writeInterval=writeInterval)

    @staticmethod
    def tick():
        if log.tracker != None:
            if not log.tracker.total or log.tracker.current < log.tracker.total:
                log.tracker.increment()
            else:
                raise Exception('Tracker is complete!')

    @staticmethod
    def startTimer(message=None):
        if message:
            log.writeln(message)
        log.timer = Timer()
        log.timer.start()
        return log.timer

    @staticmethod
    def stopTimer(timer=None, frmt='>>Completed in {0} sec.\n'):
        if timer or log.timer:
            if not timer: timer = log.timer
            timer.stop()
            elpsed = timer.elapsed()
            log.writeln(str.format(frmt, log.timer.elapsed()))
        else:
            raise Exception('No timer to stop!')

class ProgressTracker:
    def __init__(self, total=None, onIncrement=None, writeInterval=1):
        self.total = total
        self.current = 0
        self.sinceLastWrite = 0
        self.onIncrement = onIncrement
        self.writeInterval = writeInterval

    def increment(self):
        self.current += 1
        self.sinceLastWrite += 1
        if self.sinceLastWrite >= self.writeInterval:
            self.sinceLastWrite = 0
            if self.onIncrement:
                # only call 2-arg onIncrement if we have a total we're counting towards
                if self.total: self.onIncrement(self.current, self.total)
                else: self.onIncrement(self.current)

class Timer:
    def __init__(self):
        self.startTime = 0
        self.stopTime = 0
        self.started = False

    def start(self):
        if not self.started:
            self.startTime = time.time()
            self.started = True
        else:
            raise Exception('Timer already started!')

    def stop(self):
        if self.started:
            self.stopTime = time.time()
            self.started = False
        else:
            raise Exception('Timer already stopped!')

    def elapsed(self):
        if not self.started:
            return self.stopTime - self.startTime
        else:
            return time.time() - self.startTime
