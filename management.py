import os
import logging
import argparse


class Reminders():
    def __init__(self):
        parser = argparse.ArgumentParser(prog='Management Scripts', description='')
        parser.add_argument('-l', '--log',
                            default='INFO',
                            help='The logging level to be used.')

        args = parser.parse_args()
        log_level = getattr(logging, args.log.upper(), None)

        if not isinstance(log_level, int):
            print('Invalid log level: {}'.format(args.log))
            exit()

        if os.path.exists(LOGHOME) is False:
            os.mkdir(LOGHOME)

        filename = os.path.join(LOGHOME, 'reminders.log')
        logging.basicConfig(filename=filename,
                            format='%(asctime)s|%(levelname)s:%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=log_level)


if __name__ == "__main__":
    print()
