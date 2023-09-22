import sys

import numpy as np

import log


class Origin:
    def __init__(self, args) -> None:
        self.source = sys.stdin if args.input is None else open(args.input, "r")

        self.lines = np.array(self.source.readlines(), dtype=np.float64)
        self.len = len(self.lines)
        self.elapsed = np.sum(self.lines)
        self.source.close()

        if self.len == 0:
            raise RuntimeError("empty input source")

        log.c.debug("origin reading from %s" % self.source.name)
        with np.printoptions(threshold=6, precision=4, edgeitems=2):
            log.c.info("origin lines (%d) %s" % (self.len, self.lines))
        log.c.info("origin elapsed %.3fs" % self.elapsed)
