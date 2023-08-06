# -*- coding: utf-8 -*-

import argparse
import exc_tran
import repl_tran


def main():
    parser = argparse.ArgumentParser()

    parser.description = 'Renpy\'s Tools'
    parser.add_argument('files', metavar='FILE', nargs='*', action='append',help='Set the file to be processed when -r is selected')
    parser.add_argument('-e', '--exchange', dest='file', type=str, help='Select the file to be reversed')
    parser.add_argument('-r', '--replace', dest='rep', type=str, help='Select the file to be replace')


    args = parser.parse_args()

    if args.file and len(args.files[0]) == 0:
        print(exc_tran.exchange_Tran(args.file))
    elif args.rep and len(args.files[0]) == 1:
        print(repl_tran.Replace_Traslation(args.rep, args.files[0][0]))
    elif args.rep and len(args.files[0]) == 2:
        print(repl_tran.Replace_Traslation(args.rep, args.files[0][0], mode=int(args.files[0][1])))

    print('If you are puzzled and you can understand Chinese, please view \" Help_Ch.txt \" File.')


main()
