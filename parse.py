import re
import commands

def GetRegex():
    r = r"[{CMDS}]\s*\(.*\)"
    c = ''.join(commands.commands)
    return r.format(CMDS=c)

def GetCommands(f):
    '''
    Return all valid commands found in a file
    f: An open file
    '''

    reg = GetRegex()
    text = f.read()

    res = re.findall(reg, text)
    for i in range(len(res)):
        res[i] = re.sub("\(\s*","(",res[i])
        res[i] = re.sub("\s*\)",")",res[i])

    return res
