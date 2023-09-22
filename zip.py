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

        log.c.debug("scaling to %s", conv.dtos(self.time))


class C:
    def __init__(self, args) -> None:
        self.origin = origin.Origin(args)
        self.output = Output(args)

        self.run()
        self.write()

    def run(self):
        self.output.lines = np.vectorize(self.vfunc)(self.origin.lines)
        self.output.len = len(self.output.lines)
        self.output.elapsed = np.sum(self.output.lines)

        # TODO: runtime checks
        # self.output.elapsed != self.origin.elapsed

        with np.printoptions(threshold=6, precision=4, edgeitems=2):
            log.c.info("output lines (%d) %s" % (self.output.len, self.output.lines))
        log.c.info("output elapsed %.3fs" % self.output.elapsed)

    def vfunc(self, x):
        return (self.output.time.seconds * x) / self.origin.elapsed

    def write(self):
        log.c.debug("output writing lines (%d) to %s" % (self.output.len, self.output.dest.name))

        for delta in self.output.lines:
            self.output.dest.write("%s\n" % delta)
        self.output.dest.close()
