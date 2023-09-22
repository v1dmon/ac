import cli
import conv
import cut
import gen
import log
import zip


def main():
    cli.init()
    log.init(cli.args.cmd)
    if cli.args.cmd == "cut":
        try:
            cut.C(cli.args)
        except Exception as e:
            log.c.error(e)
    elif cli.args.cmd == "zip":
        try:
            zip.C(cli.args)
        except Exception as e:
            log.c.error(e)
    elif cli.args.cmd == "gen":
        try:
            gen.C(cli.args)
        except Exception as e:
            log.c.error(e)


if __name__ == "__main__":
    main()
