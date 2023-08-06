# -*- coding: utf-8 -*-
import io

def get_file1_tra(file1, M=1):
    read = io.open(file1, "r", encoding='utf-8')
    lines = read.readlines()
    Line = 0
    Mode = 1
    Tran = {}
    Boolean = False
    if M == 1:
        for line in lines:
            Line += 1

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
                            Context = lines[Line]
                            Tran[Title] = Context
                            Boolean = False
                if Mode == 2:
                    siine = line.strip()
                    if siine[:3] == "old":
                        Title = line
                        Context = lines[Line]
                        Tran[Title] = Context

            except IndexError:
                pass
    elif M == 2:
        for line in lines:
            Line += 1

            try:
                if line[0:9] == "translate" or Boolean:
                    if line[-9:-1] == "strings:":
                        Mode = 2
                        Boolean = False
                    elif Mode == 1 and line[0:9] == "translate":
                        Title = line
                        Context = lines[Line + 2]
                        Tran[Title] = Context
                        Boolean = False
                if Mode == 2:
                    siine = line.strip()
                    if siine[:3] == "old":
                        Title = line
                        Context = lines[Line]
                        Tran[Title] = Context

            except IndexError:
                pass
    elif M == 3:
        Num = 0
        for line in lines:
            Line += 1

            try:
                if line[0:9] == "translate" or Boolean:
                    if line[-9:-1] == "strings:":
                        Mode = 2
                        Boolean = False
                    elif Mode == 1:
                        Num += 1
                        Context = lines[Line + 2]
                        Tran[Num] = Context
                        Boolean = False
                if Mode == 2:
                    siine = line.strip()
                    if siine[:3] == "old":
                        Title = line
                        Context = lines[Line]
                        Tran[Title] = Context

            except IndexError:
                pass


    read.close()

    return Tran

