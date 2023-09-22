import argparse
import os
import sys
from pathlib import Path

import pandas as pd

args: argparse.Namespace


def init():
    cli = argparse.ArgumentParser(prog="ac", description="asymmetric trace converter")

    cmd = cli.add_subparsers(dest="cmd")

    cmd_cut = cmd.add_parser("cut")
    cmd_cut.add_argument("-i", help="input trace file", type=str, dest="input", metavar="FILE", action=isfile())
    cmd_cut.add_argument("-o", help="output trace file", type=str, dest="output", metavar="FILE", action=notfile())
    cmd_cut.add_argument("-t", help="time string to cut", type=pd.Timedelta, required=True, dest="time", metavar="TIME", action=isgtzero())

    cmd_zip = cmd.add_parser("zip")
    cmd_zip.add_argument("-i", help="input trace file", type=str, dest="input", metavar="FILE", action=isfile())
    cmd_zip.add_argument("-o", help="output trace file", type=str, dest="output", metavar="FILE", action=notfile())
    cmd_zip.add_argument("-t", help="time string to compress to", type=pd.Timedelta, required=True, dest="time", metavar="TIME", action=isgtzero())

    cmd_gen = cmd.add_parser("gen")
    cmd_gen.add_argument("-i", help="input trace file", type=str, dest="input", metavar="FILE", action=isfile())
    cmd_gen.add_argument("-o", help="output workload file", type=str, dest="output", metavar="FILE", action=notfile())
    cmd_gen.add_argument("-r", help="use random seed for api select", type=int, dest="random", metavar="SEED")
    cmd_gen_api = cmd_gen.add_mutually_exclusive_group(required=True)
    cmd_gen_api.add_argument("-a", help="input apispec file", type=str, dest="apispec", metavar="APIs")
    cmd_gen_api.add_argument("-A", help="api pool", type=str, dest="apipool", metavar="APIs", nargs="+")

    global args
    args = cli.parse_args()

    if len(sys.argv) == 1:
        cli.print_usage()
        cmd_cut.print_usage()
        cmd_zip.print_usage()
        cmd_gen.print_usage()
        sys.exit(1)


def ecli(parser, *args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)
    parser.print_help()
    sys.exit(1)


def isfile():
    class A(argparse.Action):
        def __call__(self, parser, args, file, _) -> None:
            if not Path(file).resolve().is_file():
                ecli(parser, "error: -i '%s' file does not exists\n" % file)
            setattr(args, self.dest, file)

    return A


def notfile():
    class A(argparse.Action):
        def __call__(self, parser, args, file, _) -> None:
            path = Path(file)
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.resolve().is_file():
                ecli(parser, "error: -o '%s' file exists\n" % file)
            setattr(args, self.dest, file)

    return A


def isgtzero():
    class A(argparse.Action):
        def __call__(self, parser, args, time, _) -> None:
            if time.total_seconds() == 0:
                ecli(parser, "error: -t arg time string must be >= 1s\n")
            setattr(args, self.dest, time)

    return A
