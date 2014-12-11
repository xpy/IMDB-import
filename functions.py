import re
import time
import math


def jumpLines(f, numOfLines):
    line = f.readline()
    while (numOfLines > 1 and line != ''):
        line = f.readline()
        numOfLines -= 1


def jumpToLineWithString(f, str):
    line = f.readline()
    while line.find(str) < 0 and line != '':
        line = f.readline()


movieRegEx = '((\s+\(([^\(\)]+)\))*(\s+\{([^\{\}]+)\})*(\s+\{\{([^\{\}]+)\}\})*(\s+\(([^\(\)]+)\))*(\s+\[([^\[\]]+)\])*(\s+\<([^\<\>]+)\>)*)$'


def wrapRegEx(l, r):
    return '\s+' + l + '([^' + r + l +']*)' + r + '$'


def getFromEnd(l, r, str):
    # print wrapRegEx(l, r)
    ret = re.search(wrapRegEx(l, r), str)
    return None if ret == None else ret.groups()[0]


def removeFromEnd(l, r, str):
    return re.sub(wrapRegEx(l, r), '', str)


def getMovie(str):
    debug = False
    if debug: print("Starting String: " + str)
    movie = {}

    movie['billingPosition'] = getFromEnd('\<', '\>', str)
    str = removeFromEnd('\<', '\>', str)
    if debug: print('remove <: ' + str)

    movie['roles'] = getFromEnd('\[', '\]', str)
    str = removeFromEnd('\[', '\]', str)
    if debug: print('remove [: ' + str + '?')

    movie['creditsName'] = getFromEnd('\(as', '\)', str)
    str = removeFromEnd('\(as', '\)', str)
    if debug: print('remove (as: ' + str + '?')

    movie['episodeName'] = getFromEnd('\{', '\}', str)
    str = removeFromEnd('\{', '\}', str)
    if debug: print('remove {: ' + str + '?')

    str = re.sub('\s+\{[^\}]*\}\}$', '', str)
    if debug: print('remove {{: ' + str + '?')

    str = re.sub('\s+\(([TV]*)\)$', '', str)
    if debug: print('remove {{: ' + str + '?')
    return dict(movie.items() + getMovieSplit(str).items())


def getMovieSplit(str):
    # print(str)
    str = str.split()
    movieName = []
    movieName.append(str[0])
    k = 1
    while k < len(str) - 1 and re.match('\([0-9\/IVXC\?]*\)', str[k]) == None:
        movieName.append(str[k])
        k += 1
    ret = {'name': ' '.join(movieName).replace('"', ''), 'year_id': str[k].replace('(', '').replace(')', ''),
           'year': None}
    if ret['year_id'] != None:
        ret['year'] = ret['year_id'].split('/')[0]
        if (ret['year'] == None or not ret['year'].isdigit()):
            ret['year'] = None
    return ret


timers = {}


def startTimer(name):
    timers[name] = time.time()
    print '---Starting "' + name + '"'


def checkTimer(name):
    print '---Checking "' + name + '" :' + readableTime(time.time() - timers[name])


def analyzedTime(time):
    t = {}
    t['hours'] = int(math.floor(time / 3600))
    time %= 3600
    t['minutes'] = int(math.floor(time / 60))
    time %= 60
    t['seconds'] = int(math.floor(time))
    time = time - t['seconds']
    t['milliseconds'] = int(time * 1000)
    return t


def readableTime(rTime):
    t = analyzedTime(rTime)
    ret = str(t['hours']) + ' Hours, '
    ret += str(t['minutes']) + ' Minutes, '
    ret += str(t['seconds']) + ' Seconds and '
    ret += str(t['milliseconds']) + ' Milliseconds '
    return ret



