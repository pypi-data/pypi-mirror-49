# -*- coding: utf-8 -*-

import os, io
import get_tran_inf
def exchange_Tran(file):

    Mode = 1

    amount = 0

    if os.path.exists(file) == False:
        return "Error: Please check if the file exists"
    tra = get_tran_inf.get_file1_tra(file)

    f = io.open(file, "r", encoding='UTF-8')
    line = f.readlines()
    l = line[:]
    f.close()

    Line = 0

    for lines in l:
        Line += 1

        if lines[:9] == "translate" and lines[-9:-1] == "strings:":
            Mode = 2
        for title, context in tra.items():
            if lines == title and Mode == 1:
                amount += 1
                line[Line] = title.replace("# ", "", 1)
                line[Line - 1] = "    # " + context.lstrip()
            elif lines == title and Mode == 2:
                amount += 1
                line[Line] = "   new " + title[7:]
                line[Line - 1] = "   old " + context[7:]

    w = io.open(file, "w", encoding='UTF-8')
    w.writelines(line)
    w.close()

    Return = '%d lines of text have been processed successfully' % amount
    return Return

