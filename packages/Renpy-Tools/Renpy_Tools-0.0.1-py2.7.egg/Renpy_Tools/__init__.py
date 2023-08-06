# -*- coding: utf-8 -*-

import argparse
import exc_tran
import repl_tran

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('files', metavar='FILE', nargs='*', action='append')
    parser.add_argument('-e', '--exchange', dest='file', type=str)
    parser.add_argument('-r', '--replace', dest='rep', type=str)

    args = parser.parse_args()

    if args.file != "" and len(args.files[0]) == 0:
        print(exc_tran.exchange_Tran(args.file))
    elif args.rep != "" and len(args.files[0]) == 1:
        print(repl_tran.Replace_Traslation(args.rep, args.files[0][0]))
    elif args.rep != "" and len(args.files[0]) == 2:
        print(repl_tran.Replace_Traslation(args.rep, args.files[0][0], mode=int(args.files[0][1])))


main()