def jumpLines(f,numOfLines):
    line = f.readline()
    while (numOfLines > 1 and line != ''):
        line = f.readline()
        numOfLines -= 1


def jumpToLineWithString(f,str):
    line = f.readline()
    while line.find('New  Distribution  Votes  Rank  Title') < 0 and line != '':
        line = f.readline()
