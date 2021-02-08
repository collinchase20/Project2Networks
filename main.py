import sys
import argparse
from Project2.interpreter import FtpInterpreter


def main():
    # Set up an argument parser for the terminal
    parser = argparse.ArgumentParser()


    parser.add_argument('--debug', action='store_true',
                        help='Use this to see debug output from the '
                             'FTP client.')

    # Add arguments
    parser.add_argument('-ls', action='store_true')
    parser.add_argument('-mkdir', action='store_true')
    parser.add_argument('-rm', action='store_true')
    parser.add_argument('rmdir', action='store_true')
    parser.add_argument('-cp', action='store_true')
    parser.add_argument('-mv', action='store_true')

    args = parser.parse_args(sys.argv[1:])

    ftps_interpreter = FtpInterpreter(debug=args.debug)
    ftps_interpreter.cmdloop()


#if __name__ == '__main__':
main()