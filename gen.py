import itertools
import random
import sys

import numpy as np
import pandas as pd
import yaml
from pandas.core.frame import itertools

import conv
import log
import origin


class Output:
    def __init__(self, args) -> None:
        self.yaml = {"expected": {}, "workload": []}
        self.rates = np.array([], dtype=np.int64)
        self.requests = np.int64(0)
        self.elapsed = np.float64(0)
        self.deltac = np.float64(0)
        self.ratec = np.int64(0)
        self.dest = sys.stdout if args.output is None else open(args.output, "w")
        self.rem = np.float64(0)
        self.random = args.random
        self.apipool = []

        log.c.debug("emitting workload file")
        if self.random is not None:
            log.c.debug("using random with seed %d" % self.random)

        self.read(args)

        log.c.debug("api pool %s" % self.apipool)

    def read(self, args):
        if args.apipool is not None:
            log.c.info("output extracting APIs from cli")
            self.apipool = args.apipool
        elif args.apispec is not None:
            log.c.info("output extracting APIs from %s" % args.apispec)
            with open(args.apispec, "r") as apispec:
                for k in yaml.safe_load(apispec)["api"].keys():
                    self.apipool.append(k)


class C:
    def __init__(self, args) -> None:
        self.origin = origin.Origin(args)
        self.output = Output(args)

        self.run()
        self.write()

    def run(self):
        if self.output.random is not None:
            random.seed(self.output.random)
            self.select = self.rand
        else:
            self.apigen = itertools.cycle(self.output.apipool)
            self.select = self.next

        self.output.yaml["expected"]["duration"] = conv.dtos(pd.Timedelta("%fs" % self.origin.elapsed))

        for delta in self.origin.lines:
            self.output.elapsed += delta  # increment elapsed by delta
            self.output.deltac += delta  # increment delta counter by delta
            if self.output.deltac >= 1:  # delta counter is >= 1s
                self.output.rates = np.append(self.output.rates, self.output.ratec)  # append rate
                self.output.deltac -= 1  # decrement delta counter by 1s and keep remainder
                self.output.rem = self.output.deltac  # store remainder for runtime checks
                self.output.ratec -= self.output.ratec  # reset rate counter
            self.output.ratec += 1  # increment by 1 second

        if not np.isclose(self.output.rem, 0):
            raise RuntimeError("time alignment (error %fs != 0)" % self.output.rem)
        if not np.isclose(self.output.elapsed, self.origin.elapsed):
            raise RuntimeError("elapsed error (%.3f...s < %.3f...s)" % (self.output.elapsed, self.origin.elapsed))

        self.output.requests = np.sum(self.output.rates)
        self.output.yaml["expected"]["requests"] = self.output.requests.item()

        for rate in self.output.rates:
            api = self.select()
            self.output.yaml["workload"].append({"api": api, "rate": f"{rate}/s"})

    def next(self):
        return next(self.apigen)

    def rand(self):
        return random.choice(self.output.apipool)

    def write(self):
        log.c.debug("output writing yaml to %s" % (self.output.dest.name))

        yaml.dump(self.output.yaml, self.output.dest)
        self.output.dest.close()
