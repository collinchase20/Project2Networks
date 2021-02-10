import sys
import argparse
from interpreter import FtpInterpreter


def main():
    # Set up an argument parser for the terminal
    parser = argparse.ArgumentParser()


    parser.add_argument('--debug', action='store_true',
                        help='Use this to see debug output from the '
                             'FTP client.')

    # Add arguments
    parser.add_argument('-ls', '--urlLS', type=str)
    parser.add_argument('-mkdir', '--urlMKDIR', type=str)
    parser.add_argument('-rm', '--urlRM', type=str)
    parser.add_argument('-rmdir', '--urlRMDIR', type=str)

    args = parser.parse_args()

    ftps_interpreter = FtpInterpreter()

    ftps_interpreter.do_connect("networks-teaching-ftp.ccs.neu.edu")


    if (args.ls):
        ftps_interpreter.do_list(args.urlLS)
    elif (args.mkdir):
        ftps_interpreter.do_mkdir(args.urlMKDIR)
    elif (args.rm):
        ftps_interpreter.do_rm(args.urlRM)
    elif (args.rmdir):
        ftps_interpreter.do_rmdir(args.urlRMDIR)
    else:
        print("Should Not Come Here")



    #ftps_interpreter.cmdloop()


#if __name__ == '__main__':
main()