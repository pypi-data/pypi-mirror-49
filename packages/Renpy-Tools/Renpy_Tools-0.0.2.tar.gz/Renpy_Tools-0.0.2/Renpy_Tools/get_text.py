def GetText(str, Boolean=False, index="\""):
    if str:
        i = str.find(index)
        if Boolean:
            if str.find("#"):
                R = str.replace("# ", "")
            return R[:i]
        else:
            return str[i:]
def GetLabel(str):
    if str:
        return str[29:]

# print(GetText("    m \"asdasdas\"", True))