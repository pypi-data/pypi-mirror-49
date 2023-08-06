# -*- coding: utf-8 -*-

from os import path
import io
import get_tran_inf

def change_file2(file2, Dic, M):
    amount = 0

    r = io.open(file2, "r", encoding='utf-8')
    lines = r.readlines()

    L = lines[:]
    Line = 0
    Mode = 1
    Boolean = False
    Num = 0
    for line in lines:
        Line += 1

        if M == 1:
            try:
                if line[0:9] == "translate" or Boolean:
                    if line[-9:-1] == "strings:":
                        Mode = 2
                        Boolean = False
                    elif Mode == 1 and Boolean == False:
                        Boolean = True
                    elif Boolean and Mode == 1:
                        sline = line.strip()
                        if sline[0] == "#":
                            Title = line
                            for title, context in Dic.items():
                                if Title == title and L[Line] != context:
                                    amount += 1
                                    L[Line] = context

                            Boolean = False
                if Mode == 2:
                    siine = line.strip()
                    if siine[:3] == "old":
                        Title = line
                        for title, context in Dic.items():
                            if Title == title and L[Line] != context:
                                amount += 1
                                L[Line] = context

            except IndexError:
                pass
        elif M == 2:
            try:
                if line[0:9] == "translate":
                    if line[-9:-1] == "strings:":
                        Mode = 2
                        Boolean = False
                    elif Mode == 1:
                        for title, context in Dic.items():
                            if line == title and L[Line + 2] != context:
                                amount += 1
                                L[Line + 2] = context
                if Mode == 2:
                    siine = line.strip()
                    if siine[:3] == "old":
                        Title = line
                        for title, context in Dic.items():
                            if Title == title and L[Line] != context:
                                amount += 1
                                L[Line] = context

            except IndexError:
                pass
        elif M == 3:
            try:
                if line[0:9] == "translate":
                    Num += 1
                    if line[-9:-1] == "strings:":
                        Mode = 2
                        Boolean = False
                    elif Mode == 1:
                        for num, context in Dic.items():
                            if Num == num:
                                if L[Line + 2] != context:
                                    amount += 1
                                    L[Line + 2] = context
                                else:
                                    continue
                if Mode == 2:
                    siine = line.strip()
                    if siine[:3] == "old":
                        Title = line
                        for title, context in Dic.items():
                            if Title == title and L[Line] != context:
                                amount += 1
                                L[Line] = context

            except IndexError:
                pass

    r.close()

    w = io.open(file2, "w", encoding='UTF-8')
    w.writelines(L)

    return amount

def Replace_Traslation(File1, File2, exchange=False, mode=1):
    if File1 == "" or File2 == "":
        return "Error: Please enter the file"

    if path.exists(File1) == False or path.exists(File2) == False:
        return "Error: Please check if the file exists"

    Dic = get_tran_inf.get_file1_tra(File1, mode)

    amount = change_file2(File2, Dic, mode)

    Return = '%d lines of text have been processed successfully' % amount
    return Return