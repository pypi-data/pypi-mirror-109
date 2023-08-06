
# python3

__version__='0.0.0'

import sys


class Prometheus_Vcgencmd:
       
    def __init__(self, args=None):
        self.args = args

    def version(self):
        return __version__

    def run(self, args=None):
        print('run')


def main():

    if sys.argv[1:]:

        if sys.argv[1] == '--version':
            out = Prometheus_Vcgencmd().version()
            print(out)

    else:
        run = Prometheus_Vcgencmd().run()


if __name__ == "__main__":
    sys.exit(main())


