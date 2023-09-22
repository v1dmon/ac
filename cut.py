import sys

import numpy as np

import conv
import log
import origin


class Output:
    def __init__(self, args) -> None:
        self.lines = np.array([], dtype=np.float64)
        self.len = 0
        self.elapsed = np.float64(0)
        self.time = args.time
        self.dest = sys.stdout if args.output is None else open(args.output, "w")
        # self.rem = np.float64(0)

        log.c.debug("cutting to %s", conv.dtos(self.time))


class C:
    def __init__(self, args) -> None:
        self.origin = origin.Origin(args)
        self.output = Output(args)

        self.run()
        self.write()

    def run(self):
        for delta in self.origin.lines:
            self.output.elapsed += delta  # increment by time delta
            if self.output.elapsed >= self.output.time.seconds:  # time limit reached
                # self.output.rem = delta  # store final remainder
                # WARN: should be the last value added to delta time list?
                self.output.lines = np.append(self.output.lines, delta)  # append last
                break
            self.output.lines = np.append(self.output.lines, delta)  # append delta
        self.output.len = len(self.output.lines)
        self.output.elapsed = np.sum(self.output.lines)

        if self.output.len == self.origin.len:
            raise RuntimeError("nothing cut")
        if self.output.len == 0:
            raise RuntimeError("empty output")
        if self.output.elapsed < self.output.time.seconds:
            raise RuntimeError("elapsed error (%.3f...s < %.3f...s)" % (self.output.elapsed, self.output.time.seconds))

        with np.printoptions(threshold=6, precision=4, edgeitems=2):
            log.c.info("output lines (%d) %s" % (self.output.len, self.output.lines))
        log.c.info("output elapsed %.3fs" % self.output.elapsed)

    def write(self):
        log.c.debug("output writing lines (%d) to %s" % (self.output.len, self.output.dest.name))

        for delta in self.output.lines:
            self.output.dest.write("%s\n" % delta)
        self.output.dest.close()
