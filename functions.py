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


movieRegEx = '\"*(\(*.*\)*[^(")]*[^("|\s)])("|\s)*\(([^\)]*)'


def getMovie(str):
    debug = False
    str = str.decode('iso-8859-1').encode('utf8')[:-1]
    if debug: print("Starting String: " + str)
    str = re.sub('\s*\<[^\>]*\>$', '', str)
    if debug: print('remove ^: ' + str)
    str = re.sub('\s*\[[^\]]*\]$', '', str)
    if debug: print('remove [: ' + str + '?')
    str = re.sub('\s*\(as[^\)]*\)$', '', str)
    if debug: print('remove (as: ' + str + '?')
    str = re.sub('\s*\{[^\}]*\}$', '', str)
    if debug: print('remove {: ' + str + '?')
    str = re.sub('\s*\{[^\}]*\}\}$', '', str)
    if debug: print('remove {{: ' + str + '?')
    year = re.search('\s*\(([^\)]*)\)$', str)
    if debug: print('remove (: ' + str + '?')
    str = re.sub('\s*\([^\)]*\)$', '', str)
    if debug: print "year.groups()"
    if debug: print year.groups()
    if str == None:
        return None
    ret = {'name': str, 'year_id': year.groups()[0], 'year': None}

    # print res.groups()
    # print str
    # print ret

    if ret['year_id'] != None:
        ret['year'] = ret['year_id'].split('/')[0]
        if (ret['year'] == None or not ret['year'].isdigit()):
            ret['year'] = None
    return ret


def getMovieSplit(str):
    str = str.split()
    movieName = []
    movieName.append(str[0])
    k=1
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
    print '---Ended "' + name + '" :' + readableTime(time.time() - timers[name])


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



